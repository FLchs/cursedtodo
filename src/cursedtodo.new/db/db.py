# singleton.py
class DatabaseConnection:
    def __init__(self):
        print("Initializing database connection...")

    def connect(self):
        print("Connected to the database")

# The single instance of the DatabaseConnection
db_instance = DatabaseConnection()

