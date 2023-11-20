import os
import json
import glob
from docx import Document
from docx.shared import Inches
from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile
from starlette.background import BackgroundTask

#Run with this: uvicorn main:app --reload

#Delete temp files in tmp
def deleteTemp():
    files = glob.glob(tmpDir + "*.docx")
    for f in files:
        os.remove(f)

dir =  os.path.dirname(__file__)
modelosPath = dir + "/modelos/"
tmpDir = dir + "/tmp/"

def json_to_doc(json):
      temp_doc = Document()
      name = ""
      for i in json.items():
            match i[1]["type"]:
                  case "name":
                        print("Nome do documento: " + i[1]["t"])
                        name = i[1]["t"]
                  case "p":
                        #print("paragraph: " + i[1]["p"])
                        print("paragraph|ajuda: " + str(i[1]["ajuda"]))
                        print("paragraph|removivel: " + str(i[1]["removivel"]))
                        print("paragraph|text:" + i[1]["c"][0]["t"])
                        temp_doc.add_paragraph(i[1]["c"][0]["t"])
                  case "i":
                        print("image: " + i[1]["i"])
                        print("image|ajuda: " + i[1]["ajuda"])
                        print("image|removivel: " + str(i[1]["removivel"]))
                  case "h":
                        print("heading: " + i[1]["c"][0]["t"])
                        print("heading|ajuda: " + i[1]["ajuda"])
                        print("heading|removivel: " + str(i[1]["removivel"]))
                        temp_doc.add_heading(i[1]["c"][0]["t"], level=int(i[1]["htype"]))
                  case "t":
                        print(f"table| [ rows: {i[1]['rows']}|cols: {i[1]['cols']} ]")
                        print(f"table|len arrays: {len(i[1]['cells'])}")
                        print(f"table|arrays: {i[1]['cells']}")
                        table = temp_doc.add_table(rows=i[1]["rows"], cols=i[1]["cols"])

                        for t in i[1]["cells"]:
                              if t == i[1]["cells"][0]:
                                    counter = 0
                                    for t in i[1]["cells"][0]:
                                          hdr_cell = table.rows[0].cells
                                          hdr_cell[counter].text = t
                                          counter = counter + 1
                              else:
                                    cell = table.add_row().cells
                                    for b in range(len(t)):
                                          cell[b].text = t[b]

      temp_doc.save(f"{tmpDir}{name}.docx")
      return name

app = FastAPI()

#root should return all models
#Whoever consuming it should either treat it or smth
@app.get("/")
async def root():
    m = []
    for x in os.listdir(dir + "/modelos"):
        if x.endswith(".json"):
            fileJson = open(modelosPath + x)
            m.append(json.load(fileJson))
    return m

@app.get("/JSON/{modelo}")
async def mandarModeloJSON(modelo):
    path = os.path.join(dir + "/modelos/", '{arquivo}.json'.format(arquivo = modelo))
    print(path)
    if os.path.exists(path):
        fileJSON = open(path)
        return json.load(fileJSON)
    else:
        return {"ERROR": "Arquivo não existe!"}

@app.post("/docx")
async def mandarModeloDocx(payload : Request):
    jd = json.loads(await payload.body())
    print(jd)
    name = json_to_doc(jd)
    return FileResponse(f"{tmpDir}{name}.docx", background=BackgroundTask(deleteTemp))#{"Receiced" : await payload.body()}#

@app.post("/docx/{modelo}")
async def mockDocx(modelo):
    fileData = open(os.path.join(dir + "/modelos/", '{arquivo}.json'.format(arquivo = modelo)))
    jd = json.load(fileData)
    json_to_doc(jd)
    return FileResponse(f"{tmpDir}{modelo}.docx", background=BackgroundTask(deleteTemp))