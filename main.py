from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from typing import Union



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Ajusta según tus necesidades
    allow_headers=["*"],  # O especifica los encabezados permitidos
)
professors_db = {}
students_db = {}

class User(BaseModel):
    email: str
    password: str

class Clase(BaseModel):
    seccion: str
    horario_inicio: str
    horario_fin: str

class Materia(BaseModel):
    id: str
    nombre: str
    secciones: List[Clase]

class Professor(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    materias: List[Materia]

class Student(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str
    materias_asistencia: List[str]


# Ingresar datos de ejemplo
professors_db["juan@gmail.com"] = Professor(
    nombre="Juan",
    apellido="González",
    email="juan@gmail.com",
    password="password123",
    materias=[
        Materia(
            id="5",
            nombre="Historia",
            secciones=[
                Clase(seccion="A", horario_inicio="09:30", horario_fin="11:00"),
                Clase(seccion="B", horario_inicio="11:15", horario_fin="12:45")
            ]
        ),
        Materia(
            id="6",
            nombre="Literatura",
            secciones=[
                Clase(seccion="X", horario_inicio="14:00", horario_fin="15:30")
            ]
        )
    ]
)

professors_db["maria@gmail.com"] = Professor(
    nombre="María",
    apellido="Pérez",
    email="maria@gmail.com",
    password="password456",
    materias=[
        Materia(
            id="2",
            nombre="Matemáticas",
            secciones=[
                Clase(seccion="A", horario_inicio="08:00", horario_fin="10:00"),
                Clase(seccion="B", horario_inicio="10:15", horario_fin="12:15")
            ]
        ),
        Materia(
            id="1",
            nombre="Física",
            secciones=[
                Clase(seccion="X", horario_inicio="13:30", horario_fin="15:30")
            ]
        )
    ]
)    


professors_db["ana@gmail.com"] = Professor(
    nombre="Ana",
    apellido="López",
    email="ana@gmail.com",
    password="password789",
    materias=[
        Materia(
            id="3",
            nombre="Web",
            secciones=[
                Clase(seccion="A", horario_inicio="08:00", horario_fin="10:00"),
                Clase(seccion="B", horario_inicio="10:15", horario_fin="12:15")
            ]
        ),
        Materia(
            id="4",
            nombre="App",
            secciones=[
                Clase(seccion="X", horario_inicio="13:30", horario_fin="15:30")
            ]
        )
    ]
)


students_db["carlos@gmail.com"] = Student(
    nombre="Carlos",
    apellido="Martínez",
    email="carlos@gmail.com",
    password="password101",
    materias_asistencia=["2", "3"]
)

students_db["laura@gmail.com"] = Student(
    nombre="Laura",
    apellido="Gómez",
    email="laura@gmail.com",
    password="password202",
    materias_asistencia=["1", "4"]
)




@app.get("/professors/{email}", response_model=Professor)
async def read_professor(email: str):
    if email in professors_db:
        return professors_db[email]
    raise HTTPException(status_code=404, detail="Professor not found")

@app.get("/professors/{email}/materias", response_model=List[str])
async def get_professor_materias(email: str):
    if email in professors_db:
        professor = professors_db[email]
        return professor.materias
    raise HTTPException(status_code=404, detail="Professor not found")


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

@app.get("/authenticate")
async def authenticate_user(email: str):
    if email in professors_db:
        return {"user_type": "profesor"}
    elif email in students_db:
        return {"user_type": "alumno"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/users/{email}", response_model=Union[Professor, Student])
async def get_user_by_email(email: str):
    # Intenta buscar al usuario en las bases de datos de profesores y estudiantes
    if email in professors_db:
        return professors_db[email]
    elif email in students_db:
        return students_db[email]

    # Si el correo electrónico no coincide con ningún usuario, devuelve un error 404
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
