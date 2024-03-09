from collections import UserDict
from datetime import datetime as dtdt

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError
        self.value=value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strftime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError
        
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        ph = Phone(phone)
        self.phones.append(ph)
        return ph

    def add_birthday(self, birthday:str):
        self.birthday = Birthday(birthday)

    def get_upcoming_birthdays(self):
        return []

    def find_phone(self, phone:str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def remove_phone(self, phone):
        ph = self.find_phone(phone)
        if ph:
            self.phones.remove(ph)
        else:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        old_ph = self.find_phone(old_phone)
        if old_ph:
            if not (new_phone.isdigit() and len(new_phone) == 10):
                raise ValueError("Invalid new phone number")
            old_ph.value = new_phone
        else:
            raise ValueError("Phone not found")
    
    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthday"

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record
        return record

    def delete(self, name:str):
        if self.find(name):
            del self.data[name]

    def find(self, name:str):
        return self.data.get(name)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Index out of range."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name, phone)
        book.add_record(record)
        message = "Contact added."

    return message

@input_error
def change_contact(args, book):
    name, phone,new_phone = args
    record = book.find(name)

    if record:
        record.remove_phone(record.phones[0].value)
        record.add_phone(new_phone)
        return "Контакт змінено."
    else:
        return "Контакт не знайдено."

@input_error
def show_all(args, book):
    for record in book.values():
        phones_str = '; '.join(str(p) for p in record.phones) if record.phones else 'Немає номера телефону'
        birthday_str = str(record.birthday) if record.birthday else 'Немає дня народження'
        print(f"Contact name: {record.name:10}, phones: {phones_str:10}, birthday: {birthday_str:10}")

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return "День народження додано."
    else:
        return "Контакт не знайдено."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if record and record.birthday:
        return f"{record.name}'s birthday: {record.birthday}"
    else:
        return "День народження не знайдено."

@input_error
def birthdays(args, book):
    upcoming_birthdays = []
    for record in book.values():
        if record.birthday:
            upcoming_birthdays.append(f"{record.name}: {record.birthday}")
    return "\n".join(upcoming_birthdays) if upcoming_birthdays else "Немає днів народження."

@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "show":
                print(book.find(args[0]).phones[0] if book.find(args[0]) else "Contact not found.")
            elif command == "all":
                print(show_all(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
