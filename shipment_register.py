import sqlite3
import datetime
import sys

" Database classes "


class Database:
    """Class with all functions and objects from database side"""

    # assigning requirement variables to create database
    db_file = sqlite3.connect("shipment_database.db")
    db_manager = db_file.cursor()

    def __init__(self):
        """Assigning database objects into variables"""
        self.Database = Database.db_file
        self.Manager = Database.db_manager

    def shipments_table_creator(self):
        """Creating database table if not exists"""
        self.Manager.execute(
            "CREATE TABLE IF NOT EXISTS shipments (Title TEXT, Order_number TEXT type UNIQUE, Article TEXT,"
            " Amount INTEGER, Shipping_date TEXT)"
        )

    def save_changes(self):
        """ Saving changes in database"""
        while True:
            select = input("Save changes in database? [Y/N]: ").upper()
            try:
                if select == "Y":
                    # committing changes in database
                    print("Saving changes...")
                    self.Database.commit()
                    break
                elif select == "N":
                    # closing without saving.
                    print("Changes not saved.")
                    break
                else:
                    print("Wrong input! (Yes-> Y/N <- No)")
            except sqlite3.Error:
                print("Saving failure!")
                break

    def insert_statement(self, statement: str):
        """Inserting new data into database."""
        while True:
            try:
                print("Inserting data...")
                # inserting new data by Database.Manager object.
                if self.db_manager.execute(statement):
                    print("Data loaded into database.")
                    break
            # catching Database Error if Manager object received invalid statement.
            except sqlite3.Error:
                print("Inserting data goes wrong.")
                break

    @staticmethod
    def insert_statement_creator() -> str:
        """Create a INSERT INTO SQL statement based on user input data"""

        table_columns = {"Title": '', "Order number": '', "Article": '', "Amount": ''}
        # collecting all data from user by iterating over columns and updating columns values.
        for key, val in table_columns.items():
            while True:
                val = input(f"Input {key}: ").strip()
                if len(val) != 0:
                    table_columns.update({key: val})
                    break
                else:
                    print("Your input is empty. Type again.")
        # creating statement string with for loop and collected user data.
        statement = ""
        for column in table_columns.values():
            statement = statement + f"'{column}', "
        # adding shipping date into statement
        # outer While loop.
        while True:
            select = input("Did shipment arrived today?[Y/N]: ").upper()
            if select == "Y":
                shipping_date = actual_date()
                break
            elif select == "N":
                # inner While loop.
                while True:
                    date = input(f"Input date in format({actual_date()}): ")
                    # expected date format
                    date_format = "%d-%m-%Y"
                    # checking if user input date have expected format.
                    try:
                        shipping_date = datetime.datetime.strptime(date, date_format).date()
                        # if user date is from past.
                        if shipping_date < datetime.datetime.now().date():
                            approve = input("Did you want to input past date?[Y/N]: ").upper()
                            if approve == "Y":
                                # leaving inner While loop.
                                break
                            elif approve == "N":
                                # if user don't approve to insert past date. Going back to input date.
                                continue
                            else:
                                print("Wrong input! (Yes-> Y/N <- No)")
                        else:
                            # leaving inner While loop.
                            break
                    # catching ValueError if user inputted date have invalid format.
                    except ValueError:
                        print("Date is wrong. Try again.")
                # leaving outer While loop.
                break
            else:
                print("Wrong input! (Yes-> Y/N <- No)")
        # preparing statement as string for insert into database.
        # noinspection SqlInsertValues
        statement = f"INSERT INTO shipments VALUES({statement}'{shipping_date}')"
        # returning statement for manager object to execute.
        return statement

    """Functions to display all database records sorted by column."""

    def sort_by_title(self):
        """Sorted by Title"""
        db_rows = self.Manager.execute("SELECT * FROM shipments ORDER BY Title;").fetchall()
        for row in db_rows:
            print(row)

    def sort_by_order_number(self):
        """Sorted by Order number"""
        db_rows = self.Manager.execute("SELECT * FROM shipments ORDER BY Order_number;").fetchall()
        for row in db_rows:
            print(row)

    def sort_by_article(self):
        """Sorted by Article"""
        db_rows = self.Manager.execute("SELECT * FROM shipments ORDER BY Article;").fetchall()
        for row in db_rows:
            print(row)

    def sort_by_amount(self):
        """Sorted by Amount"""
        db_rows = self.Manager.execute("SELECT * FROM shipments ORDER BY Amount;").fetchall()
        for row in db_rows:
            print(row)

    def sort_by_shipping_date(self):
        """Sorted by Shipping date"""
        db_rows = self.Manager.execute("SELECT * FROM shipments ORDER BY Shipping_date;").fetchall()
        for row in db_rows:
            print(row)

    def delete_shipment(self):
        """Delete shipment from database"""
        order_number = input("Input order number: ").strip()
        delete_statement = f"DELETE FROM shipments WHERE Order_number = '{order_number}'"
        display_statement = f"SELECT * FROM shipments WHERE Order_number = '{order_number}'"
        # selecting record from database to display.
        display_statement = self.Manager.execute(display_statement).fetchall()
        # checking if record is not empty.
        if len(display_statement) == 0:
            print("Shipment with that order number not exists... Try again.")
            return
        # if record is valid.
        while True:
            print(f"Selected shipment -> {display_statement}")
            select = input("Delete?[Y/N]: ").upper()
            if select == "Y":
                # deleting record from database.
                self.Manager.execute(delete_statement)
                print("Shipment successfully deleted from database.")
                break
            elif select == "N":
                print("Shipment not deleted.")
                break
            else:
                print("Wrong input! (Yes-> Y/N <- No)")

    def update_shipment(self):
        """Update value in selected shipment."""
        order_number = input("Input order number: ")
        # capitalizing string like it's in columns name if user input only small letters.
        column = input("What's you want change?(ex:.Title): ").capitalize()
        display_statement = f"SELECT * FROM shipments WHERE Order_number = '{order_number}'"
        display_list = self.Manager.execute(display_statement).fetchall()
        # checking if record it's not empty.
        if len(display_list) == 0:
            print("Shipment with that order number not exists... Try again.")
            return
        # if record is valid.
        print(f"To update -> {display_list}")
        new_value = input(f"Input new value for {column}: ")
        # updating record with new value.
        update_statement = f"UPDATE shipments SET {column} = '{new_value}' WHERE Order_number = '{order_number}'"
        self.Manager.execute(update_statement)
        # displaying final result.
        updated = self.Manager.execute(display_statement).fetchall()
        print(60 * "=",
              f"\nBefore update -> {display_list}\n"
              f"After update -> {updated}"
              )


" Program classes "


class MainMenu:
    """Class including all program classes as class attributes"""

    def __init__(self, shipment_register, work_with_shipments, shipments_board, exit_system):
        # assigning program classes as class attributes.
        self.shipment_register = shipment_register
        self.work_with_shipments = work_with_shipments
        self.shipments_board = shipments_board
        self.exit_system = exit_system
        self.options = {'1': self.shipment_register,
                        '2': self.work_with_shipments,
                        '3': self.shipments_board,
                        '4': self.exit_system
                        }

    def __call__(self, *args, **kwargs):
        # displaying main option's menu.
        print("__Shipment Registering System__".center(70), actual_date().center(20))
        for number, option in self.options.items():
            print(number + ".", option)
        self.option_selector()

    def option_selector(self):
        while True:
            try:
                select = input("-> ")
                if select in self.options.keys():
                    option = (self.options.get(select))
                    # calling function got from options.
                    option()
                else:
                    print("Option out of range.")
            # catching user wrong input.
            except ValueError:
                print("Wrong input!")


class ShipmentRegister:
    """Class responsible for collecting data from user and inserting it as new record into database"""

    def __init__(self):
        self.creator = DB.insert_statement_creator

    def __str__(self):
        # returning class representation in Main menu when displayed.
        return "Register New Shipment"

    def __call__(self):
        """Create a SQL statement and insert it into 'shipments' table as new record"""
        statement = self.creator()
        DB.insert_statement(statement)
        # after successfully insert data program is going back to main menu.
        start_program()


class WorkWithShipments:
    """Class responsible for deleting and updating data in database"""

    def __init__(self):
        # assigning database functions used for that class.
        self.update = DB.update_shipment
        self.delete = DB.delete_shipment
        self.go_back = start_program

    def __str__(self):
        # returning class representation in Main menu when displayed.
        return "Work With Shipments"

    def __call__(self, *args, **kwargs):
        # calling class function by calling a class in Main menu.
        self.shipment_updater()

    def shipment_updater(self):
        # update or delete record from database.
        update_options = {
            1: self.update,
            2: self.delete,
            3: self.go_back,
        }
        # options menu
        instructions = [
            "1. Update value in shipment",
            "2. Delete shipment from database",
            "3. Back to main menu",
        ]
        # display menu
        while True:
            print(60 * "=",
                  "\n", )
            [print(line) for line in instructions]
            select = int(input("-> "))
            try:
                if select in update_options.keys():
                    option = update_options.get(select)
                    # calling function got from options.
                    option()
                elif select == 3:
                    # going back to Main menu.
                    self.go_back()
            # catching a ValueError if user select wrong option.
            except ValueError:
                print("Option out of range!")


class ShipmentsBoard:
    """Class responsible for displaying database records with sorting functionalities"""

    def __init__(self, ):
        # assigning database functions used for that class.
        self.sort_by_title = DB.sort_by_title
        self.sort_by_order_number = DB.sort_by_order_number
        self.sort_by_article = DB.sort_by_article
        self.sort_by_amount = DB.sort_by_amount
        self.sort_by_shipping_date = DB.sort_by_shipping_date
        self.go_back = start_program

    def __str__(self):
        # returning class representation in Main menu when displayed.
        return "Shipments Board"

    def __call__(self):
        # Displaying all records from database when called from Main menu.
        db_rows = DB.Manager.execute("SELECT * FROM shipments;").fetchall()
        for row in db_rows:
            print(row)
        # calling class function by calling class in Main menu.
        self.shipment_displayer()

    def shipment_displayer(self):
        # options to display sorted database records.
        sorting_options = {
            1: self.sort_by_title,
            2: self.sort_by_order_number,
            3: self.sort_by_article,
            4: self.sort_by_amount,
            5: self.sort_by_shipping_date,
            6: self.go_back,
        }
        # options menu
        instructions = [
            "1. Display sorted",
            "2. Back to main menu"
        ]
        print(20 * "_", "\n")
        for instruction in instructions:
            print(instruction)
        # sorting menu
        sorting_instructions = [
            "1. By Title", "2. By Order number", "3. By Article",
            "4. By Amount", "5. By Shipping date", "6. Back to main menu"]
        while True:
            try:
                # selecting option from instructions
                select_outer = int(input("-> "))
                if select_outer == 1:
                    while True:
                        try:
                            [print(line) for line in sorting_instructions]
                            # selecting option from sorting options.
                            select_inner = int(input("-> "))
                            if select_inner in sorting_options.keys():
                                option = sorting_options.get(select_inner)
                                # calling function got from options.
                                option()
                        # catching a ValueError if user selected wrong option.
                        except ValueError:
                            print("Option out of range!")
                # going back to Main menu.
                elif select_outer == 2:
                    self.go_back()
            except ValueError:
                print("Options out of range!")


class ExitSystem:
    """Class responsible for closing system and saving user changes"""

    def __init__(self):
        # assigning database functions used for that class.
        self.save_changes = DB.save_changes

    def __str__(self):
        # returning class representation in Main menu when displayed.
        return "Exit"

    def __call__(self, *args, **kwargs):
        # calling database functionality to save changes.
        self.save_changes()
        print("Data successfully saved."
              "\nClosing system...")
        # closing system
        sys.exit(0)


" Utils Functions "


def actual_date() -> datetime:
    """Actual datetime in format (DD-MM-YYYY)"""
    actual_datetime = datetime.datetime.now().strftime("%d-%m-%Y")
    return actual_datetime


def start_program():
    """Starting program and displaying main screen."""
    MAIN_MENU()


""" Creating and assigning requirement objects. """
# database object
DB = Database()
# creating shipments table
DB.shipments_table_creator()
# assigning classes as functionalities of Main menu class.
MAIN_MENU = MainMenu(ShipmentRegister(), WorkWithShipments(), ShipmentsBoard(), ExitSystem())

if __name__ == "__main__":
    start_program()
