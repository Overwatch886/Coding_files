from atm_functions import *
while True : 
    account_number = validate_user(customers)
    if account_number is None:
        continue
    print("Welcome to the Overwatch Bank")
    print("What operation do you want to do?")
    
    user_command = input("Enter :\n W to make cash withdrawals \n B to check balance and \n T to make transfers \n D to make deposits")

     #Converting all user input to capital letterand eliminatingw hitespaces
    user_command = user_command.strip().upper()
    
    # Calling the ATM processor function
    atm_operations_processor(customers, user_command, account_number)
   