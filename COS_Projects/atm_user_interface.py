from withdrawals import withdraw_funds
while True : 
    print("Welcome to the Overwatch Bank")
    print("What operation do you want to do?")
    user_command=input("Enter :\n W to make cash withdrawals \n B to check balance and \n T to make transfers")
    user_command = user_command.strip().upper()
    def user_command_processor(user_command):
        if user_command == 'W':
            withdrawals.withdraw_funds()
        