# importing the random module
import random
#informing the user of the name of the game
print('ROCK . . . PAPER . .  SCISSORS . . ')
players_move = 's'
# win record
no_of_wins = 0
no_of_losses = 0
no_of_ties = 0    
while players_move != 'q' : 
    print(str(no_of_wins) + ' wins ' + str(no_of_ties) + ' ties ' + str(no_of_losses) + ' losses ')
    #player enters move
    print('enter (p)aper (s)cissors (r)ock or (q)uit')
    players_move = input('')
    computer_move = random.randint(1,3)
    if computer_move == 1 :
        computer_move = 'p'
        print('paper')
    elif computer_move == 2 :
         computer_move = 'r'
         print('rock')
    elif computer_move == 3 :
          computer_move = 's'
          print('scissors')
    else :
        print('Oops there is an error in this code')
    if (computer_move == 'p' and players_move == 'r')  :
        print('Paper defeats Rock')
        print('You lose !, Computer wins, Try again ')
        no_of_losses = no_of_losses + 1
    elif (computer_move == 'r' and players_move == 'p') :
        print('Paper defeats Rock')
        print('You win !!')
        no_of_wins = no_of_wins + 1
    elif (computer_move == 'r' and players_move == 's') :
        print('Rock defeats Scissors')
        print('You lose !, Computer wins, Try again ')
        no_of_losses = no_of_losses + 1
    elif (computer_move == 's' and players_move == 'r') :
        print('Rock defeats Scissors')
        print('You win!!')
        no_of_wins = no_of_wins + 1
    elif (computer_move == 's' and players_move == 'p' ) : 
        print('Scissors defeats Paper')
        print('You lose!, Computer wins, Try again')
        no_of_losses = no_of_losses + 1
    elif (computer_move == 'p' and players_move == 's' ) : 
        print('Scissors defeats Paper')
        print('You win!!')
        no_of_wins = no_of_wins + 1
    elif (computer_move == players_move) :
        print('There is a tie')
        no_of_ties = no_of_ties + 1
    elif (players_move == 'q') : 
        print('You ended the game. See you soon')
    else :
        print('Wrong input')
        print('Input r for ROCK, p for PAPER, s for SCISSORS or q to QUIT this game')
        