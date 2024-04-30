import dbm
import os
import io
from pony_models import *
from pony.orm.core import Entity, Set, Required, Optional
import datetime


def analyze_pony_model(model):
    fields = {}
    for attr in dir(model):
        if attr.startswith('_'):
            continue
        attribute = getattr(model, attr)
        if isinstance(attribute, (Required, Optional)):
            # print("attribute:" ,attribute, "attribute.reverse:", '<===>' ,str(attribute.reverse), '\n==========\n')
            field_type = attribute.py_type
            if field_type in [datetime.date, datetime.datetime, datetime.time, datetime.timedelta]:
                field_type = f'datetime.{field_type.__name__}'
            else:
                field_type = field_type.__name__
            if field_type == 'LongStr':
                field_type = 'str'
            if field_type == 'Decimal':
                field_type = 'float'
            # field_type = f'Optional["{field_type}"]' if isinstance(attribute, Optional) else field_type
            field_type = (f'Annotated["{field_type}", Field({{"required": True,\n'
                          f'                "relation_type": "{"ManyToOne" if str(attribute.reverse).split(".")[1].lower() == str(attribute).split(".")[0].lower()+"s" else "OneToOne"}",\n'
                          f'                "reverse_name": "{attribute.reverse}"}})]') if isinstance(attribute, Required) and field_type in db.entities else \
                (f'Annotated[Optional["{field_type}"], Field({{"required": False,\n'
                 f'             "relation_type": "ZeroOrOne",\n'
                 f'             "reverse_name": "{attribute.reverse}"}})]') if isinstance(attribute, Optional) and field_type in db.entities else field_type

            # print(field_type)
            if field_type in db.entities:
                field_type = f'"{field_type}"'
                # print(field_type)
            fields[attr] = field_type
        elif isinstance(attribute, Set):

            related_entity = attribute.py_type.__name__
            # print(related_entity, str(attribute.reverse).split(".")[1].lower() == str(attribute).split(".")[0].lower()+'s')
            fields[attr] = f'List["{related_entity}"]'
            fields[attr] = f'Annotated[List["{related_entity}"], Field({{"required": False,\n' \
                           f'        "relation_type": "{"ManyToMany" if str(attribute.reverse).split(".")[1].lower() == str(attribute).split(".")[0].lower()+"s" else "OneToMany"}",\n' \
                           f'        "reverse_name": "{attribute.reverse}"}})]'
    # print(fields, db.entities)
    return fields


def generate_pydantic_models():
    pydantic_models = ("from pydantic import BaseModel, Field\n"
                       "from typing import List, Optional, Annotated\n"
                       "import datetime\n\n")
    for entity in db.entities.values():
        if not issubclass(entity, Entity):
            continue
        fields = analyze_pony_model(entity)
        model_name = entity.__name__

        # Base Model
        base_model_str = f'\nclass {model_name}(BaseModel):\n'
        for field_name, field_type in fields.items():
            base_model_str += f'    {field_name}: {field_type}\n'
        base_model_str += '    \n    class Config:\n        arbitrary_types_allowed = True\n\n\n'

        # Create Model
        create_model_str = f'class {model_name}Create(BaseModel):\n'
        for field_name, field_type in fields.items():
            if field_name == 'id' or 'List[' in field_type:
                continue  # Skip 'id' field

            # For Create model, all fields are required
            print(field_name, field_type,  db.entities)
            if 'Annotated' in str(field_type):
                if "Optional" in field_type:
                    create_model_str += f'    {field_name}_ID_: Optional[int] = None\n'
                else:
                    create_model_str += f'    {field_name}_ID_: int\n'
            else:
                # Correct handling of Optional fields
                is_optional = "Optional" in field_type
                corrected_field_type = field_type if is_optional else f'Optional["{field_type}"]'
                create_model_str += f'    {field_name}: {corrected_field_type} = None\n' if is_optional else f'    {field_name}: {field_type}\n'

        # Update Model
        update_model_str = f'\n\nclass {model_name}Update(BaseModel):\n'
        for field_name, field_type in fields.items():
            # For Update model, all fields are optional
            # corrected_field_type = field_type.replace('List[', 'Optional[List[').replace(']', ']]', 1) if 'List[' in field_type else f'Optional[{field_type}]'
            # corrected_field_type = field_type.replace('List[', 'Optional[List[').replace('"]', '"]]', 1) if 'List[' in field_type else f'Optional[{field_type}]'
            # corrected_field_type = corrected_field_type.replace('Optional[Optional[', 'Optional[').replace(']]', ']').replace('})]', '})]]') if not 'List[' in field_type else corrected_field_type
            # update_model_str += f'    {field_name}: {corrected_field_type} = None\n'
            if 'Annotated' in str(field_type):
                if 'List' in field_type:
                    update_model_str += f'    {field_name}_ID_: Optional[List[int]] = []\n'
                    continue
                if "Optional" in field_type:
                    update_model_str += f'    {field_name}_ID_: Optional[int] = None\n'
                else:
                    update_model_str += f'    {field_name}_ID_: Optional[int] = None\n'
            else:
                # Correct handling of Optional fields
                is_optional = "Optional" in field_type
                corrected_field_type = field_type if is_optional else f'Optional["{field_type}"]'
                update_model_str += f'    {field_name}: {corrected_field_type} = None\n'


        # Generate ModelNameOut models
        out_model_str = f'\n\nclass {model_name}Out(BaseModel):\n'
        for field_name, field_type in fields.items():
            if 'List[' in field_type:
                # For related entities, output only their IDs in a list
                out_model_str += f'    {field_name}: Optional[List[any]] = []\n'
                continue
            if field_name.capitalize() in db.entities:
                if "Optional" in field_type:
                    out_model_str += f'    {field_name}: Optional[int] = None\n'
                else:
                    out_model_str += f'    {field_name}: int\n'
            else:
                # For regular fields, output them as they are
                out_model_str += f'    {field_name}: {field_type}\n'
        out_model_str += '    \n    class Config:\n        arbitrary_types_allowed = True\n'


        pydantic_models += base_model_str + create_model_str + update_model_str + out_model_str + '\n'

    return pydantic_models



def write_pydantic_models_to_file(file_path=None):
    models = generate_pydantic_models()
    print(models)
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'pydantic_models.py')
    with io.open(file_path, 'w', encoding='utf-8') as file:
        file.write(models)


if __name__ == '__main__':
    write_pydantic_models_to_file('pydantic_models.py')

