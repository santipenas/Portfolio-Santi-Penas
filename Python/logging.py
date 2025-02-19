import random
from datetime import datetime
import logging
import sys

# 🔹 Step 1: Set up the logger
logger = logging.getLogger(__name__)  
stream_handler = logging.StreamHandler(sys.stdout)  

# 🔹 Step 2: Define log format  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('formatted.log')  # Logs are saved in a file
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)  
logger.addHandler(file_handler)  

logger.setLevel(logging.INFO)  

# 🔹 Step 3: Simulating an ATM transaction system  
class BankAccount:
    def __init__(self):
        self.balance = 100
        logger.info("Bank account created with an initial balance of $100")

    def authenticate(self):
        while True:
            pin = int(input("Enter account pin: "))
            if pin != 1234:
                logger.error('Invalid PIN entered. Access denied.')
            else:
                logger.info("Authentication successful")
                break

    def deposit(self):
        try:
            amount = float(input("Enter amount to be deposited: "))
            if amount < 0:
                logger.warning("Attempted to deposit a negative amount.")
            else:
                self.balance += amount
                logger.info(f"Deposit Successful: ${amount} | New Balance: ${self.balance}")
        except ValueError:
            logger.error("Deposit failed: Non-numeric input detected.")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to be withdrawn: "))
            if self.balance >= amount:
                self.balance -= amount
                logger.info(f"Withdrawal Successful: ${amount} | New Balance: ${self.balance}")
            else:
                logger.error("Insufficient funds for withdrawal.")
        except ValueError:
            logger.error("Withdrawal failed: Non-numeric input detected.")

    def display(self):
        logger.info(f"Current balance: ${self.balance}")

# 🔹 Step 4: Running the ATM System
acct = BankAccount()
acct.authenticate()
acct.deposit()
acct.withdraw()
acct.display()

