import json
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine


router = APIRouter(
    prefix="/geo",
    tags=["Geo"],
)


class NodeCreate(BaseModel):
    name: str
    vertex_type: Literal["well", "junction"]

    longitude: float
    latitude: float


class NodeUpdate(BaseModel):
    name: str
    vertex_type: Literal["well", "junction"]

    longitude: float
    latitude: float


# =========================================================
# GEOJSON ВСЕЙ СЕТИ
# =========================================================

@router.get("/network")
def get_network_geojson():
    features = []

    with Session(engine) as db:

        vertices = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    vertex_type,
                    ST_X(geometry) AS longitude,
                    ST_Y(geometry) AS latitude,
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

                    "geometry":
                        json.loads(
                            vertex["geometry"]
                        ),

                    "properties": {
                        "object_type": "vertex",
                        "id": vertex["id"],
                        "name": vertex["name"],
                        "vertex_type":
                            vertex["vertex_type"],
                    },
                }
            )


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

                    "geometry":
                        json.loads(
                            pipe["geometry"]
                        ),

                    "properties": {
                        "object_type": "pipe",
                        "id": pipe["id"],
                        "name": pipe["name"],

                        "vertex_start_id":
                            pipe["vertex_start_id"],

                        "vertex_end_id":
                            pipe["vertex_end_id"],

                        "condition":
                            pipe["condition"],

                        "diameter":
                            pipe["diameter"],

                        "material":
                            pipe["material"],
                    },
                }
            )


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

                    "geometry":
                        json.loads(
                            part["geometry"]
                        ),

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


# =========================================================
# СОЗДАНИЕ НОВОГО УЗЛА / СКВАЖИНЫ
# =========================================================

@router.post("/nodes", status_code=201)
def create_node(
    node: NodeCreate,
):
    with engine.begin() as conn:

        result = conn.execute(
            text("""
                INSERT INTO vertices (
                    name,
                    vertex_type,
                    geometry
                )

                VALUES (
                    :name,
                    :vertex_type,

                    ST_SetSRID(
                        ST_MakePoint(
                            :longitude,
                            :latitude
                        ),
                        4326
                    )
                )

                RETURNING
                    id,
                    name,
                    vertex_type
            """),

            {
                "name":
                    node.name,

                "vertex_type":
                    node.vertex_type,

                "longitude":
                    node.longitude,

                "latitude":
                    node.latitude,
            },
        ).mappings().first()

    return dict(result)


# =========================================================
# РЕДАКТИРОВАНИЕ УЗЛА
# =========================================================

@router.patch("/nodes/{vertex_id}")
def update_node(
    vertex_id: int,
    node: NodeUpdate,
):
    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE vertices

                SET
                    name = :name,

                    vertex_type =
                        :vertex_type,

                    geometry =
                        ST_SetSRID(
                            ST_MakePoint(
                                :longitude,
                                :latitude
                            ),
                            4326
                        )

                WHERE id = :vertex_id

                RETURNING id
            """),

            {
                "vertex_id":
                    vertex_id,

                "name":
                    node.name,

                "vertex_type":
                    node.vertex_type,

                "longitude":
                    node.longitude,

                "latitude":
                    node.latitude,
            },
        ).first()


        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Узел не найден",
            )


        # Перестраиваем трубы,
        # связанные с этой вершиной
        conn.execute(
            text("""
                UPDATE pipes AS p

                SET geometry =
                    ST_MakeLine(
                        start_vertex.geometry,
                        end_vertex.geometry
                    )

                FROM
                    vertices AS start_vertex,
                    vertices AS end_vertex

                WHERE
                    start_vertex.id =
                        p.vertex_start_id

                    AND end_vertex.id =
                        p.vertex_end_id

                    AND (
                        p.vertex_start_id =
                            :vertex_id

                        OR

                        p.vertex_end_id =
                            :vertex_id
                    )
            """),

            {
                "vertex_id":
                    vertex_id,
            },
        )


        # Пока участки повторяют трубу
        conn.execute(
            text("""
                UPDATE pipe_parts AS pp

                SET geometry =
                    p.geometry

                FROM pipes AS p

                WHERE
                    pp.pipe_id = p.id

                    AND (
                        p.vertex_start_id =
                            :vertex_id

                        OR

                        p.vertex_end_id =
                            :vertex_id
                    )
            """),

            {
                "vertex_id":
                    vertex_id,
            },
        )


    return {
        "status": "ok",
        "vertex_id": vertex_id,
    }