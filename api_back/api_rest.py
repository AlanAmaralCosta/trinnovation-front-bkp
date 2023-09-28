import httpx
import hashlib
import base64
from dotenv import load_dotenv
from envs import env

load_dotenv()

# Função que gera o hash code
def generate_key_from_password(secret_word):
    # Use um algoritmo de hash seguro, como SHA-256
    hashed_password = hashlib.sha256(secret_word.encode()).digest()
    # A chave pode ser uma representação em base64 do hash
    key = base64.b64encode(hashed_password).decode()
    return key

# Palavra-chave para a criptografia (substitua pela sua própria palavra-chave)
secret_word = env('SECRET_WORD')
key = generate_key_from_password(secret_word)

# Função para fazer uma solicitação HTTP (GET ou POST)
async def call_api(email, password, route=None, method="POST"):
    base_url = env('URL_BASE_BACKEND')
    
    url = f"{base_url}{route}"  # Construa a URL completa

    headers = {
        "Content-Type": "application/json"
    }  # Inicialize os cabeçalhos

    # Gere e envie a chave criptografada no cabeçalho X-Secret-Key
    encrypted_key = generate_key_from_password(secret_word)
    headers["X-Secret-Key"] = encrypted_key

    async with httpx.AsyncClient() as client:
        if method == "POST":
            response = await client.post(url, json={"email": email, "password": password}, headers=headers)
        elif method == "GET":
            response = await client.get(url, headers=headers)
        else:
            raise ValueError("Método HTTP inválido. Use 'GET' ou 'POST'.")

        return response
