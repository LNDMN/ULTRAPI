import inspect
import crud
from typing import get_type_hints


def write_api_to_file(file_path: str, folder_path: str = 'app'):
    api_code = f"""

from fastapi import FastAPI, Query, Path, Body
import {folder_path + '.' if folder_path else ''}crud as crud
from pydantic_models import *  
# from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth  # Импорт модуля авторизации
import crud  # Импорт CRUD операций



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")


# Mount static files, assuming your Vue.js app's entry point is "admin.html" in the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/admin")
async def get_admin_panel():
    # Redirect or serve your Vue.js admin panel statically
    # This is just a placeholder; serving static files correctly might need adjustments
    return FileResponse('static/admin.html')


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={{"WWW-Authenticate": "Bearer"}},
        )
    access_token = auth.create_access_token(data={{"sub": user.username}})
    return {{"access_token": access_token, "token_type": "bearer"}}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={{"WWW-Authenticate": "Bearer"}},
    )
    return auth.verify_token(token, credentials_exception)


"""

    for name, function in inspect.getmembers(crud, inspect.isfunction):
        # Getting type annotations for function arguments
        print(name, function)
        if name == 'desc' or name == 'select':
            continue
        type_hints = get_type_hints(function)
        # Generating the argument string for the FastAPI function
        args_list = []
        for arg_name, arg_type in type_hints.items():
            if arg_name == "return":
                continue
            arg_str = f"{arg_name}: {arg_type.__name__}"
            # Using Path for path parameters, Query for other parameters, and Body for POST and PUT
            if arg_name == "item_id":
                arg_str += " = Path(...)"
            elif arg_name == "filters":
                arg_str += " = Query"
            elif name.startswith(("create_", "update_")):
                arg_str += " = Body(...)"
            else:
                arg_str += " = Query(None)"
            args_list.append(arg_str)
        args_str = ", ".join(args_list)

        # Determining the HTTP method and path
        method, route = "get", "/"
        if name.startswith("create_"):
            method, route = "post", f"/{name[7:]}/"
        elif name.startswith("get_") and name.endswith("s"):
            method, route = "get", f"/{name[4:]}/"
        elif name.startswith("get_"):
            method, route = "get", f"/{name[4:]}/{{item_id}}"
        elif name.startswith("update_"):
            method, route = "put", f"/{name[7:]}/{{item_id}}"
        elif name.startswith("delete_"):
            method, route = "delete", f"/{name[7:]}/{{item_id}}"

        # Generating the code for the endpoint
        api_code += f"""
@app.{method}("{route}")
async def {name}({args_str}):
    return await crud.{name}({', '.join([arg.split(':')[0] for arg in args_list])})

"""
    api_code +="""
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', reload=True)
    """

    # Writing the generated code to a file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(api_code)

# Example call to the function to generate the API file
# write_api_to_file("api.py")
