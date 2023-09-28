from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from api_back import api_graphql, api_rest
from dotenv import load_dotenv
from envs import env

import threading

load_dotenv()


api_rest
app = FastAPI()
templates = Jinja2Templates(directory="views")

app.mount("/src", StaticFiles(directory="src"), name="src")
# app.mount("/static", StaticFiles(directory="static"), name="static")


app.secret_key = env('SECRET_KEY')


# Dicionário de cabeçalhos com as informações que você deseja enviar
headers = {
    "Content-Type": "application/json"  # Valor padrão para Content-Type
}

# Modelo para o token de autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

# Variável global para armazenar o token de autenticação
access_token = None

# Função para obter o token de autenticação
async def get_access_token():
    return access_token

# Limite de TimeOut do Login
login_timeout = 300

# Função para limpar o token de autenticação após o tempo limite
def clear_access_token():
    global access_token
    access_token = None

########################## Rotas para RestAPI #####################
@app.get("/")
async def home(request: Request):
    context = {"request": request}
    # global access_token
    # access_token = None
    return templates.TemplateResponse("index.html", context)

# Rota para exibir o formulário de login
@app.get("/login")
async def show_login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)

# Rota para o Login
@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):  
    
    context = {"request": request}
    rota_login = "/login"
    
    # Função call_api com a rota, email e password
    response = await api_rest.call_api(route=rota_login, email=email, password=password, method="POST")
    global access_token

    if response.status_code == 200:
        access_token = response.json().get("token")
        # Timer para limpar o token após o tempo limite
        timer = threading.Timer(login_timeout, clear_access_token)
        timer.start()
        return RedirectResponse("/dashboard",  status_code=303)
    else:
        if response.status_code == 401:
            # Credenciais inválidas
            return templates.TemplateResponse("login.html", context)
        else:
            return templates.TemplateResponse("index.html", context, status_code=307)
        

# Rota para o cadastro de usuário
@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):  
    context = {"request": request}
    rota_cadastro = "/usuario"

    # Chame a API para criar o usuário no Firebase Authentication
    response = await api_rest.call_api(route=rota_cadastro, email=email, password=password, method="POST")

    if response.status_code == 200:
        context["flash_message_success"] = True
        context["flash_message"] = "Usuário cadastrado com sucesso! Agora pode se logar."
        return templates.TemplateResponse("login.html", context)
    else:
        context["flash_message_failure"] = True
        context["flash_message"] = "Usuário já existe!"
        return templates.TemplateResponse("login.html", context)

           
@app.get("/dashboard")
async def dashboard(request: Request, access_token: str = Depends(get_access_token)):
    context = {"request": request}
    if access_token:
        graphql_query = """
        {
          dvds {
            id
            title
            director
            releaseYear
            genre
          }
        }
        """
        graphql_result = await api_graphql.call_graphql_api(graphql_query)

        context["graphql_result"] = graphql_result
        return templates.TemplateResponse("dashboard.html", context)
    else:
        return RedirectResponse("/login")
################ Rotas para RestAPI - FIM ##########################################

############### Rotas para GraphQL ################################################
# Rota para consultas GraphQL
@app.get("/graphql")
async def graphql_dashboard(request: Request, access_token: str = Depends(get_access_token)):
    context = {"request": request}

    if access_token:
        # Faz uma consulta GraphQL aqui
        graphql_query = """
        {
          users {
            id
            name
            email
          }
        }
        """
        graphql_result = await api_graphql.call_graphql_api(graphql_query)
        print("Resultado da consulta GraphQL:", graphql_result)

        # Pode manipular os resultados ou passá-los para o template
        context["graphql_result"] = graphql_result

        return templates.TemplateResponse("dashboard.html", context)
    else:
        return RedirectResponse("/login")
    
# Rota para listar DVDs usando GraphQL
@app.get("/list_dvds")
async def list_dvds(access_token: str = Depends(get_access_token)):
    context = {}

    if access_token:
        # Faz uma consulta GraphQL para obter a lista de DVDs
        graphql_query = """
        {
          dvds {
            id
            title
            director
            releaseYear
            genre
          }
        }
        """
        graphql_result = await api_graphql.call_graphql_api(graphql_query)

        # Pode manipular os resultados ou passá-los para o template
        context["graphql_result"] = graphql_result
        print("Resultado do graphql : ", graphql_result)
        return templates.TemplateResponse("components/list_dvds.html", context)
        # return templates.TemplateResponse("dashboard.html", context)  # Crie um template list_dvds.html para exibir os resultados
    else:
        return RedirectResponse("/login")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
