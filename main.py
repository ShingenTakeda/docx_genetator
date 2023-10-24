import json

nome_do_modelo = "test"

def add_nome(nome):
    return nome


data = {}

with open(f"{nome_do_modelo}.json", "w") as write:
    json.dump(data, write)
