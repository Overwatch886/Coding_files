def withdraw_funds(amount):
    if balance > amount :
        balance = balance-amount
        print(f"N{amount} has been successfully withdrawn from available balance")
        print(f"New balance is {balance}")