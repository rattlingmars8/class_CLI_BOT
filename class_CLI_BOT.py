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
    def __init__(self, value=""):
        self.set_value(value)

    def normal_phone(self, phone: str):
        digits = [char for char in phone if char.isdigit()]
        if len(digits) == 10 and digits[0] == "0":
            return "+38" + "".join(digits)
        elif len(digits) == 12 and digits[:3] == ["3", "8", "0"]:
            return "+" + "".join(digits)
        elif len(digits) == 12 and phone[0] == "+" and digits[:3] == ["3", "8", "0"]:
            return "+" + "".join(digits)
        else:
            raise ValueError("Invalid phone number")

    def set_value(self, phone):
        self.value = self.normal_phone(phone)

class Record():
    def __init__(self, name:Name, phone:Phone=None):
        self.name = name
        self.phones = [phone] if phone else []

    def add_phone(self, phone:Phone):
        self.phones.append(phone)

    def remove_phone(self, index: int):
        self.phones.pop(index)

    def change_phone(self, index: int, new_phone:Phone):
        self.phones[index] = new_phone

    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
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
    if name.value.strip() == "":
        return "Try again. Enter contact name you want to add."
    if name.value in contacts.keys():
        return "This contact already exists."
    else:
        if len(args) > 1:
            phone = Phone(args[1])
            record = Record(name, phone)
            contacts.add_record(record)
            return f"{name.value} with {phone.value} has been added to the phonebook."
        else:
            record = Record(name)
            contacts.add_record(record)
            return f"{name.value} has been added to the phonebook." 

@input_error
def show_all(*args):
    all_contacts = ""
    for _, record in contacts.items():
        all_contacts += f'{record}\n'
    return all_contacts
 

@input_error
def change_phone(*args):
    name = args[0]
    if name == "":
        return "Try again. Enter contact name for whom change phone number."
    if name not in contacts.keys():
        return f'Contact ({name}) is not in phonebook.'
    else:
        record = contacts.get(name)
        if len(record.phones) == 0:
            return f"Contact ({name}) haven't any phone yet."
        print(f'{name} phone numbers:')
        for i, number in enumerate([phone.value for phone in record.phones], 0):
            print(f'{i+1}. {number}\n')
        while True:
            try:
                pos_input = input('Enter the position of a phone you want to edit: ')
                if pos_input.lower() in ['exit', 'end', 'stop']:
                    return 'Exiting change_phone...'
                pos = int(pos_input) - 1
                if pos > len(record.phones)-1 or pos < 0:
                    raise IndexError
            except IndexError:
                print('Wrong index. Please try again.')
                continue
            except ValueError:
                print('Please enter a valid integer index.')
                continue
            while True:
                phone_input = input(f'Enter new phone number for contact - {name}: ')
                if phone_input.lower() in ['exit', 'end']:
                    return 'Exiting change_phone...'
                try:
                    new_phone = Phone(phone_input)
                except ValueError:
                    print('Please enter a valid phone number. Recommended format: "+380123456789" or "0123456879".')
                else:
                    break
            record.change_phone(pos, new_phone)
            return f"{name}'s phone {number} was changed to {new_phone}."

@input_error        
def append_phone(*args):
    name = args[0]
    if name == "":
        return "Try again. Enter contact name you want to add."
    if name not in contacts.keys():
        return f'Contact ({name}) is not in phonebook.'
    else:
        if len(args) > 1:
            new_phone = Phone(args[1])
            record = contacts.get(name)
            for phone in record.phones:
                if phone.value == new_phone.value:
                    return f"{new_phone.value} is already in {name}'s phones. Try again."
            else:
                record.add_phone(new_phone)
                return f"To {name}'s phones was add {new_phone.value}."
        else:
            return f"Enter the phone you want to add for {name}. Try again."

@input_error
def remove_phone(*args):
    name = args[0]
    if name == "":
        return "Try again. Enter contact name for whom you want to delete phone number."
    if name not in contacts.keys():
        return f'Contact ({name}) is not in phonebook.'
    else:
        record = contacts.get(name)
        if len(record.phones) == 0:
            return f"For contact ({name}) there's nothing to remove."
        print(f'{name} phone numbers:')
        for i, number in enumerate([phone.value for phone in record.phones], 0):
            print(f'{i+1}. {number}')
        while True:
            try:
                pos_input = input('Enter the position of a phone you want to remove: ')
                if pos_input.lower() in ['exit', 'end', 'stop']:
                    return 'Exiting del_phone...'
                pos = int(pos_input) - 1
                if pos > len(record.phones)-1 or pos < 0:
                    raise IndexError
            except IndexError:
                print('Wrong index. Please try again.')
                continue
            except ValueError:
                print('Please enter a valid integer index.')
                continue

            record.remove_phone(pos)
            return f"{name}'s phone {number} was deleted."

@input_error       
def contact_remove(*args):
    name = args[0]
    if name == "":
        return "Try again. Enter contact name you want to delete."
    if name not in contacts.keys():
        return f'Contact ({name}) is not in phonebook.'
    else:
        del contacts.data[name]
        return f"Contact {name} was deleted from phonebook."

@input_error  
def show_cont_phones(*args):
    name = args[0]
    if name == "":
        return "Try again. Enter contact name."
    if name not in contacts.keys():
        return f'Contact ({name}) is not in phonebook.'
    else:
        record = contacts.get(name)
        if len(record.phones) == 0:
            return f"For contact ({name}) there's no any phone."
        print(f'{name} phone numbers:')
        for i, number in enumerate([phone.value for phone in record.phones], 0):
            return(f'{i+1}. {number}')

COMMANDS = {
    hello: 'hello',
    show_all: "show all",
    add_contact: "add",
    change_phone: "change phone",
    append_phone: "append phone",
    remove_phone: "remove phone",
    contact_remove: "del contact", 
    show_cont_phones: "show phones"
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