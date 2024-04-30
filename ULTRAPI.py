from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
import json
import auth  # Импорт модуля авторизации, где описаны функции для работы с пользователями и JWT
import uvicorn
import main  # Импорт функций для работы с моделями и генерации файлов

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = auth.verify_token(token, HTTPException(status_code=401, detail="Invalid token"))
    return {"username": user['username'], "roles": user['roles']}


@app.post("/create-user")
async def create_user(username: str = Form(...), password: str = Form(...), roles: str = Form(...)):
    roles_list = json.loads(roles)
    try:
        user = auth.create_user(username, password, roles_list)
        return {"message": "User created successfully", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/update-models")
async def update_models(models: str = Form(...)):
    # Обновление моделей Pony ORM и генерация CRUD API
    try:
        main.create_pony_models_file(models)
        folder_name = 'app'  # Имя папки, где будут храниться сгенерированные файлы
        main.generate_files(models, folder_name=folder_name, api_name='api', crud_name='crud', pydantic_models_name='pydantic_models')
        return {"message": "Models updated and CRUD API generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
