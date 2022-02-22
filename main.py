import os
import random    
import time     #just for testing for now, remove before submitted
import sqlite3  

# change database name as needed
data = sqlite3.connect('testdata.db')
cursor = data.cursor()

def loginScreen():
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

def newUserScreen():
    while True:
        # This loop prompts the user to input a username and confirm it
        newUser = input('Please enter a username: ')
        userConfirm = input(f'Are you sure you want [{newUser}] as your username? [y/n] ')
        if userConfirm == 'y':
            break
        else:
            os.system('cls||clear')

    os.system('cls||clear')    
    while True:
        # This loop prompts the user for a password and confirms it
        print(f'Please enter a username: {newUser}')
        password = input('Please choose a password: ')
        passConfirm = input(f'Confirm the password {password} [y/n] ')
        if passConfirm == 'y':
            break
        else:
            os.system('cls||clear')

    newCid = idGenerator(1) 
    cursor.execute('INSERT INTO customers VALUES (?,?,?)',(newCid,newUser,password))
    data.commit()

def idGenerator(type):
    ''' Generates id's. 
        If type = 1, function generates a cid (char(4) | cxxx)
        If type = 2, function generates a pid (int | xxxx)
        If type = 3, function generates a mid (char(4) | mxxx)
        If type = 4, function generetes a sid (int | xxxx)
        If type = 5, function generates a eid (char(4) | exxx)
    '''
    while True:
        # generates a random integer with leading zeros. cid, mid, and eid generate with leading letter
        # loops until a new valid id is generated
        if type == 1:
            retVal = 'c' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT cid FROM customers WHERE cid = (?)',(retVal,))
            row_count = cursor.rowcount
            if row_count <= 0:
                # value is not in the table, so it is a good id and we can add it
                break 
        elif type == 2:
            retVal = str(random.randrange(1,9999)).zfill(4)
            cursor.execute('SELECT pid FROM moviePeople WHERE pid = (?)',(retVal,))
            row_count = cursor.rowcount
            if row_count <= 0:
                # value is not in the table, so it is a good id and we can add it
                print('Value not in table')
                break 
        elif type == 3:
            retVal = 'm' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT mid FROM movies WHERE mid = (?)',(retVal,))
            row_count = cursor.rowcount
            if row_count <= 0:
                # value is not in the table, so it is a good id and we can add it
                print('Value not in table')
                break 
        elif type == 4:
            retVal = str(random.randrange(1,9999)).zfill(4)
            cursor.execute('SELECT sid FROM sessions WHERE sid = (?)',(retVal,))
            row_count = cursor.rowcount
            if row_count <= 0:
                # value is not in the table, so it is a good id and we can add it
                print('Value not in table')
                break 
        elif type == 5:
            retVal = 'e' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT eid FROM editors WHERE eid = (?)',(retVal,))
            row_count = cursor.rowcount
            if row_count <= 0:
                # value is not in the table, so it is a good id and we can add it
                print('Value not in table')
                break 
    return retVal



def main():
    os.system('cls||clear')     # these commands clear the terminal to make it look nicer
    editor = False
    while True:
        ''' This loop allows the user to select wether they are an editor or a customer '''
        break
    while True:

        ''' This loop allows the user to select wether they want to register or login normally.
            A User can press '1' to login or '2' to register.
            A User who enters anything else is instructed to try again
        '''

        choice = input('Type [1] to login or [2] to register: ')
        if choice == str(1):
            # Login Subroutine
            print('Logged in')
            break
        elif choice == str(2):
            # new user subroutine
            print('new User')
            break
        else:
            print('Invalid entry. Please try again')

    choice = int(choice)        # convert choice to an integer so we can utilize it later



    time.sleep(1)
    os.system('cls||clear')

newUserScreen()