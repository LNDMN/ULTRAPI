import os
import io
from pony.orm.core import Entity, Set
import pony_models as p  # Import Pony ORM models with an alias
import pydantic_models as pm  # Import Pydantic models with an alias
from datetime import date, datetime


def analyze_entity_relationships(entity):
    """Analyzes relationships in a Pony ORM entity and returns a list of relationships with the names of related entities."""
    relationships = []
    for attr in dir(entity):
        attribute = getattr(entity, attr)
        if isinstance(attribute, Set):
            related_entity = attribute.py_type.__name__
            relationships.append((attr, related_entity))
    return relationships


def generate_relationship_functions(entity, relationships):
    """
    Generates functions for retrieving data of related entities.
    """
    relationship_functions = ""
    for rel_attr, related_entity in relationships:
        # Generating a function to retrieve related data
        relationship_functions += f"""\n
async def get_{entity.__name__.lower()}_{rel_attr}(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.{entity.__name__}.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.{entity.__name__}, '{rel_attr}').py_type if e in getattr(parent, '{rel_attr}')).limit(limit, offset=skip)[:]
        return [pm.{related_entity}(**e.to_dict()) for e in related_data]
"""
    return relationship_functions


def generate_crud_functions(folder_path: str = 'app'):
    """Generates CRUD functions for each entity in Pony ORM models."""
    crud_operations = "from pony.orm import db_session, select, desc\n"
    crud_operations += f"import {folder_path+'.' if folder_path else ''}pony_models as p\n"  # Import Pony ORM models with an alias
    crud_operations += f"import {folder_path+'.' if folder_path else ''}pydantic_models as pm\n"  # Import Pydantic models with an alias
    crud_operations += "from datetime import date, datetime\n"

    for entity in p.db.entities.values():
        if not issubclass(entity, Entity):
            continue

        entity_name = entity.__name__
        pydantic_model = f'pm.{entity_name}'

        # Creation
        crud_operations += f"""

async def create_{entity_name.lower()}(item_data: {pydantic_model}Create):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {{}}
        for field, value in item_data_dict.items():
            if field.endswith('_ID_') and value is not None:
                # Получаем имя атрибута без '_ID_'
                attr_name = field[:-4]
                # Получаем класс связанной модели ORM на основе имени поля
                
                related_orm_model = getattr(p, attr_name.capitalize())
                # Получаем объект связанной модели по ID
                if related_orm_model:
                    related_object = related_orm_model.get(id=value)
                if related_object:
                    prepared_data[attr_name] = related_object
            else:
                prepared_data[field] = value
        item = p.{entity_name}(**prepared_data)
        return pm.{entity_name}Out(**item.to_dict())

"""

        # Read with advanced filtering
        crud_operations += f"""
async def get_{entity_name.lower()}s(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.{entity_name}.select()
        if isinstance(filters, dict):
            for field, criteria in filters.items():
                if isinstance(criteria, dict):
                    # Handling complex criteria
                    if 'range' in criteria:
                        min_val, max_val = criteria['range']
                        query = query.filter(lambda e: min_val <= getattr(e, field, 0) <= max_val)
                    if 'contains' in criteria:
                        query = query.filter(lambda e: criteria['contains'] in getattr(e, field, ''))
                    if 'date_range' in criteria:
                        start_date, end_date = criteria['date_range']
                        query = query.filter(lambda e: start_date <= getattr(e, field, date.min) <= end_date)
                else:
                    # Handling simple criteria
                    query = query.filter(lambda e: getattr(e, field, None) == criteria)
        if order_by and hasattr(p.{entity_name}, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.{entity_name}Out(**e.to_dict()) for e in result]

"""

        # Update
        crud_operations += f"""
async def update_{entity_name.lower()}(item_id: int, item_data: {pydantic_model}Update):
    with db_session:
        item = p.{entity_name}.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {{}}
        for field, value in item_data_dict.items():
            if field.endswith('_ID_') and value is not None:
                # Получаем имя атрибута без '_ID_'
                attr_name = field[:-4]
                # Получаем класс связанной модели ORM на основе имени поля
                related_orm_model = getattr(p, attr_name.capitalize())
                # Получаем объект связанной модели по ID
                if related_orm_model:
                    related_object = related_orm_model.get(id=value)
                if related_object:
                    prepared_data[attr_name] = related_object
            else:
                prepared_data[field] = value
        item.set(**prepared_data)
        return pm.{entity_name}Out(**item.to_dict())

"""

        # Delete
        crud_operations += f"""
async def delete_{entity_name.lower()}(item_id: int):
    with db_session:
        item = p.{entity_name}.get(id=item_id)
        if item:
            item.delete()
            return True
        return False
"""
        relationships = analyze_entity_relationships(entity)
        crud_operations += generate_relationship_functions(entity, relationships)

    return crud_operations


# Function to write CRUD operations to a file
def write_crud_to_file(file_path: str, folder_path: str = 'app'):
    """Writes generated CRUD operations to a file."""
    crud_code = generate_crud_functions(folder_path)
    with io.open(file_path, 'w', encoding='utf-8') as file:
        file.write(crud_code)


# Path to the crud.py file
crud_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crud.py')

if __name__ == '__main__':
    write_crud_to_file(crud_file_path)
