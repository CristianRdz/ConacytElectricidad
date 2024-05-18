from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from functions import getEnergyByCords, capacidadRed

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/energia/{lat}/{lon}")
async def get_energia(lat: float, lon: float):
    return await getEnergyByCords(lat, lon)

@app.post("/red/{lat}/{lon}")
async def get_red(lat: float, lon: float):
    return await capacidadRed(lat, lon)




