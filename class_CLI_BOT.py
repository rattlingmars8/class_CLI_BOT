from collections import UserDict
import re


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
        def __init__(self, value):
            self.value = normal_phone(value)

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            self._value = normal_phone(value)

    

class Record():
    def __init__(self, name:Name, phone:Phone = None):
        self.name = name 
        self.phones = [phone] if phone else []
    
    def add_phone(self, other_phone:Phone):
            self.phones.append(other_phone)

    def del_phone(self, phone:Phone):
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                return self.phones.pop(i)
            
    def change_phone(self, old_phone:Phone, new_phone:Phone):
        if self.del_phone(old_phone):
            self.add_phone(new_phone)

    def __repr__(self) -> str:
      return f'{self.phones}'
        
        
class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record.phones


contacts = AddressBook()

# Decorator function for common input errors
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(
                *args, **kwargs
            )  # Call the decorated function with the given arguments
        except KeyError:
            return "This contact doesn't exist in the phonebook"
        except ValueError:
            return "Please enter name and correct phone number separated by a space"
        except IndexError:
            return "Please enter name and correct phone number separated by a space"

    return wrapper


@input_error
def hello(*args):
    return "How can I help you?"

# fnc to add a new contact to the phonebook
@input_error
def add_contact(*args, **kwargs):
    name = Name(args[0])
    if name.value in contacts.keys():
        return "This contact already exists"
    else:
        try:
            phone = Phone(args[1])
        except IndexError:
            phone = None
        record = Record(name, phone)
        contacts.add_record(record)
        return f"{name} with {phone} has been added to the phonebook"

#fnc to append phone number to phones of some contact/////command should looks like: append phone (name) (new phone)  
@input_error
def append_phone(*args):
    name = args[0]
    phone = args[1]
    if name not in contacts:
        return "This contact doesn't exist in the phonebook"
    else:
        record = Record(Name(name), Phone(phone))
        contacts[name].append(record.phones[0])
        return f"{phone} has been added to {name}'s phones"

#fnc to change contact phone num by typing old phone num 
@input_error
def change_contact(*args, **kwargs):
    name = Name(args[0])
    if name.value in contacts.keys():
        old_phone = Phone(args[1])
        if old_phone.value in [phone.value for phone in contacts[name.value]]:
            new_phone = Phone(args[2])
            record = Record(name, old_phone)
            for i, phone in enumerate(contacts[name.value]):
                if phone.value == old_phone.value:
                    contacts[name.value][i] = new_phone
                    record.change_phone(old_phone, new_phone)
                    return f"The phone number for {name} has been updated to {new_phone}"
    else:
        return "This contact doesn't exist"

# fnc to find the phone number of a given contact
# @input_error
# def find_phone(*args, **kwargs):
#     name = args[0]
#     return f"The phone number for {name} is {contacts[name]}"


# fnc to show all contacts and their phone numbers
@input_error
def show_all(*args, **kwargs):
    output = ""
    for name, phone in contacts.items():
        output += f"{name}: {phone}\n"
    return output


COMMANDS = {
    hello: 'hello',
    show_all: "show all",
    add_contact: "add",
    change_contact: "change",
    # find_phone: "phone",
    append_phone: 'append phone'
}


# fnc to keep only needed part of the command
def remove_unnecessary_text(text):
    regex_pattern = "|".join(map(re.escape, COMMANDS.values()))
    match = re.search(regex_pattern, text.lower())
    if not match:
        return text
    start_index = match.start()
    return text[start_index:]


def command_handler(user_input: str):
    for command, command_words in COMMANDS.items():
        if user_input.lower().startswith(command_words):
            return command, user_input[len(command_words):].strip().split(" ")
    return None, None


def main():
    while True:
        user_input = input("Enter a command: ")
        cmd = remove_unnecessary_text(user_input)
        command, data = command_handler(cmd)
        # print(data)
        if command:
            print(command(*data))
        elif any(word in user_input.lower() for word in ['exit', 'close', 'good bye', 'goodbye']):
            print('Good bye!')
            break
        else:
            print('Command is not supported. Try again.')


if __name__ == "__main__":
    main()
