from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "estoque.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            perfil TEXT NOT NULL CHECK (perfil IN ('usuario', 'gestor')),
            data_nascimento TEXT,
            cep TEXT,
            endereco TEXT,
            numero TEXT,
            complemento TEXT,
            cidade TEXT,
            estado TEXT
        );

        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0)
        );
    """)
    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar o sistema.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


@app.template_filter("perfil")
def perfil_filter(value):
    return "Gestor" if value == "gestor" else "Usuário"


@app.template_filter("data_br")
def data_br(value):
    if not value:
        return ""
    try:
        ano, mes, dia = value.split("-")
        return f"{dia}/{mes}/{ano}"
    except ValueError:
        return value


@app.context_processor
def global_context():
    return {
        "app_name": "StockFlow",
        "app_subtitle": "Gestão de Estoque",
        "usuario_logado": session.get("usuario_nome"),
        "usuario_perfil": session.get("usuario_perfil"),
    }


@app.context_processor
def navigation():
    return {
        "navigation": [
            ("dashboard", "Dashboard", "bi-grid-1x2"),
            ("listar_usuarios", "Usuários", "bi-people"),
            ("cadastrar_usuario", "Novo usuário", "bi-person-plus"),
            ("listar_produtos", "Produtos", "bi-box-seam"),
            ("cadastrar_produto", "Novo produto", "bi-plus-square"),
            ("saida_produto", "Saída de produto", "bi-box-arrow-right"),
        ]
    }


@app.route("/")
def index():
    return redirect(url_for("dashboard" if "usuario_id" in session else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Template didático: qualquer senha não vazia é aceita
        # para um e-mail previamente cadastrado.
        conn = get_db()
        usuario = conn.execute(
            "SELECT id, nome, email, perfil FROM usuarios WHERE lower(email)=?",
            (email,)
        ).fetchone()
        conn.close()

        if usuario and senha:
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            session["usuario_perfil"] = usuario["perfil"]
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    total_usuarios = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_produtos = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    estoque_total = conn.execute(
        "SELECT COALESCE(SUM(quantidade), 0) FROM produtos"
    ).fetchone()[0]
    produtos_baixo = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE quantidade BETWEEN 1 AND 9"
    ).fetchone()[0]
    sem_estoque = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE quantidade = 0"
    ).fetchone()[0]
    conn.close()

    return render_template(
        "dashboard.html",
        total_usuarios=total_usuarios,
        total_produtos=total_produtos,
        estoque_total=estoque_total,
        produtos_baixo=produtos_baixo,
        sem_estoque=sem_estoque,
    )


@app.route("/usuarios")
@login_required
def listar_usuarios():
    conn = get_db()
    usuarios = conn.execute(
        "SELECT * FROM usuarios ORDER BY nome"
    ).fetchall()
    conn.close()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@app.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
def cadastrar_usuario():
    dados = {}

    if request.method == "POST":
        campos = [
            "nome", "email", "telefone", "perfil", "data_nascimento",
            "cep", "endereco", "numero", "complemento", "cidade", "estado"
        ]
        dados = {campo: request.form.get(campo, "").strip() for campo in campos}

        if not dados["nome"] or not dados["email"] or not dados["perfil"]:
            flash("Preencha nome, e-mail e perfil.", "danger")
            return render_template("usuarios/cadastro.html", dados=dados)

        if dados["perfil"] not in ("usuario", "gestor"):
            flash("Perfil inválido.", "danger")
            return render_template("usuarios/cadastro.html", dados=dados)

        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO usuarios
                (nome, email, telefone, perfil, data_nascimento, cep,
                 endereco, numero, complemento, cidade, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(dados.values()))
            conn.commit()
            conn.close()
            flash("Usuário cadastrado com sucesso.", "success")
            return redirect(url_for("listar_usuarios"))
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "danger")

    return render_template("usuarios/cadastro.html", dados=dados)


@app.route("/produtos")
@login_required
def listar_produtos():
    conn = get_db()
    produtos = conn.execute(
        "SELECT * FROM produtos ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("produtos/listar.html", produtos=produtos)


@app.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def cadastrar_produto():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()

        try:
            quantidade = int(request.form.get("quantidade", "0"))
        except ValueError:
            quantidade = -1

        if not nome or quantidade < 0:
            flash("Informe o nome e uma quantidade válida.", "danger")
            return render_template("produtos/cadastro.html")

        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO produtos (nome, descricao, quantidade) VALUES (?, ?, ?)",
            (nome, descricao, quantidade)
        )
        produto_id = cursor.lastrowid
        conn.commit()
        conn.close()

        flash(f"Produto #{produto_id} cadastrado com sucesso.", "success")
        return redirect(url_for("listar_produtos"))

    return render_template("produtos/cadastro.html")


@app.route("/produtos/saida", methods=["GET", "POST"])
@login_required
def saida_produto():
    if request.method == "POST":
        try:
            produto_id = int(request.form.get("id", "0"))
            quantidade = int(request.form.get("quantidade", "0"))
        except ValueError:
            produto_id = quantidade = 0

        if produto_id <= 0 or quantidade <= 0:
            flash("Informe um ID e uma quantidade válidos.", "danger")
            return render_template("produtos/saida.html")

        conn = get_db()
        produto = conn.execute(
            "SELECT * FROM produtos WHERE id=?", (produto_id,)
        ).fetchone()

        if not produto:
            conn.close()
            flash("Produto não encontrado.", "danger")
            return render_template("produtos/saida.html")

        if quantidade > produto["quantidade"]:
            conn.close()
            flash(
                f"Estoque insuficiente. Disponível: {produto['quantidade']} unidade(s).",
                "danger"
            )
            return render_template("produtos/saida.html")

        conn.execute(
            "UPDATE produtos SET quantidade = quantidade - ? WHERE id=?",
            (quantidade, produto_id)
        )
        conn.commit()
        conn.close()

        flash("Saída registrada com sucesso.", "success")
        return redirect(url_for("listar_produtos"))

    return render_template("produtos/saida.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
