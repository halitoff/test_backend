from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Включение CORS (обязательно!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модели данных
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# "База данных" в памяти
fake_db = {}


# Сервисные функции
def fake_hash_password(password: str):
    return "fake_hashed_" + password  # В реальном приложении используйте bcrypt!


# Роуты
@app.post("/register")
async def register(user: UserCreate):
    if user.username in fake_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Сохраняем "хэшированный" пароль
    fake_db[user.username] = fake_hash_password(user.password)
    return {"message": "User created successfully"}


@app.post("/login")
async def login(user: UserLogin):
    stored_password = fake_db.get(user.username)
    if not stored_password or stored_password != fake_hash_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return {
        "access_token": f"fake-token-for-{user.username}",
        "token_type": "bearer"
    }


@app.get("/protected-route")
async def protected_route(username: str = "test"):
    return {
        "message": f"Hello {username}!",
        "secret_data": "This is protected information"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)