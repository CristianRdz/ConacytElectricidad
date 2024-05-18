import pandas as pd
from geopy.distance import geodesic
import httpx


async def capacidadRed(lat, lon):
    redes_url = 'https://energia.conacyt.mx/planeas/geodata/electricidad/lineas_transmision_operacion_mayo2022.geojson'
    async with httpx.AsyncClient() as client:
        response = await client.get(redes_url)
    redes = response.json()
    redes_df = pd.json_normalize(redes['features'])
    redes_df = redes_df.fillna('')
    redes_df['distancia'] = redes_df.apply(
        lambda x: geodesic((lat, lon), (x['geometry.coordinates'][0][0][1], x['geometry.coordinates'][0][0][0])).km,
        axis=1)
    return {
        'Nombre': str(redes_df.loc[redes_df['distancia'].idxmin()]['properties.Nombre']),
        'Caracterí': str(redes_df.loc[redes_df['distancia'].idxmin()]['properties.Caracterí']),
        'Voltaje_KV': str(redes_df.loc[redes_df['distancia'].idxmin()]['properties.Voltaje_KV']),
        'Categ': str(redes_df.loc[redes_df['distancia'].idxmin()]['properties.Categ']),
        'voltaje_la': str(redes_df.loc[redes_df['distancia'].idxmin()]['properties.voltaje_la']),
    }


async def getEnergyByCords(lat, lon):
    try:
        plantas_url = 'https://energia.conacyt.mx/planeas/geodata/electricidad/plantas_generadoras_operacion.geojson'
        async with httpx.AsyncClient() as client:
            response = await client.get(plantas_url)
        plantas = response.json()
        plantas_df = pd.json_normalize(plantas['features'])
        plantas_df = plantas_df.fillna('')
        plantas_df['distancia'] = plantas_df.apply(
            lambda x: geodesic((lat, lon), (x['geometry.coordinates'][1], x['geometry.coordinates'][0])).km, axis=1)
        planta_cercana = plantas_df.loc[plantas_df['distancia'].idxmin()]

        return {'central': planta_cercana['properties.central'], 'energet_pr': planta_cercana['properties.energet_pr'],
                'empresa': planta_cercana['properties.empresa'], 'matriz': planta_cercana['properties.matriz'],
                'sector': planta_cercana['properties.sector'], 'fecha_oper': planta_cercana['properties.fecha_oper'],
                'capacid_mw': planta_cercana['properties.capacid_mw'],
                'gener_gwh': planta_cercana['properties.gener_gwh'],
                'entidad': planta_cercana['properties.entidad'],
                'tecnologia': planta_cercana['properties.tecnologia'], }
    except Exception as e:
        return str(e)
