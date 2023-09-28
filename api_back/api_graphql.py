import httpx
from envs import env

graphql_endpoint = "http://0.0.0.0:8001/graphql"  # Substitua pela URL correta do seu servidor GraphQL

async def list_dvds():
    query = """
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
    return await call_graphql_api(query)

async def call_graphql_api(query):
    headers = {
        "Content-Type": "application/json",
    }

    data = {"query": query}

    async with httpx.AsyncClient() as client:
        response = await client.post(graphql_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na solicitação GraphQL: {response.text}")
