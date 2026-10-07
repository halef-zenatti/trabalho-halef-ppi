# Gestoq — Gestão de Estoque 

Template gestão de estoque

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
4. Qualquer senha não vazia é aceita.

## Git

```bash
git init
git add .
git commit -m "feat: cria sistema de gestao de estoque com flask"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/gestao-estoque-flask.git
git push -u origin main
```
