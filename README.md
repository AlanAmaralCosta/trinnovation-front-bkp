# MicroServiço de FrontEnd

Este projeto faz parte da Disciplina **Desenvolvimento Full Stack Avançado** 

O objetivo é um FrontEnd que se conecta com uma API RestFull e uma API GraphQL para autenticar usuários no FireBase e autorizar o acesso ao Dashboard apenas se logado. Uma vez logado o usuário consegue ver o Dashboard que tem dados dinamicos e staticos de exemplo.

As principais tecnologias que serão utilizadas aqui é o:
 - [FastApi](https://flask.palletsprojects.com/en/2.3.x/)
 - [OpenAPI3](https://swagger.io/specification/)
 - [FireBase](https://firebase.google.com/?hl=pt-br)
 - [Docker](https://www.docker.com/)

---
### Pré Requisito
Os outros dois micro serviços precisam estar rodando pois o front end depende deles então antes rodar o front, certifique-se que já subiu os outros dois microserviços.

### Instalação

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando o servidor


Para executar o FrontEnd  basta executar:

```
(env)$ uvicorn app:app
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ uvicorn app:app --reload
```

---
### Acesso no browser

Abra o [http://localhost:8000/](http://localhost:8000/) no navegador para verificar o status do FrontEnd em execução.

### Uso do FrontEnd

Existem áreas livres e protegidas
home e login estão disponíveis
Dashboard está protegida

Então para usar você só precisa ir para a tela de login, informar um email e uma senha e clicar em cadastrar, depois é só usar essas credenciais para se logar no sistema e se divertir.

# Bibliotecas e pré-requisitos
- fastapi
- uvicorn
- jinja2
- pytailwindcss
- python-dotenv
- envs