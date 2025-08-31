from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import cafe_logica_difusa as cafe 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CafeRequest(BaseModel):
    hora: float
    estado: float
    clima: float

@app.post("/evaluar")
async def evaluar(req: CafeRequest):
    buf = cafe.evaluar_cafe(req.hora, req.estado, req.clima)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/visualizacion")
async def visualizacion():
    buf = cafe.visualizacion_cafe()
    return Response(content=buf.getvalue(), media_type="image/png")
