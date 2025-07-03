# 🎬 MovieEnjoyer - Sistema de Avaliação de Filmes - Backend

MovieEnjoyer é uma aplicação web desenvolvida com Flask (backend) e HTML/CSS/JavaScript puro (frontend), que permite que usuários se cadastrem, façam login, visualizem os filmes mais assistidos, marquem filmes como assistidos e deixem suas avaliações.

---

## 🚀 Funcionalidades

- Cadastro e login de usuários
- Listagem dos filmes mais assistidos em cards
- Detalhes completos de cada filme
- Marcar filmes como assistidos
- Avaliar filmes assistidos
- Backend RESTful com documentação Swagger: integrada

---

## 🧰 Tecnologias Utilizadas

- **Backend:** Python 3.11+, Flask, Flask-RESTX, SQLAlchemy
- **Banco de dados:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Documentação da API:** Swagger (via Flask-RESTX)

---

## ⚙️ Instalação e Configuração

### 🔁 1. Clone o repositório
```bash
git clone https://github.com/arthurmourab/backend-mvp-full-stack-basico.git
```

### 🐍 2. Crie e ative um ambiente virtual
#### Windows:
Criar a pasta .venv na raíz do repositório
```bash
py -3 -m venv .venv
```

Ative o ambiente virtual criado
```bash
.venv\Scripts\activate
```
<br />

#### macOS/Linux:
```bash
python3 -m venv .venv
```

```bash
 . .venv/bin/activate
```

### 📦 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### ▶ 4. Popule o banco e execute a aplicação
#### Popule o banco com o arquivo seed.py
```bash
flask --app flaskr seed-db
```
<br />

#### Pronto, agora é só executar a aplicação!
```bash
flask --app flaskr run
```

ou 
```bash
flask --app flaskr run --debug
```
para executar no modo de debug







