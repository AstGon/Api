from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

professors_db = {}
students_db = {}

class UserBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contraseña: str

class Section(BaseModel):
    seccion: str
    horario_inicio: str
    horario_fin: str

class Professor(UserBase):
    materias: List[str]
    secciones: List[Section]

class Student(UserBase):
    materias_asistencia: List[str]


# Ingresar datos de ejemplo
professors_db["juan@gmail.com"] = Professor(
    nombre="Juan",
    apellido="González",
    correo="juan@gmail.com",
    contraseña="password123",
    materias=["Matemáticas", "Física"],
    secciones=[
        Section(seccion="A", horario_inicio="08:00", horario_fin="10:00"),
        Section(seccion="B", horario_inicio="10:15", horario_fin="12:15")
    ]
)

students_db["maria@gmail.com"] = Student(
    nombre="María",
    apellido="Pérez",
    correo="maria@gmail.com",
    contraseña="password456",
    materias_asistencia=["Matemáticas", "Física"]
)    

# Ingresar más datos de ejemplo para profesores
professors_db["ana@gmail.com"] = Professor(
    nombre="Ana",
    apellido="López",
    correo="ana@gmail.com",
    contraseña="password789",
    materias=["Historia", "Literatura"],
    secciones=[
        Section(seccion="A", horario_inicio="09:30", horario_fin="11:00"),
        Section(seccion="B", horario_inicio="11:15", horario_fin="12:45")
    ]
)


students_db["carlos@gmail.com"] = Student(
    nombre="Carlos",
    apellido="Martínez",
    correo="carlos@gmail.com",
    contraseña="password101",
    materias_asistencia=["Historia", "Matemáticas"]
)

students_db["laura@gmail.com"] = Student(
    nombre="Laura",
    apellido="Gómez",
    correo="laura@gmail.com",
    contraseña="password202",
    materias_asistencia=["Literatura", "Física"]
)


@app.post("/professors/", response_model=Professor)
def create_professor(professor: Professor):
    professors_db[professor.correo] = professor
    return professor

@app.get("/professors/{correo}", response_model=Professor)
def read_professor(correo: str):
    if correo in professors_db:
        return professors_db[correo]
    raise HTTPException(status_code=404, detail="Professor not found")

@app.get("/professors/{correo}/materias", response_model=List[str])
def get_professor_materias(correo: str):
    if correo in professors_db:
        professor = professors_db[correo]
        return professor.materias
    raise HTTPException(status_code=404, detail="Professor not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


