class Dong :
    id : int
    name : str
    amount : int
    participants : list
    additional_info : str
    def __init__(self, id = None, name = None, amount = None, participants =None, additional_info = None):
        super().__init__()
        self.id = id
        self.name = name
        self.amount = amount
        self.participants = participants
        self.additional_info = additional_info

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
