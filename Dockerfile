# Define a imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY . .

# Define o comando de execução da API
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]