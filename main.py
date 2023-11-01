from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from typing import Union



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Reemplaza con la URL de tu aplicación Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


professors_db = {}
students_db = {}

class User(BaseModel):
    email: str
    password: str
 

class Section(BaseModel):
    seccion: str
    horario_inicio: str
    horario_fin: str

class Professor(User):
    nombre: str
    apellido: str
    materias: List[str]
    secciones: List[Section]

class Student(User):
    nombre: str
    apellido: str   
    materias_asistencia: List[str]


# Ingresar datos de ejemplo
professors_db["juan@gmail.com"] = Professor(
    nombre="Juan",
    apellido="González",
    email="juan@gmail.com",
    password="password123",
    materias=["Matemáticas", "Física"],
    secciones=[
        Section(seccion="A", horario_inicio="08:00", horario_fin="10:00"),
        Section(seccion="B", horario_inicio="10:15", horario_fin="12:15")
    ]
)

students_db["maria@gmail.com"] = Student(
    nombre="María",
    apellido="Pérez",
    email="maria@gmail.com",
    password="password456",
    materias_asistencia=["Matemáticas", "Física"]
)    

# Ingresar más datos de ejemplo para profesores
professors_db["ana@gmail.com"] = Professor(
    nombre="Ana",
    apellido="López",
    email="ana@gmail.com",
    password="password789",
    materias=["Historia", "Literatura"],
    secciones=[
        Section(seccion="A", horario_inicio="09:30", horario_fin="11:00"),
        Section(seccion="B", horario_inicio="11:15", horario_fin="12:45")
    ]
)


students_db["carlos@gmail.com"] = Student(
    nombre="Carlos",
    apellido="Martínez",
    email="carlos@gmail.com",
    password="password101",
    materias_asistencia=["Historia", "Matemáticas"]
)

students_db["laura@gmail.com"] = Student(
    nombre="Laura",
    apellido="Gómez",
    email="laura@gmail.com",
    password="password202",
    materias_asistencia=["Literatura", "Física"]
)


@app.post("/professors/", response_model=Professor)
def create_professor(professor: Professor):
    professors_db[professor.email] = professor
    return professor

@app.get("/professors/{email}", response_model=Professor)
def read_professor(email: str):
    if email in professors_db:
        return professors_db[email]
    raise HTTPException(status_code=404, detail="Professor not found")

@app.get("/professors/{email}/materias", response_model=List[str])
def get_professor_materias(email: str):
    if email in professors_db:
        professor = professors_db[email]
        return professor.materias
    raise HTTPException(status_code=404, detail="Professor not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/authenticate/")
def authenticate_user(user_info: User):
    if user_info.correo in professors_db:
        return {"user_type": "profesor"}
    elif user_info.correo in students_db:
        return {"user_type": "alumno"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@app.post("/login")
async def login(user: User):
    # Verifica si las credenciales coinciden con los valores en la base de datos de ejemplo
    if user.email in professors_db:
        professor = professors_db[user.email]
        if professor.password == user.password:
            return {"success": True, "message": "Inicio de sesión exitoso", "email": user.email, "user_type": "profesor"}
    
    elif user.email in students_db:
        student = students_db[user.email]
        if student.password == user.password:
            return {"success": True, "message": "Inicio de sesión exitoso", "email": user.email, "user_type": "alumno"}
    
    # Si las credenciales no son válidas, devuelve un error
    return {"success": False, "message": "Credenciales incorrectas"}

@app.get("/authenticate/")
def authenticate_user(email: str):
    if email in professors_db:
        return {"user_type": "profesor"}
    elif email in students_db:
        return {"user_type": "alumno"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/users/{email}", response_model=Union[Professor, Student])
def get_user_by_email(email: str):
    # Intenta buscar al usuario en las bases de datos de profesores y estudiantes
    if email in professors_db:
        return professors_db[email]
    elif email in students_db:
        return students_db[email]

    # Si el correo electrónico no coincide con ningún usuario, devuelve un error 404
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
