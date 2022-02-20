import os
import time     #just for testing for now, remove before submitted
import sqlite3

data = sqlite3.connect('testdata.db')

def loginScreen(currentUserData):
    ''' Input: database containing usernames and their passwords
        Output: Boolean

        Description: This function returns True if the password matches the username entered
        This function returns False if the username does not exist in the database or if the
        password does not match the username. The function also prints the appropriate messages
        to the terminal.
    '''
    block = '-' * 50

    print(block)
    print('Welcome\n')
    username = input('Enter username: ')
    if username not in currentUsers:
        print('Sorry that is not a valid username!')
        return False
    password = input('Enter password: ')


def main():
    os.system('cls||clear')     # these commands clear the terminal to make it look nicer

    while True:

        ''' This loop allows the user to select wether they want to register or login normally.
            A User can press '1' to login or '2' to register.
            A User who enters anything else is instructed to try again
        '''

        choice = input('Type [1] to login or [2] to register: ')
        if choice == str(1): 
            print('Logged in')
            break
        elif choice == str(2):
            print('new User')
            break
        else:
            print('Invalid entry. Please try again')

    choice = int(choice)        # convert choice to an integer so we can utilize it later



    time.sleep(1)
    os.system('cls||clear')
main()