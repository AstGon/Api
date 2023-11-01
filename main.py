from typing import Union, List
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Configura el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Reemplaza con la URL de origen de tu aplicación Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Seccion(BaseModel):
    nombre: str
    horario_inicio: str
    horario_fin: str

class Curso(BaseModel):
    nombre: str
    secciones: List[Seccion]

class Profesor(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: int
    cursos: List[Curso]

profesores_data = []

# Agregar datos de 5 profesores a la lista, cada uno con 3 cursos, y cada curso con 3 secciones
profesores_data.append(Profesor(
    nombre="Alejandro",
    apellido="Almeja",
    correo="p@duoc.cl",
    telefono="77777777",
    cursos=[
        Curso(
            nombre="Estadistica",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="09:00 AM", horario_fin="11:00 AM"),
                Seccion(nombre="Seccion2", horario_inicio="11:00 AM", horario_fin="01:00 PM"),
                Seccion(nombre="Seccion3", horario_inicio="02:00 PM", horario_fin="04:00 PM"),
            ]
        ),
        Curso(
            nombre="Algebra",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="10:00 AM", horario_fin="12:00 PM"),
                Seccion(nombre="Seccion2", horario_inicio="01:00 PM", horario_fin="03:00 PM"),
                Seccion(nombre="Seccion3", horario_inicio="03:00 PM", horario_fin="05:00 PM"),
            ]
        ),
        Curso(
            nombre="Matematica",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="09:30 AM", horario_fin="11:30 AM"),
                Seccion(nombre="Seccion2", horario_inicio="11:30 AM", horario_fin="01:30 PM"),
                Seccion(nombre="Seccion3", horario_inicio="02:30 PM", horario_fin="04:30 PM"),
            ]
        )
    ]
))

profesores_data.append(Profesor(
    nombre="Alejandra",
    apellido="Gonzalez",
    correo="ale@duoc.cl",
    telefono="777456647",
    cursos=[
        Curso(
            nombre="App movil",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="09:00 AM", horario_fin="11:00 AM"),
                Seccion(nombre="Seccion2", horario_inicio="11:00 AM", horario_fin="01:00 PM"),
                Seccion(nombre="Seccion3", horario_inicio="02:00 PM", horario_fin="04:00 PM"),
            ]
        ),
        Curso(
            nombre="Web",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="10:00 AM", horario_fin="12:00 PM"),
                Seccion(nombre="Seccion2", horario_inicio="01:00 PM", horario_fin="03:00 PM"),
                Seccion(nombre="Seccion3", horario_inicio="03:00 PM", horario_fin="05:00 PM"),
            ]
        ),
        Curso(
            nombre="Diseño",
            secciones=[
                Seccion(nombre="Seccion1", horario_inicio="09:30 AM", horario_fin="11:30 AM"),
                Seccion(nombre="Seccion2", horario_inicio="11:30 AM", horario_fin="01:30 PM"),
                Seccion(nombre="Seccion3", horario_inicio="02:30 PM", horario_fin="04:30 PM"),
            ]
        )
    ]
))

# Puedes hacer lo mismo para los otros profesores

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/profesor/{profesor_id}")
def read_item(profesor_id: int, q: Union[str, None] = None):
    if profesor_id < len(profesores_data):
        return {"profesor_id": profesor_id, "profesor": profesores_data[profesor_id], "q": q}
    else:
        return {"message": "Profesor no encontrado"}

@app.put("/profesor/{profesor_id}")
def update_item(profesor_id: int, profesor: Profesor):
    if profesor_id < len(profesores_data):
        profesores_data[profesor_id] = profesor
        return {"profesor_nombre": profesor.nombre, "profesor_id": profesor_id, "message": "Profesor actualizado exitosamente"}
    else:
        return {"message": "Profesor no encontrado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/profesor/{profesor_id}/cursos")
def get_cursos_profesor(profesor_id: int):
    if profesor_id < len(profesores_data):
        cursos_profesor = profesores_data[profesor_id].cursos
        return {"cursos": cursos_profesor}
    else:
        return {"message": "Profesor no encontrado"}