from pymongo import MongoClient

# Altere a URL conforme necessário
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)

# Nome do banco de dados
db = client["meubanco"]

# Exemplo de acesso à coleção (tabela)
usuarios_collection = db["usuarios"]
