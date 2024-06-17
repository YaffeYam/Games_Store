from datetime import datetime
import json
from icecream import ic
from standards import StoreActions, UserActions, AdminActions

DEBUG = True


def custom_output(*args):
    """
    Custom output function for logging with timestamp.
    flush() = The log file updates in real time
    """
    time_str = datetime.now().strftime("%d-%m-%Y - %H:%M:%S")
    log_message = f"{time_str} {' '.join(map(str, args))}\n"
    log_file.write(log_message)
    log_file.flush()  # Ensure it's written immediately
    print(log_message)


class Client:
    """
    Creating a Client Class
    """
    print("User Created!")
    # Constructor Method - Builds the object
    def __init__(self, user_id, first_name, last_name, username, password):
        """Initialize a new client."""
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self._password = password
        self._balance = 0
        self._purchase_history = []

    def __repr__(self):
        return f"Client (ID = {self.user_id}, Name={self.first_name} {self.last_name})"

    def __str__(self) -> str:
        return json.dumps({
            "User ID": self.user_id,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Username': self.username,
            'Balance': self._balance,
            'Purchase History': self._purchase_history
        })

    def basic_client(self):
        print(f"User ID: {self.user_id}, First Name: {self.first_name} Is A Basic Client")

    def reset_password(self, new_password):
        """Reset the client's password."""
        self._password = new_password

    def check_password(self, password):
        """Check if the provided password is correct."""
        return password == self._password

    def deposit(self, amount):
        """Deposit an amount to the client's balance."""
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount):
        """Withdraw an amount from the client's balance."""
        if self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError("Insufficient balance")

    def add_purchase(self, game_title):
        """Add a game to the client's purchase history."""
        # purchase_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self._purchase_history.append(("Title: " ,game_title))

    @property
    def balance(self):
        return self._balance

    @property
    def purchase_history(self):
        return self._purchase_history


# Creating an ADMIN USER class that inherits information from the Client class
class AdminUser(Client):
    """
    Creating an Admin user class that inherits from the Client class
    """

    def client_is_admin(self):
        print(f"User ID: {self.user_id}, First Name: {self.first_name} Is an Admin")

    def __str__(self) -> str:
        return json.dumps({
            "User ID": self.user_id,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Username': self.username,
            'Balance': self._balance,
            'Admin': True
        })


class Game:
    def __init__(self, title, price, stock):
        self.title = title
        self.price = price
        self.stock = stock

    def __str__(self):
        return json.dumps({
            'Title': self.title,
            'Price': f"${self.price:.2f}",
            'Stock': self.stock
        })


class GamingStore:
    """Represents the gaming store."""

    def __init__(self):
        """Initialize the gaming store with clients and games."""
        self.clients = []
        self.games = []

    def check_duplicate(self, user_id):
        """Check if a user ID already exists."""
        return any(client.user_id == user_id for client in self.clients)

    def create_account(self, user_id, first_name, last_name, username, password, is_admin=False):
        """Create a new client or admin account."""
        if self.check_duplicate(user_id):
            print(f"User ID {user_id} already exists.")
            return
        client = AdminUser(user_id, first_name, last_name, username, password) if is_admin else Client(user_id, first_name, last_name, username, password)
        self.clients.append(client)
        print(f"Account Created! ID: {client.user_id}, Name: {client.first_name} {client.last_name}")
        ic("User Created!", user_id)
        return client

    def get_client_by_id(self, user_id):
        """Retrieve a client by their user ID."""
        return next((client for client in self.clients if str(client.user_id) == str(user_id)), None)
    
    def get_client_by_username(self, username):
        """Retrieve a client by their username."""
        return next((client for client in self.clients if client.username == username), None)

    def show_all_clients(self, show_admins=False):
        """Display all clients, optionally showing admin users."""
        print("Accounts:")

        if show_admins:
            clients_to_show = self.clients
        else:
            clients_to_show = [client for client in self.clients if not isinstance(client, AdminUser)]

        for client in clients_to_show:
            if isinstance(client, AdminUser):
                client.client_is_admin()
            else:
                client.basic_client()
            print(client)
            print()


        print("Users: ")
        for client in self.clients:
            if not isinstance(client, AdminUser):
                client.basic_client()
                print(client)
                print()

    def deposit_to_account(self, client):
        """Allow a client to deposit money into their account."""
        try:
            amount = float(input("Enter amount to deposit: "))
            client.deposit(amount)
            print(f"Deposit of ${amount:.2f} successful. New balance: ${client.balance:.2f}")
        except ValueError:
            print("Invalid amount. Deposit failed.")

    def check_balance(self, client):
        """Check the balance of a client's account."""
        print(f"Current Balance for {client.username}: ${client.balance:.2f}")

    def delete_account(self, client):
        """Delete a client's account and log them out."""
        username = input("Enter username: ")
        password = input("Enter password: ")
        if client.username == username and client.check_password(password):
            confirmation = input("Are you sure you want to delete the account? (y/n): ")
            if confirmation.lower() == 'y':
                self.clients.remove(client)
                print(f"Account for {client.username} deleted.")
                print("Logging out...")
                return True  # Indicate successful deletion
        else:
            print("Incorrect username or password. Account deletion failed.")
        return False  # Indicate deletion failure

    def purchase_history(self, client):
        """View the purchase history of a client."""
        print(f"Purchase History for {client.username}:")
        for purchase in client.purchase_history:
            print(f"Game - {purchase}")

    def view_all_users(self):
        """View all registered users."""
        print("All Registered Users:")
        for client in self.clients:
            print(f'{client.user_id}: Name: {client.first_name} {client.last_name} (Usernamee: {client.username})')

    def client_withdrawal(self):
        """Withdraw an amount from a client's account."""
        self.show_all_clients()
        client_id = input("Please Insert User ID: ")
        c = self.get_client_by_id(client_id)
        if c:
            try:
                amount = float(input("Please Insert Amount to Withdraw: "))
                c.withdraw(amount)
                print("After Withdrawal: ")
                print(c)
                ic("Withdrawal: ", c)
            except ValueError as e:
                print(e)
        else:
            print(f"Client with ID {client_id} not found.")

    def view_store(self):
        """Display all games in the store."""
        if not self.games:
            print("OOPS...No games yet :(")
        else:
            for game in self.games:
                print(game)

    def view_library(self, client):
        """Display the games in the user's library (purchased games)."""
        if not client.purchase_history:
            print("You have no games in your library.")
        else:
            print("Your Library:")
            for game_title in client.purchase_history:
                print("Title: ", game_title)

    def add_game(self):
        """Add a new game to the store's inventory."""
        title = input("Enter game title: ")
        price = float(input("Enter game price: "))
        stock = int(input("Enter game stock: "))
        game = Game(title, price, stock)
        self.games.append(game)
        print ("Game", title, "added the inventory")

    def remove_game(self):
        """Remove a game from the store's inventory."""
        self.view_store()
        title = input("Enter the title of the game to remove: ")
        for game in self.games:
            if game.title == title:
                confirmation = input(f"Are you sure you want to delete the game '{title}'? (y/n): ")
                if confirmation.lower() == 'y':
                    self.games.remove(game)
                    print(f"The game '{title}' has been successfully deleted.")
                    return
                else:
                    print("Deletion cancelled.")
        print("Game not found.")

    def change_game_price(self):
        """Change the price of a game."""
        self.view_store()
        title = input("Enter the title of the game to change the price: ")
        for game in self.games:
            if game.title == title:
                new_price = float(input("Enter the new price: "))
                game.price = new_price
                print(f"Game '{title}' price updated to ${new_price}.")
                return
        print("Game not found.")

    def change_game_stock(self):
        """Change the stock quantity of a game."""
        self.view_store()
        title = input("Enter the title of the game to change the stock: ")
        for game in self.games:
            if game.title == title:
                new_stock = int(input("Enter the new stock: "))
                game.stock = new_stock
                print(f"Game '{title}' stock updated to {new_stock}.")
                return
        print("Game not found.")

    def purchase_game(self, client):
        """Allow a client to purchase a game."""
        self.view_store()
        title = input("Enter the title of the game to purchase: ")
        for game in self.games:
            if game.title == title:
                if game.stock > 0:
                    if client.balance >= game.price:
                        client.withdraw(game.price)
                        game.stock -= 1
                        client.add_purchase(game.title)
                        print(f"Game '{title}' purchased successfully.")
                    else:
                        print("Insufficient balance.")
                else:
                    print("Game is out of stock.")
                return
        print("Game not found.")

    def gift_game(self, gift_from):
        """Allow a user to gift a game to another registered user."""
        print("Accounts:")
        self.show_all_clients(show_admins=False)  # Show only non-admin users

        # Get recipient account
        while True:
            gift_to_id = input("Please Insert User ID To Gift To: ")
            if str(gift_to_id) == str(gift_from.user_id):
                print("You cannot gift a game to yourself. Please choose a different user.")
            else:
                gift_to = self.get_client_by_id(gift_to_id)
                if gift_to:
                    break
                else:
                    print("Invalid client ID. Please try again.")

        # Show available games
        self.view_store()
        title = input("Enter the title of the game to gift: ")
        
        for game in self.games:
            if game.title == title:
                if game.stock > 0:
                    if gift_from.balance >= game.price:
                        gift_from.withdraw(game.price)
                        gift_from.add_purchase(game.title)  # Add to gifting user's purchase history
                        game.stock -= 1
                        gift_to.add_purchase(game.title)  # Add to recipient's library
                        print(f"Game '{title}' gifted successfully to {gift_to.username}.")
                    else:
                        print("Insufficient balance.")
                else:
                    print("Game is out of stock.")
                return
        print("Game not found.")

    def show_menu(self):
        """Display the main menu for the store."""
        while True:
            for action in StoreActions:
                print(f'{action.value} - {action.name}')
            try:
                selection = int(input("Please Select - "))
                return StoreActions(selection)
            except (ValueError, KeyError):
                print("Invalid selection. Please try again.")
                continue

    def show_user_menu(self):
        """Display the menu for logged-in users."""
        while True:
            for action in UserActions:
                print(f'{action.value} - {action.name}')
            try:
                selection = int(input("Please Select - "))
                return UserActions(selection)
            except (ValueError, KeyError):
                print("Invalid selection. Please try again.")
                continue

    def show_admin_menu(self):
        """Display the menu for admin users."""
        while True:
            for action in AdminActions:
                print(f'{action.value} - {action.name}')
            try:
                selection = int(input("Please Select - "))
                if selection == AdminActions.VIEW_USERS.value:
                    return AdminActions.VIEW_USERS  # Return VIEW_USERS action
                return AdminActions(selection)
            except (ValueError, KeyError):
                print("Invalid selection. Please try again.")
                continue

def user_data_gathering():
    user_id = input("User ID: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    username = input("Username: ")
    password = input("Password: ")
    is_admin = input("Is the user an admin? (y/n): ").lower() == 'y'

    return user_id, first_name, last_name, username, password, is_admin

def test_add_clients(gaming_store):
    if DEBUG:
        c1 = gaming_store.create_account(1, "1", "1", "1", "1", is_admin=True)
        c1.deposit(500)
        c2 = gaming_store.create_account(2, "2", "2", "2", "2")
        c2.deposit(300)
        c3 = gaming_store.create_account(3, "3", "3", "3", "3")
        c3.deposit(50)

if __name__ == '__main__':
    log_file = open('debug.log', 'w')
    ic.configureOutput(outputFunction=custom_output)
    ic("Program started")

    gaming_store = GamingStore()
    test_add_clients(gaming_store)

    while True:
        user_selection = gaming_store.show_menu()

        if user_selection == StoreActions.REGISTER:
            user_data = user_data_gathering()
            gaming_store.create_account(*user_data)

        elif user_selection == StoreActions.LOGIN:
            username = input("Username: ")
            password = input("Password: ")
            user = next((client for client in gaming_store.clients if client.username == username and client.check_password(password)), None)
            if user:
                print(f"Welcome {user.first_name}!")

                if isinstance(user, AdminUser):
                    while True:
                        admin_selection = gaming_store.show_admin_menu()
                        if admin_selection == AdminActions.VIEW_STORE:
                            gaming_store.view_store()

                        elif admin_selection == AdminActions.VIEW_USERS:
                            gaming_store.view_all_users()

                        elif admin_selection == AdminActions.ADD_GAME:
                            gaming_store.add_game()

                        elif admin_selection == AdminActions.REMOVE_GAME:
                            gaming_store.remove_game()

                        elif admin_selection == AdminActions.CHANGE_STOCK:
                            gaming_store.change_game_stock()

                        elif admin_selection == AdminActions.CHANGE_PRICE:
                            gaming_store.change_game_price()

                        elif admin_selection == AdminActions.USER_LOGOUT:
                            break

                        elif admin_selection == AdminActions.EXIT:
                            log_file.close()
                            print("Goodbye :)")
                            exit()

                else:
                    while True:
                        user_selection = gaming_store.show_user_menu()
                        if user_selection == UserActions.VIEW_STORE:
                            gaming_store.view_store()

                        elif user_selection == UserActions.BUY_GAME:
                            gaming_store.purchase_game(user)

                        elif user_selection == UserActions.VIEW_LIBRARY:
                            gaming_store.view_library(user)

                        elif user_selection == UserActions.PURCHASE_HISTORY:
                            gaming_store.purchase_history(user)

                        elif user_selection == UserActions.SEND_GIFT:
                            gaming_store.gift_game(user)

                        elif user_selection == UserActions.DEPOSIT:
                            gaming_store.deposit_to_account(user)

                        elif user_selection == UserActions.CHECK_BALANCE:
                            gaming_store.check_balance(user)

                        elif user_selection == UserActions.USER_LOGOUT:
                            break

                        elif user_selection == UserActions.EXIT:
                            log_file.close()
                            print("Goodbye :)")
                            exit()

                        elif user_selection == UserActions.DELETE_ACCOUNT:
                            if gaming_store.delete_account(user):
                                print("Logged out.")
                                break
                            else:
                                print("Account deletion failed.")

                        elif user_selection == UserActions.USER_LOGOUT:
                            break

                        elif user_selection == UserActions.EXIT:
                            log_file.close()
                            print("Goodbye :)")
                            exit()

            else:
                print("Invalid username or password.")

        elif user_selection == StoreActions.EXIT:
            log_file.close()
            print("Goodbye :)")
            exit()
