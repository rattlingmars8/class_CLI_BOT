from collections import UserDict


def normal_phone(phone: str):
    digits = [char for char in phone if char.isdigit()]
    if len(digits) == 10:
        return "+38" + "".join(digits)
    elif len(digits) == 12 and digits[:3] == ["3", "8", "0"]:
        return "+" + "".join(digits)
    elif len(digits) == 12 and phone[0] == "+" and digits[:3] == ["3", "8", "0"]:
        return "+" + "".join(digits)
    else:
        raise ValueError("Invalid phone number")



class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value): # Для створення екземпляру цього класу, значення обов'язкове
        value = normal_phone(value) # трохи поспішили) такі перевірки робляться в сеттерах )
        super().__init__(value)

    # def __iter__(self):
    #     return iter(str(self.value))  Навіщо тут iter?
    

class Record():
    def __init__(self, name:Name, phone:Phone = None):
        self.name = name # Екземпляри класів повинні створюватись явно, тому тут помилка
        if phone:
            # self.data = {self.name}
        # else:
        
            self.phones = [phone]
        else:
            self.phones = []
        
            # self.data = {self.name: self.phone}

    # def __repr__(self) -> str:
    #     return f'{self.data}'
    
    def add_phone(self, other_phone: Phone):
        # try: При явному створенні екземпляру Phone ця помилка виникне ще на етапі його створення
        self.phones.append(other_phone) 
        # except ValueError:
        #     return "You've enter an invalid phone number. Try again"
        
    # def del_phone(self, phone):
    #     for p in self.phone:
    #         if p == phone:
    #             self.phone.remove(phone)

    def del_phone(self, phone:Phone):
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                return self.phones.pop(i)
            
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if self.del_phone(old_phone):
            self.add_phone(new_phone)

    def __repr__(self) -> str:
        # try:
            # return ', '.join([p.value for p in self.phone])
            return f'{self.phones}'
        # except AttributeError: phones повинен створитись при створенні екземпляру класу Record 
        #     return ""
        
        
class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        if name in self.data:
            existing_record = self.data[name]
            existing_phones = [phone.value for phone in existing_record.phone]
            for phone in record.phone:
                if phone.value in existing_phones:
                    print(f'Контакт з іменем "{name}" і номером телефону "{phone.value}" вже існує, тому він не був доданий до телефонної книги')
                else:
                    existing_record.add_phone(phone.value)
            # так не годиться працювати з класами - це не відповідальність класу AddressBook 
            # працювати з функціональністю класу Record
        else:
            self.data[name] = record


if __name__ == "__main__":
    book = AddressBook()
    name = Name('Vladik')
    record1 = Record(name, Phone('0731404451'))
    record1.add_phone(Phone('0930030322'))
    book.add_record(record1)
    record1.del_phone(Phone('+380930030322'))
    print(book)
