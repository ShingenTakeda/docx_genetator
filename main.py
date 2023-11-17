import os
import json
from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse


#Run with this: uvicorn main:app --reload

dir =  os.path.dirname(__file__)

app = FastAPI()

#root should return all models
#Whoever consuming it should either treat it or 
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/JSON/{modelo}")
async def mandarModeloJSON(modelo):
    path = os.path.join(dir, '{arquivo}.json'.format(arquivo = modelo))

    if os.path.exists(path):
        fileJSON = open(path)
        return json.load(fileJSON)
    else:
        return {"ERROR": "Arquivo não existe!"}

@app.get("/docx")
async def mandarModeloDocx(request: Request):
    print("what")
#all other roots should return the actual model