from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
import datetime


class User(BaseModel):
    bots: Annotated[List["Bot"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "Bot.users"})]
    channels: Annotated[List["Channel"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "Channel.users"})]
    chats: Annotated[List["Chat"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "Chat.users"})]
    end_of_premium: datetime.datetime
    first_date: datetime.datetime
    id: int
    investment: Annotated[Optional["Investment"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Investment.user"})]
    is_active: bool
    is_premium: bool
    is_referral_of: Annotated[Optional["Partnership"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Partnership.referrals"})]
    last_date: datetime.datetime
    limit_level: int
    messages: Annotated[List["Message"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "Message.user"})]
    nickname: str
    partnerships: Annotated[Optional["Partnership"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Partnership.user"})]
    tokens: int
    user_id: str
    username: str
    wallet: Annotated[List["Wallet"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "Wallet.user"})]
    
    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    end_of_premium: datetime.datetime
    first_date: datetime.datetime
    investment_ID_: Optional[int] = None
    is_active: bool
    is_premium: bool
    is_referral_of_ID_: Optional[int] = None
    last_date: datetime.datetime
    limit_level: int
    nickname: str
    partnerships_ID_: Optional[int] = None
    tokens: int
    user_id: str
    username: str


class UserUpdate(BaseModel):
    bots_ID_: Optional[List[int]] = []
    channels_ID_: Optional[List[int]] = []
    chats_ID_: Optional[List[int]] = []
    end_of_premium: Optional["datetime.datetime"] = None
    first_date: Optional["datetime.datetime"] = None
    id: Optional["int"] = None
    investment_ID_: Optional[int] = None
    is_active: Optional["bool"] = None
    is_premium: Optional["bool"] = None
    is_referral_of_ID_: Optional[int] = None
    last_date: Optional["datetime.datetime"] = None
    limit_level: Optional["int"] = None
    messages_ID_: Optional[List[int]] = []
    nickname: Optional["str"] = None
    partnerships_ID_: Optional[int] = None
    tokens: Optional["int"] = None
    user_id: Optional["str"] = None
    username: Optional["str"] = None
    wallet_ID_: Optional[List[int]] = []


class UserOut(BaseModel):
    bots: Optional[List[any]] = []
    channels: Optional[List[any]] = []
    chats: Optional[List[any]] = []
    end_of_premium: datetime.datetime
    first_date: datetime.datetime
    id: int
    investment: Optional[int] = None
    is_active: bool
    is_premium: bool
    is_referral_of: Annotated[Optional["Partnership"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Partnership.referrals"})]
    last_date: datetime.datetime
    limit_level: int
    messages: Optional[List[any]] = []
    nickname: str
    partnerships: Annotated[Optional["Partnership"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Partnership.user"})]
    tokens: int
    user_id: str
    username: str
    wallet: Optional[List[any]] = []
    
    class Config:
        arbitrary_types_allowed = True


class Bot(BaseModel):
    id: int
    id_of_bot: int
    messages: Annotated[List["Message"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "Message.bot"})]
    name: str
    token: str
    type_of_bot: str
    username: str
    users: Annotated[List["User"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "User.bots"})]
    
    class Config:
        arbitrary_types_allowed = True


class BotCreate(BaseModel):
    id_of_bot: int
    name: str
    token: str
    type_of_bot: str
    username: str


class BotUpdate(BaseModel):
    id: Optional["int"] = None
    id_of_bot: Optional["int"] = None
    messages_ID_: Optional[List[int]] = []
    name: Optional["str"] = None
    token: Optional["str"] = None
    type_of_bot: Optional["str"] = None
    username: Optional["str"] = None
    users_ID_: Optional[List[int]] = []


class BotOut(BaseModel):
    id: int
    id_of_bot: int
    messages: Optional[List[any]] = []
    name: str
    token: str
    type_of_bot: str
    username: str
    users: Optional[List[any]] = []
    
    class Config:
        arbitrary_types_allowed = True


class Channel(BaseModel):
    channel_id: str
    id: int
    name: str
    users: Annotated[List["User"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "User.channels"})]
    
    class Config:
        arbitrary_types_allowed = True


class ChannelCreate(BaseModel):
    channel_id: str
    name: str


class ChannelUpdate(BaseModel):
    channel_id: Optional["str"] = None
    id: Optional["int"] = None
    name: Optional["str"] = None
    users_ID_: Optional[List[int]] = []


class ChannelOut(BaseModel):
    channel_id: str
    id: int
    name: str
    users: Optional[List[any]] = []
    
    class Config:
        arbitrary_types_allowed = True


class Partnership(BaseModel):
    id: int
    referrals: Annotated[List["User"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "User.is_referral_of"})]
    total_earned: str
    total_invested_by_referrals: float
    total_referrals: int
    user: Annotated["User", Field({"required": True,
                "relation_type": "ManyToOne",
                "reverse_name": "User.partnerships"})]
    
    class Config:
        arbitrary_types_allowed = True


class PartnershipCreate(BaseModel):
    total_earned: str
    total_invested_by_referrals: float
    total_referrals: int
    user_ID_: int


class PartnershipUpdate(BaseModel):
    id: Optional["int"] = None
    referrals_ID_: Optional[List[int]] = []
    total_earned: Optional["str"] = None
    total_invested_by_referrals: Optional["float"] = None
    total_referrals: Optional["int"] = None
    user_ID_: Optional[int] = None


class PartnershipOut(BaseModel):
    id: int
    referrals: Optional[List[any]] = []
    total_earned: str
    total_invested_by_referrals: float
    total_referrals: int
    user: int
    
    class Config:
        arbitrary_types_allowed = True


class Wallet(BaseModel):
    addictional_wallet_info: str
    address: str
    balance: float
    currency: str
    id: int
    total_received: int
    total_withdrawn: float
    user: Annotated["User", Field({"required": True,
                "relation_type": "OneToOne",
                "reverse_name": "User.wallet"})]
    
    class Config:
        arbitrary_types_allowed = True


class WalletCreate(BaseModel):
    addictional_wallet_info: str
    address: str
    balance: float
    currency: str
    total_received: int
    total_withdrawn: float
    user_ID_: int


class WalletUpdate(BaseModel):
    addictional_wallet_info: Optional["str"] = None
    address: Optional["str"] = None
    balance: Optional["float"] = None
    currency: Optional["str"] = None
    id: Optional["int"] = None
    total_received: Optional["int"] = None
    total_withdrawn: Optional["float"] = None
    user_ID_: Optional[int] = None


class WalletOut(BaseModel):
    addictional_wallet_info: str
    address: str
    balance: float
    currency: str
    id: int
    total_received: int
    total_withdrawn: float
    user: int
    
    class Config:
        arbitrary_types_allowed = True


class Investment(BaseModel):
    id: int
    investment_fund: Annotated["InvestmentFund", Field({"required": True,
                "relation_type": "ManyToOne",
                "reverse_name": "InvestmentFund.investments"})]
    total_invested: float
    total_profit: float
    user: Annotated["User", Field({"required": True,
                "relation_type": "OneToOne",
                "reverse_name": "User.investment"})]
    
    class Config:
        arbitrary_types_allowed = True


class InvestmentCreate(BaseModel):
    investment_fund_ID_: int
    total_invested: float
    total_profit: float
    user_ID_: int


class InvestmentUpdate(BaseModel):
    id: Optional["int"] = None
    investment_fund_ID_: Optional[int] = None
    total_invested: Optional["float"] = None
    total_profit: Optional["float"] = None
    user_ID_: Optional[int] = None


class InvestmentOut(BaseModel):
    id: int
    investment_fund: Annotated["InvestmentFund", Field({"required": True,
                "relation_type": "ManyToOne",
                "reverse_name": "InvestmentFund.investments"})]
    total_invested: float
    total_profit: float
    user: int
    
    class Config:
        arbitrary_types_allowed = True


class InvestmentFund(BaseModel):
    balance: float
    id: int
    investments: Annotated[List["Investment"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "Investment.investment_fund"})]
    total_invested: float
    total_users_profit: float
    total_withdrawn: float
    
    class Config:
        arbitrary_types_allowed = True


class InvestmentFundCreate(BaseModel):
    balance: float
    total_invested: float
    total_users_profit: float
    total_withdrawn: float


class InvestmentFundUpdate(BaseModel):
    balance: Optional["float"] = None
    id: Optional["int"] = None
    investments_ID_: Optional[List[int]] = []
    total_invested: Optional["float"] = None
    total_users_profit: Optional["float"] = None
    total_withdrawn: Optional["float"] = None


class InvestmentFundOut(BaseModel):
    balance: float
    id: int
    investments: Optional[List[any]] = []
    total_invested: float
    total_users_profit: float
    total_withdrawn: float
    
    class Config:
        arbitrary_types_allowed = True


class Message(BaseModel):
    bot: Annotated[Optional["Bot"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Bot.messages"})]
    chat: Annotated[Optional["Chat"], Field({"required": False,
             "relation_type": "ZeroOrOne",
             "reverse_name": "Chat.messages"})]
    content: str
    content_path: str
    content_type: str
    id: int
    message_id: int
    user: Annotated["User", Field({"required": True,
                "relation_type": "ManyToOne",
                "reverse_name": "User.messages"})]
    
    class Config:
        arbitrary_types_allowed = True


class MessageCreate(BaseModel):
    bot_ID_: Optional[int] = None
    chat_ID_: Optional[int] = None
    content: str
    content_path: str
    content_type: str
    message_id: int
    user_ID_: int


class MessageUpdate(BaseModel):
    bot_ID_: Optional[int] = None
    chat_ID_: Optional[int] = None
    content: Optional["str"] = None
    content_path: Optional["str"] = None
    content_type: Optional["str"] = None
    id: Optional["int"] = None
    message_id: Optional["int"] = None
    user_ID_: Optional[int] = None


class MessageOut(BaseModel):
    bot: Optional[int] = None
    chat: Optional[int] = None
    content: str
    content_path: str
    content_type: str
    id: int
    message_id: int
    user: int
    
    class Config:
        arbitrary_types_allowed = True


class Chat(BaseModel):
    chat_id: str
    id: int
    messages: Annotated[List["Message"], Field({"required": False,
        "relation_type": "OneToMany",
        "reverse_name": "Message.chat"})]
    users: Annotated[List["User"], Field({"required": False,
        "relation_type": "ManyToMany",
        "reverse_name": "User.chats"})]
    
    class Config:
        arbitrary_types_allowed = True


class ChatCreate(BaseModel):
    chat_id: str


class ChatUpdate(BaseModel):
    chat_id: Optional["str"] = None
    id: Optional["int"] = None
    messages_ID_: Optional[List[int]] = []
    users_ID_: Optional[List[int]] = []


class ChatOut(BaseModel):
    chat_id: str
    id: int
    messages: Optional[List[any]] = []
    users: Optional[List[any]] = []
    
    class Config:
        arbitrary_types_allowed = True

