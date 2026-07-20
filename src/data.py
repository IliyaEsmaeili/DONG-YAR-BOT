from __future__ import annotations
import telebot.types
from enum import Enum

class UserState(Enum):
    STAGE_BEGIN = "stage_begin"
    STAGE_NAME = "stage_name"
    STAGE_AMOUNT = "stage_amount"
    STAGE_PARTICIPANTS = "stage_participants"
    STAGE_ADDITIONAL_INFO = "stage_additional_info"
    STAGE_CONFIRM = "stage_confirm"

class Dong :
    local_dong_id : str
    name : str
    amount : int
    participants : list
    additional_info : str
    big_prompt_message : telebot.types.Message
    group_id : int
    creator : User
    def __init__(self, dong_id = None, name = None, amount = None, participants =None, additional_info = None, big_prompt_message = None, group_id = None , creator=None ):
        super().__init__()
        self.local_dong_id = dong_id
        self.name = name
        self.amount = amount
        self.participants = participants
        self.additional_info = additional_info
        self.big_prompt_message = big_prompt_message
        self.group_id = group_id
        self.creator = creator

    def __repr__(self):
        return f"Dong(id={self.local_dong_id}, creator = {self.creator} , name={self.name}, amount={self.amount}, participants={self.participants}, additional_info={self.additional_info})"


class User :
    telegram_id : int
    full_name : str
    dong : list[Dong]
    state : UserState
    def __init__(self , messanger_id = None , dong = None , full_name = None , state = UserState.STAGE_BEGIN) :
        super().__init__()
        self.telegram_id = messanger_id
        self.dong = dong
        self.full_name = full_name
        self.state = state

    def __repr__(self):
        return f"User(telegram_id={self.telegram_id},full name = {self.full_name} ,current_state = {self.state} ,  dongs={self.dong})"



user_list = []
