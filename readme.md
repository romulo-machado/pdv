# 🍕 Sistema de Registro de Pedidos - Pizzaria

Este é um sistema web desenvolvido com **Django (Python)** para uma pizzaria. A aplicação permite que os clientes selecionem produtos, adicionem ao carrinho e realizem pedidos, com os itens organizados por categorias como **Combos, Lanches e Bebidas**.

---

## 🚀 Funcionalidades

- ✅ Visualização dos produtos organizados por categoria  
- ✅ Adição de produtos ao carrinho  
- ✅ Cálculo automático de subtotal e total do pedido  
- ✅ Página de carrinho com listagem dos itens  
- ✅ Menu lateral com navegação entre categorias  
- ✅ Sistema de pedidos simples  
- ✅ Integração com Django Admin para cadastro de produtos  

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3  
- 🌐 Django  
- 🎨 Bootstrap 5 (interface responsiva)  
- 💾 SQLite (banco de dados padrão do Django)  

---

## 💻 Como rodar o projeto localmente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


```
2️⃣ 
#  Crie e ative um ambiente virtual (opcional, recomendado)

python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/macOS:
source venv/bin/activate
```bash

```
3️⃣ 
# Instale as dependências

pip install -r requirements.txt
```bash

```
4️⃣ 
# Realize as migrações
python manage.py makemigrations
python manage.py migrate
```bash

```
5️⃣ 
# Crie um superusuário (opcional para acessar o admin)

python manage.py createsuperuser
```bash

```
6️⃣ 
# Execute o servidor de desenvolvimento

python manage.py runserver

# Acesse no navegador:
http://127.0.0.1:8000/
```bash

```
# 📂 Estrutura de diretórios
    ├── registrador/            # App principal (produtos e pedidos)
    ├── registrador_de_pedidos/ # Configurações do projeto Django
    ├── media/                  # Arquivos de imagens dos produtos
    ├── templates/              # Templates HTML
    ├── static/                 # Arquivos estáticos (CSS, JS, imagens)
    ├── db.sqlite3              # Banco de dados SQLite
    ├── manage.py               # Script de gerenciamento Django
```bash

```
# 🤝 Contribuição
Sinta-se livre para abrir issues, sugerir melhorias ou enviar pull requests! 🚀

# 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

# 🔗 Contato
Desenvolvido por Seu Nome
📧 romulomachado1@outlook.com
```bash