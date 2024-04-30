

from fastapi import FastAPI, Query, Path, Body
import app.crud as crud
from pydantic_models import *  
# from typing import Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Assuming your templates are stored in a directory named "templates"
templates = Jinja2Templates(directory="templates")


# Mount static files, assuming your Vue.js app's entry point is "admin.html" in the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/admin")
async def get_admin_panel():
    # Redirect or serve your Vue.js admin panel statically
    # This is just a placeholder; serving static files correctly might need adjustments
    return FileResponse('static/admin.html')


@app.post("/bot/")
async def create_bot(item_data: BotCreate = Body(...)):
    return await crud.create_bot(item_data)


@app.post("/channel/")
async def create_channel(item_data: ChannelCreate = Body(...)):
    return await crud.create_channel(item_data)


@app.post("/chat/")
async def create_chat(item_data: ChatCreate = Body(...)):
    return await crud.create_chat(item_data)


@app.post("/investment/")
async def create_investment(item_data: InvestmentCreate = Body(...)):
    return await crud.create_investment(item_data)


@app.post("/investmentfund/")
async def create_investmentfund(item_data: InvestmentFundCreate = Body(...)):
    return await crud.create_investmentfund(item_data)


@app.post("/message/")
async def create_message(item_data: MessageCreate = Body(...)):
    return await crud.create_message(item_data)


@app.post("/partnership/")
async def create_partnership(item_data: PartnershipCreate = Body(...)):
    return await crud.create_partnership(item_data)


@app.post("/user/")
async def create_user(item_data: UserCreate = Body(...)):
    return await crud.create_user(item_data)


@app.post("/wallet/")
async def create_wallet(item_data: WalletCreate = Body(...)):
    return await crud.create_wallet(item_data)


@app.delete("/bot/{item_id}")
async def delete_bot(item_id: int = Path(...)):
    return await crud.delete_bot(item_id)


@app.delete("/channel/{item_id}")
async def delete_channel(item_id: int = Path(...)):
    return await crud.delete_channel(item_id)


@app.delete("/chat/{item_id}")
async def delete_chat(item_id: int = Path(...)):
    return await crud.delete_chat(item_id)


@app.delete("/investment/{item_id}")
async def delete_investment(item_id: int = Path(...)):
    return await crud.delete_investment(item_id)


@app.delete("/investmentfund/{item_id}")
async def delete_investmentfund(item_id: int = Path(...)):
    return await crud.delete_investmentfund(item_id)


@app.delete("/message/{item_id}")
async def delete_message(item_id: int = Path(...)):
    return await crud.delete_message(item_id)


@app.delete("/partnership/{item_id}")
async def delete_partnership(item_id: int = Path(...)):
    return await crud.delete_partnership(item_id)


@app.delete("/user/{item_id}")
async def delete_user(item_id: int = Path(...)):
    return await crud.delete_user(item_id)


@app.delete("/wallet/{item_id}")
async def delete_wallet(item_id: int = Path(...)):
    return await crud.delete_wallet(item_id)


@app.get("/bot_messages/")
async def get_bot_messages(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_bot_messages(parent_id, skip, limit)


@app.get("/bot_users/")
async def get_bot_users(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_bot_users(parent_id, skip, limit)


@app.get("/bots/")
async def get_bots(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_bots(filters, order_by, desc_order, skip, limit)


@app.get("/channel_users/")
async def get_channel_users(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_channel_users(parent_id, skip, limit)


@app.get("/channels/")
async def get_channels(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_channels(filters, order_by, desc_order, skip, limit)


@app.get("/chat_messages/")
async def get_chat_messages(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_chat_messages(parent_id, skip, limit)


@app.get("/chat_users/")
async def get_chat_users(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_chat_users(parent_id, skip, limit)


@app.get("/chats/")
async def get_chats(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_chats(filters, order_by, desc_order, skip, limit)


@app.get("/investmentfund_investments/")
async def get_investmentfund_investments(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_investmentfund_investments(parent_id, skip, limit)


@app.get("/investmentfunds/")
async def get_investmentfunds(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_investmentfunds(filters, order_by, desc_order, skip, limit)


@app.get("/investments/")
async def get_investments(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_investments(filters, order_by, desc_order, skip, limit)


@app.get("/messages/")
async def get_messages(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_messages(filters, order_by, desc_order, skip, limit)


@app.get("/partnership_referrals/")
async def get_partnership_referrals(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_partnership_referrals(parent_id, skip, limit)


@app.get("/partnerships/")
async def get_partnerships(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_partnerships(filters, order_by, desc_order, skip, limit)


@app.get("/user_bots/")
async def get_user_bots(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_user_bots(parent_id, skip, limit)


@app.get("/user_channels/")
async def get_user_channels(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_user_channels(parent_id, skip, limit)


@app.get("/user_chats/")
async def get_user_chats(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_user_chats(parent_id, skip, limit)


@app.get("/user_messages/")
async def get_user_messages(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_user_messages(parent_id, skip, limit)


@app.get("/user_wallet/{item_id}")
async def get_user_wallet(parent_id: int = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_user_wallet(parent_id, skip, limit)


@app.get("/users/")
async def get_users(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_users(filters, order_by, desc_order, skip, limit)


@app.get("/wallets/")
async def get_wallets(filters: dict = Query, order_by: str = Query(None), desc_order: bool = Query(None), skip: int = Query(None), limit: int = Query(None)):
    return await crud.get_wallets(filters, order_by, desc_order, skip, limit)


@app.put("/bot/{item_id}")
async def update_bot(item_id: int = Path(...), item_data: BotUpdate = Body(...)):
    return await crud.update_bot(item_id, item_data)


@app.put("/channel/{item_id}")
async def update_channel(item_id: int = Path(...), item_data: ChannelUpdate = Body(...)):
    return await crud.update_channel(item_id, item_data)


@app.put("/chat/{item_id}")
async def update_chat(item_id: int = Path(...), item_data: ChatUpdate = Body(...)):
    return await crud.update_chat(item_id, item_data)


@app.put("/investment/{item_id}")
async def update_investment(item_id: int = Path(...), item_data: InvestmentUpdate = Body(...)):
    return await crud.update_investment(item_id, item_data)


@app.put("/investmentfund/{item_id}")
async def update_investmentfund(item_id: int = Path(...), item_data: InvestmentFundUpdate = Body(...)):
    return await crud.update_investmentfund(item_id, item_data)


@app.put("/message/{item_id}")
async def update_message(item_id: int = Path(...), item_data: MessageUpdate = Body(...)):
    return await crud.update_message(item_id, item_data)


@app.put("/partnership/{item_id}")
async def update_partnership(item_id: int = Path(...), item_data: PartnershipUpdate = Body(...)):
    return await crud.update_partnership(item_id, item_data)


@app.put("/user/{item_id}")
async def update_user(item_id: int = Path(...), item_data: UserUpdate = Body(...)):
    return await crud.update_user(item_id, item_data)


@app.put("/wallet/{item_id}")
async def update_wallet(item_id: int = Path(...), item_data: WalletUpdate = Body(...)):
    return await crud.update_wallet(item_id, item_data)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', reload=True)
    