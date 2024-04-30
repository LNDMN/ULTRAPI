# from fastapi import FastAPI, Form, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
import os


# update pony_models.py
def update_pony_models(pony_models_str: str = None):
    if not pony_models_str:
        with open('pony_models.py', 'r', encoding='utf-8') as pmf:
            pm = pmf.read()
    else:
        pm = pony_models_str
        if 'db.generate_mapping()' in pm:
            pmn = pm.replace('db.generate_mapping()', """db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)\n""")
            with open('pony_models.py', 'w', encoding='utf-8') as pmfn:
                pmfn.write(pmn)


# update crud_generator.py
def update_crud_generator(folder_name='app'):
    with open('generators/crud_generator.py', 'r', encoding='utf-8') as pmf:
        pm = pmf.read()
        if 'import pydantic_models' in pm:
            pmn = pm.replace('import pydantic_models as pm', 'import ' + folder_name + '.pydantic_models as pm')
            with open('generators/crud_generator.py', 'w', encoding='utf-8') as pmfn:
                pmfn.write(pmn)


# update api_generator.py
def update_api_generator(folder_name='app'):
    with open('generators/api_generator.py', 'r', encoding='utf-8') as pmf:
        pm = pmf.read()
        if 'import crud' in pm:
            pmn = pm.replace('import crud', 'import ' + folder_name + '.crud as crud')
            with open('generators/api_generator.py', 'w', encoding='utf-8') as pmfn:
                pmfn.write(pmn)


#restore api_generator.py
def restore_api_generator(folder_name='app'):
    with open('generators/api_generator.py', 'r', encoding='utf-8') as pmf:
        pm = pmf.read()
        if 'import ' + folder_name + '.crud' in pm:
            pmn = pm.replace('import ' + folder_name + '.crud as crud', 'import crud')
            with open('generators/api_generator.py', 'w', encoding='utf-8') as pmfn:
                pmfn.write(pmn)


# restore crud_generator.py
def restore_crud_generator(folder_name='app'):
    with open('generators/crud_generator.py', 'r', encoding='utf-8') as pmf:
        pm = pmf.read()
        if 'import ' + folder_name + '.pydantic_models' in pm:
            pmn = pm.replace('import ' + folder_name + '.pydantic_models as pm', 'import pydantic_models as pm')
            with open('generators/crud_generator.py', 'w', encoding='utf-8') as pmfn:
                pmfn.write(pmn)


# copy pony_models.py to app_folder
def copy_pony_models(folder_name='app'):
    # create folder
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name), exist_ok=True)
    with open('pony_models.py', 'r', encoding='utf-8') as pmf:
        pm = pmf.read()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, 'pony_models.py'), 'w', encoding='utf-8') as pmfn:
            pmfn.write(pm)


def create_pony_models_file(pony_models_str):
    with open('pony_models.py', 'w', encoding='utf-8') as pmfn:
        pmfn.write(pony_models_str)


def generate_files(pony_models_str: str = None, folder_name='app', api_name='api', crud_name='crud', pydantic_models_name='pydantic_models'):

    if not pony_models_str and not os.path.exists('pony_models.py'):
        return False

    copy_pony_models(folder_name)

    # generate files
    from generators import pydantic_models_generator

    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{pydantic_models_name}.py'))
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{crud_name}.py'))
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{api_name}.py'))

    pydantic_models_generator.write_pydantic_models_to_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{pydantic_models_name}.py'))


    # update crud_generator.py
    update_crud_generator(folder_name)
    from generators import crud_generator
    crud_generator.write_crud_to_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{crud_name}.py'), folder_path=folder_name)

    # update api_generator.py
    update_api_generator(folder_name)
    from generators import api_generator
    api_generator.write_api_to_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, f'{api_name}.py'), folder_path=folder_name)

    # restore crud_generator.py
    restore_crud_generator(folder_name)

    # restore api_generator.py
    restore_api_generator(folder_name)


if __name__ == "__main__":
    generate_files()

