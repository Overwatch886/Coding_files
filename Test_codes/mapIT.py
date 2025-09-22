#! python3
" " "  Program to open Google Maps using an address specified in the command line else retrieve address from clipboard" " "
import webbrowser, sys, pyperclip
if len(sys.argv) > 1 :
    # retrieving address from command line input
    address = ' '.join(sys.argv[1:])
    print(address)
else :
    # retrieving address from clipboard if no input is made to command line
    address = pyperclip.paste()
webbrowser.open(f'https://www.google.com/maps/place/{address}')