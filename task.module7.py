from datetime import datetime as dtdt, timedelta as td

class Birthday:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def validate_phone(self, phone):
        pass

    def add_birthday(self, birthday):
        try:
            dtdt.strptime(birthday, '%Y-%m-%d')
            self.birthday = birthday
        except ValueError:
            print('Incorrect format')

    def validate_birthday(self, birthday):
        try:
            dtdt.strptime(birthday, '%Y-%m-%d')
            self.birthday = birthday
            return True
        except ValueError:
            return False

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        next_week = dtdt.now() + td(days=7)
        upcoming_birthdays = []

        for record in self.records:
            if record.birthday is not None:
                birthday_date = dtdt.strptime(record.birthday, "%Y-%m-%d").date()
                days_until_birthday = (birthday_date - dtdt.now().date()).days
                if 0 <= days_until_birthday <= 7:
                    upcoming_birthdays.append((record.name, birthday_date))

        return upcoming_birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
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
    name, new_phone = args
    record = book.find(name)

    if record:
        record.phone = new_phone
        return "Contact changed."
    else:
        return "Contact not found."

@input_error
def show_all(args, book):
    for record in book.records:
        print(f"{record.name:10} : {record.phone:10}")

@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
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
            print(book.find(args[0]).phone if book.find(args[0]) else "Contact not found.")
        elif command == "all":
            print(show_all(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()