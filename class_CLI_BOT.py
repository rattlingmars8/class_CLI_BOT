from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._value = self.normal_phone(value)

    def normal_phone(self, phone: str):
        digits = [char for char in phone if char.isdigit()]
        if len(digits) == 10:
            return "+38" + "".join(digits)
        elif len(digits) == 12 and digits[:3] == ["3", "8", "0"]:
            return "+" + "".join(digits)
        elif len(digits) == 12 and phone[0] == "+" and digits[:3] == ["3", "8", "0"]:
            return "+" + "".join(digits)
        else:
            raise ValueError("Invalid phone number")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.normal_phone(value)

    def __str__(self):
        return self._value

class Record():
    def __init__(self, name:Name, phone:Phone=None):
        self.name = name
        self.phones = [phone] if phone else []

    def add_phone(self, phone:Phone):
        self.phones.append(phone)

    def remove_phone(self, phone:Phone):
        self.phones.remove(phone)

    def change_phone(self, index: int, new_phone:Phone):
        self.phones[index] = new_phone

    def __str__(self):
        phones = "\n".join([str(phone) for phone in self.phones])
        return f"{self.name}: {phones}"
    

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record
    
# name = Name("Vladik")
# phone = Phone('0930030322')
# rec = Record(name, phone)
# ab = AddressBook()
# ab.add_record(rec)
# print(ab)    



contacts = AddressBook()

# Decorator function for common input errors
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Call the decorated function with the given arguments
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
def add_contact(*args):
    name = Name(args[0])
    if name.value in contacts.keys():
        return "This user already exists."
    else:
        try:
            phone = Phone(args[1])
        except IndexError:
            phone = ""
        record = Record(name, phone)
        contacts.add_record(record)
        if phone:
            return f"{name} with {phone} has been added to the phonebook"
        return f"{name} has been added to the phonebook"

@input_error
def show_all(*args):
    all_contacts = ""
    for name, record in contacts.items():
        all_contacts += f'{record}\n'
    return all_contacts

@input_error
def change_phone(*args):
    record = contacts.get(args[0])
    for i, number in enumerate([phone.value for phone in record.phones], 0):
            print(f'{i}: {number}')
    while True:
        try:
            pos = int(input('Enter the index of a phone you want to edit >>> '))
            if pos > len(record.phones)-1:
                raise IndexError
        except IndexError:
            print('Wrong index. Please try again.')
        except ValueError:
            print('Please enter a valid integer index.')
        else:
            user_input = input('Enter new phone num for this contact >>>> ')
            try:
                new_phone = Phone(user_input)
            except ValueError:
                print('Please enter a valid phone number.')
            else:
                record.change_phone(pos, new_phone)
                return f"Phone was changed to {new_phone}."



    


COMMANDS = {
    hello: 'hello',
    show_all: "show all",
    add_contact: "add",
    change_phone: "change phone", 
    # find_phone: "phone",
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
