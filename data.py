import telebot.types


class Dong :
    id : str
    name : str
    amount : int
    participants : list
    additional_info : str
    big_prompt_message : telebot.types.Message
    group_id : int
    def __init__(self, dong_id = None, name = None, amount = None, participants =None, additional_info = None, big_prompt_message = None, group_id = None):
        super().__init__()
        self.id = dong_id
        self.name = name
        self.amount = amount
        self.participants = participants
        self.additional_info = additional_info
        self.big_prompt_message = big_prompt_message
        self.group_id = group_id

    def __repr__(self):
        return f"Dong(id={self.id}, name={self.name}, amount={self.amount}, participants={self.participants}, additional_info={self.additional_info})"


class User :
    messanger_id : int
    dong : Dong
    def __init__(self , messanger_id = None , dong = None):
        super().__init__()
        self.messanger_id = messanger_id
        self.dong = dong

    def __repr__(self):
        return f"User(messanger_id={self.messanger_id}, dong={self.dong})"



user_list = []
