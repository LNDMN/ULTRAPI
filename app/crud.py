from pony.orm import db_session, select, desc
import app.pony_models as p
import app.pydantic_models as pm
from datetime import date, datetime


async def create_user(item_data: pm.UserCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.User(**prepared_data)
        return pm.UserOut(**item.to_dict())


async def get_users(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.User.select()
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
        if order_by and hasattr(p.User, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.UserOut(**e.to_dict()) for e in result]


async def update_user(item_id: int, item_data: pm.UserUpdate):
    with db_session:
        item = p.User.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.UserOut(**item.to_dict())


async def delete_user(item_id: int):
    with db_session:
        item = p.User.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_user_bots(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.User.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.User, 'bots').py_type if e in getattr(parent, 'bots')).limit(limit, offset=skip)[:]
        return [pm.Bot(**e.to_dict()) for e in related_data]


async def get_user_channels(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.User.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.User, 'channels').py_type if e in getattr(parent, 'channels')).limit(limit, offset=skip)[:]
        return [pm.Channel(**e.to_dict()) for e in related_data]


async def get_user_chats(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.User.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.User, 'chats').py_type if e in getattr(parent, 'chats')).limit(limit, offset=skip)[:]
        return [pm.Chat(**e.to_dict()) for e in related_data]


async def get_user_messages(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.User.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.User, 'messages').py_type if e in getattr(parent, 'messages')).limit(limit, offset=skip)[:]
        return [pm.Message(**e.to_dict()) for e in related_data]


async def get_user_wallet(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.User.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.User, 'wallet').py_type if e in getattr(parent, 'wallet')).limit(limit, offset=skip)[:]
        return [pm.Wallet(**e.to_dict()) for e in related_data]


async def create_bot(item_data: pm.BotCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Bot(**prepared_data)
        return pm.BotOut(**item.to_dict())


async def get_bots(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Bot.select()
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
        if order_by and hasattr(p.Bot, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.BotOut(**e.to_dict()) for e in result]


async def update_bot(item_id: int, item_data: pm.BotUpdate):
    with db_session:
        item = p.Bot.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.BotOut(**item.to_dict())


async def delete_bot(item_id: int):
    with db_session:
        item = p.Bot.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_bot_messages(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Bot.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Bot, 'messages').py_type if e in getattr(parent, 'messages')).limit(limit, offset=skip)[:]
        return [pm.Message(**e.to_dict()) for e in related_data]


async def get_bot_users(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Bot.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Bot, 'users').py_type if e in getattr(parent, 'users')).limit(limit, offset=skip)[:]
        return [pm.User(**e.to_dict()) for e in related_data]


async def create_channel(item_data: pm.ChannelCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Channel(**prepared_data)
        return pm.ChannelOut(**item.to_dict())


async def get_channels(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Channel.select()
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
        if order_by and hasattr(p.Channel, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.ChannelOut(**e.to_dict()) for e in result]


async def update_channel(item_id: int, item_data: pm.ChannelUpdate):
    with db_session:
        item = p.Channel.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.ChannelOut(**item.to_dict())


async def delete_channel(item_id: int):
    with db_session:
        item = p.Channel.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_channel_users(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Channel.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Channel, 'users').py_type if e in getattr(parent, 'users')).limit(limit, offset=skip)[:]
        return [pm.User(**e.to_dict()) for e in related_data]


async def create_partnership(item_data: pm.PartnershipCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Partnership(**prepared_data)
        return pm.PartnershipOut(**item.to_dict())


async def get_partnerships(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Partnership.select()
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
        if order_by and hasattr(p.Partnership, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.PartnershipOut(**e.to_dict()) for e in result]


async def update_partnership(item_id: int, item_data: pm.PartnershipUpdate):
    with db_session:
        item = p.Partnership.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.PartnershipOut(**item.to_dict())


async def delete_partnership(item_id: int):
    with db_session:
        item = p.Partnership.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_partnership_referrals(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Partnership.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Partnership, 'referrals').py_type if e in getattr(parent, 'referrals')).limit(limit, offset=skip)[:]
        return [pm.User(**e.to_dict()) for e in related_data]


async def create_wallet(item_data: pm.WalletCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Wallet(**prepared_data)
        return pm.WalletOut(**item.to_dict())


async def get_wallets(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Wallet.select()
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
        if order_by and hasattr(p.Wallet, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.WalletOut(**e.to_dict()) for e in result]


async def update_wallet(item_id: int, item_data: pm.WalletUpdate):
    with db_session:
        item = p.Wallet.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.WalletOut(**item.to_dict())


async def delete_wallet(item_id: int):
    with db_session:
        item = p.Wallet.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def create_investment(item_data: pm.InvestmentCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Investment(**prepared_data)
        return pm.InvestmentOut(**item.to_dict())


async def get_investments(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Investment.select()
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
        if order_by and hasattr(p.Investment, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.InvestmentOut(**e.to_dict()) for e in result]


async def update_investment(item_id: int, item_data: pm.InvestmentUpdate):
    with db_session:
        item = p.Investment.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.InvestmentOut(**item.to_dict())


async def delete_investment(item_id: int):
    with db_session:
        item = p.Investment.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def create_investmentfund(item_data: pm.InvestmentFundCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.InvestmentFund(**prepared_data)
        return pm.InvestmentFundOut(**item.to_dict())


async def get_investmentfunds(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.InvestmentFund.select()
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
        if order_by and hasattr(p.InvestmentFund, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.InvestmentFundOut(**e.to_dict()) for e in result]


async def update_investmentfund(item_id: int, item_data: pm.InvestmentFundUpdate):
    with db_session:
        item = p.InvestmentFund.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.InvestmentFundOut(**item.to_dict())


async def delete_investmentfund(item_id: int):
    with db_session:
        item = p.InvestmentFund.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_investmentfund_investments(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.InvestmentFund.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.InvestmentFund, 'investments').py_type if e in getattr(parent, 'investments')).limit(limit, offset=skip)[:]
        return [pm.Investment(**e.to_dict()) for e in related_data]


async def create_message(item_data: pm.MessageCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Message(**prepared_data)
        return pm.MessageOut(**item.to_dict())


async def get_messages(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Message.select()
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
        if order_by and hasattr(p.Message, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.MessageOut(**e.to_dict()) for e in result]


async def update_message(item_id: int, item_data: pm.MessageUpdate):
    with db_session:
        item = p.Message.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.MessageOut(**item.to_dict())


async def delete_message(item_id: int):
    with db_session:
        item = p.Message.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def create_chat(item_data: pm.ChatCreate):
    with db_session:
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        item = p.Chat(**prepared_data)
        return pm.ChatOut(**item.to_dict())


async def get_chats(filters: dict = None, order_by: str = None, desc_order: bool = False, skip: int = 0, limit: int = 10):
    with db_session:
        query = p.Chat.select()
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
        if order_by and hasattr(p.Chat, order_by):
            query = query.order_by(lambda e: desc(getattr(e, order_by)) if desc_order else getattr(e, order_by))
        result = query.limit(limit, offset=skip)
        return [pm.ChatOut(**e.to_dict()) for e in result]


async def update_chat(item_id: int, item_data: pm.ChatUpdate):
    with db_session:
        item = p.Chat.get(id=item_id)
        if item is None:
            return None
        # Prepare data for update
        item_data_dict = item_data.model_dump(exclude_unset=True)
        prepared_data = {}
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
        return pm.ChatOut(**item.to_dict())


async def delete_chat(item_id: int):
    with db_session:
        item = p.Chat.get(id=item_id)
        if item:
            item.delete()
            return True
        return False


async def get_chat_messages(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Chat.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Chat, 'messages').py_type if e in getattr(parent, 'messages')).limit(limit, offset=skip)[:]
        return [pm.Message(**e.to_dict()) for e in related_data]


async def get_chat_users(parent_id: int, skip: int = 0, limit: int = 10):
    with db_session:
        parent = p.Chat.get(id=parent_id)
        if not parent:
            return []
        related_data = select(e for e in getattr(p.Chat, 'users').py_type if e in getattr(parent, 'users')).limit(limit, offset=skip)[:]
        return [pm.User(**e.to_dict()) for e in related_data]
