import json

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine


router = APIRouter(
    prefix="/geo",
    tags=["Geo"],
)


@router.get("/network")
def get_network_geojson():
    features = []

    with Session(engine) as db:

        # -------------------------
        # ВЕРШИНЫ / СКВАЖИНЫ
        # -------------------------
        vertices = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    ST_AsGeoJSON(geometry) AS geometry
                FROM vertices
                WHERE geometry IS NOT NULL
                ORDER BY id
            """)
        ).mappings().all()

        for vertex in vertices:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(vertex["geometry"]),
                    "properties": {
                        "object_type": "vertex",
                        "id": vertex["id"],
                        "name": vertex["name"],
                    },
                }
            )


        # -------------------------
        # ТРУБЫ
        # -------------------------
        pipes = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    vertex_start_id,
                    vertex_end_id,
                    condition,
                    diameter,
                    material,
                    ST_AsGeoJSON(geometry) AS geometry
                FROM pipes
                WHERE geometry IS NOT NULL
                ORDER BY id
            """)
        ).mappings().all()

        for pipe in pipes:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(pipe["geometry"]),
                    "properties": {
                        "object_type": "pipe",
                        "id": pipe["id"],
                        "name": pipe["name"],
                        "vertex_start_id": pipe["vertex_start_id"],
                        "vertex_end_id": pipe["vertex_end_id"],
                        "condition": pipe["condition"],
                        "diameter": pipe["diameter"],
                        "material": pipe["material"],
                    },
                }
            )


        # -------------------------
        # ЧАСТИ ТРУБ
        # -------------------------
        pipe_parts = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    pipe_id,
                    ST_AsGeoJSON(geometry) AS geometry
                FROM pipe_parts
                WHERE geometry IS NOT NULL
                ORDER BY id
            """)
        ).mappings().all()

        for part in pipe_parts:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(part["geometry"]),
                    "properties": {
                        "object_type": "pipe_part",
                        "id": part["id"],
                        "name": part["name"],
                        "pipe_id": part["pipe_id"],
                    },
                }
            )


    return {
        "type": "FeatureCollection",
        "features": features,
    }