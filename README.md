# StockFlow — Gestão de Estoque com Flask

Template completo de um sistema web de gestão de estoque para estudos e evolução.

## Tecnologias

- Python
- Flask
- SQLite
- Jinja2
- Bootstrap 5
- Bootstrap Icons
- HTML5/CSS3
- Git/GitHub

## Funcionalidades

### Login
- E-mail e senha.
- Sessão Flask.
- Logout.
- Proteção das páginas internas com `login_required`.

> A senha está simplificada neste template didático. Para produção, utilize hash com `werkzeug.security`.

### Usuários
- Cadastro.
- Nome.
- E-mail.
- Telefone.
- Perfil: usuário ou gestor.
- Data de nascimento.
- CEP.
- Endereço.
- Número.
- Complemento.
- Cidade.
- Estado.
- Listagem.

### Produtos
- Cadastro.
- ID automático.
- Nome.
- Breve descrição.
- Quantidade inicial.
- Listagem.
- Saída por ID e quantidade.
- Bloqueio de saída superior ao estoque.

## Interface

A interface foi criada com Bootstrap 5 e Bootstrap Icons e possui:

- Dashboard administrativo.
- Sidebar profissional.
- Topbar.
- Cards de indicadores.
- Tabelas responsivas.
- Badges para status.
- Formulários organizados por seção.
- Estados vazios.
- Tela de login em duas colunas.
- Responsividade para telas menores.

### Alternar sidebar/topnav

Em `templates/base.html`:

```jinja2
{% set layout = 'sidebar' %}
```

Use:

```jinja2
{% set layout = 'topnav' %}
```

para utilizar o menu superior.

As rotas continuam sendo as mesmas.

## Rotas

| URL | Função |
|---|---|
| `/login` | Login |
| `/logout` | Logout |
| `/dashboard` | Dashboard |
| `/usuarios` | Listar usuários |
| `/usuarios/novo` | Cadastrar usuário |
| `/produtos` | Listar produtos |
| `/produtos/novo` | Cadastrar produto |
| `/produtos/saida` | Registrar saída |

A navegação usa `url_for()`:

```jinja2
<a href="{{ url_for('listar_produtos') }}">Produtos</a>
```

## Estrutura

```text
gestao_estoque_flask/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── layouts/
│   │   ├── _sidebar.html
│   │   └── _topnav.html
│   ├── usuarios/
│   │   ├── cadastro.html
│   │   └── listar.html
│   └── produtos/
│       ├── cadastro.html
│       ├── listar.html
│       └── saida.html
└── static/
    └── css/
        └── style.css
```

## Instalação

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Depois acesse:

```text
http://127.0.0.1:5000
```

O banco `estoque.db` é criado automaticamente.

## Primeiro acesso

1. Abra o sistema.
2. Cadastre um usuário diretamente pela aplicação.
3. Use o e-mail cadastrado na tela de login.
4. Para este template didático, qualquer senha não vazia é aceita.

## Git

```bash
git init
git add .
git commit -m "feat: cria sistema de gestao de estoque com flask"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/gestao-estoque-flask.git
git push -u origin main
```

## Melhorias recomendadas para produção

- Hash de senha.
- Controle de autorização por perfil.
- Flask-WTF e CSRF.
- Blueprints.
- Flask-Migrate.
- Histórico de movimentações.
- Edição/exclusão.
- Testes automatizados.
- Variáveis de ambiente.
- Deploy com servidor WSGI.
