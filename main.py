import os        # used for os.system('cls||clear') which clears the terminal
import random    # used for generating random id's
import time      # used for sleeps & date manipulation   
import sqlite3   # used for sql database manipulation
import datetime  # used for recording session times 
import select

# change database name as needed
data = sqlite3.connect('testdata.db')
cursor = data.cursor()

def loginScreen(user = 1):
    ''' Input: type of user [1] customers or [2] editor
        Output: Tuple (boolean of logged in, username/[id if editor])

        Description: This function returns True if the password matches the username entered
        This function returns False if the username does not exist in the database or if the
        password does not match the username. The function also prints the appropriate messages
        to the terminal.
    '''
    os.system('cls||clear')
    print('Welcome\n')
    if user == 1:
        while True:
            os.system('cls||clear')
            
            choice = input('Please select [1] to login, [2] to register or type [esc] to go back: ')
            if choice == '1':
                attempts = 3
                while True:
                    custID = input('Please enter your customer id or type [esc] to return: ')
                    if custID == 'esc':
                        break
                    cursor.execute('SELECT cid FROM customers WHERE cid = (?)',(custID,))
                    row_count = cursor.fetchone()
                    if row_count:
                        # cid is in db, so we prompt for password
                        while True:
                            password = input('Please enter your password: ')
                            cursor.execute('SELECT name FROM customers WHERE cid = (?) AND pwd = (?)',(custID,password))
                            row_count = cursor.fetchone() #returns None if there were no results of the query
                            if row_count:
                                return (True,row_count[0],custID)
                            else:
                                attempts -= 1
                                print(f'Incorrect Password, Please try again. {attempts} attempts remaining')
                                time.sleep(1)
                                if attempts == 0:
                                    os.system('cls||clear')
                                    break
                    else:
                        print('ID not found. Please try again')
                        time.sleep(1)

            elif choice == '2':
                newUserScreen(1)
                return (False,'New User succesfully created!')
            elif choice == 'esc':
                return (False, 'Returning to Home Screen')
            else:
                print('That is in an invalid choice please try again')
                time.sleep(1)

    elif user == 2:
        # editor login screen
        attempts = 3
        while True:
            os.system('cls||clear')
            editorID = input('Please enter your editor ID or type [esc] to return: ')
            if editorID == 'esc':
                break
            cursor.execute('SELECT eid FROM editors WHERE eid = (?)', (editorID,))
            row_count = cursor.fetchone()
            if row_count:
                # prompt editor for password
                password = input('Please enter your password: ')
                cursor.execute('SELECT eid FROM editors WHERE eid = (?) AND pwd = (?)',(editorID,password))
                row_count = cursor.fetchone()
                if row_count:
                    return (True, row_count[0])
                else:
                    attempts -= 1
                    print(f'Incorrect password. {attempts} attempts remaining.')
                    time.sleep(1)
                    if attempts == 0:
                        break
    
        return (False, 'Returning to Home Screen')

def newUserScreen(user = 1):
    ''' Creates a new user and adds it into the database.
        type : specifies whether the user is adding a customer [1] or an editor [2] 
    '''
    if user == 1:
        while True:
            # This loop prompts the user to input a username and confirm it
            newUser = input('Please enter your name: ')
            userConfirm = input(f'Are you sure you want [{newUser}] as your name? [y/n] ')
            if userConfirm == 'y':
                break
            else:
                os.system('cls||clear')
        newUserID = idGenerator(1)

    os.system('cls||clear')

    if user != 1: # Generate an editor ID
        newUserID = idGenerator(5)  

    while True:
        # This loop prompts the user for a password and confirms it
        print(f'Your login ID is: {newUserID}')
        password = input('Please choose a password: ')
        passConfirm = input(f'Confirm the password {password} [y/n] ')
        if passConfirm == 'y':
            break
        else:
            os.system('cls||clear')

    if user == 1:
        # add new user data to db
        cursor.execute('INSERT INTO customers VALUES (?,?,?)',(newUserID,newUser,password))
        data.commit()
    else:
        # add new editor data to db
        cursor.execute('INSERT INTO editors VALUES (?,?)',(newUserID,password))
        data.commit()

    print(f'Your ID is: {newUserID} and your password is: {password}')
    time.sleep(2)

def idGenerator(idType):
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
        if idType == 1:
            retVal = 'c' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT cid FROM customers WHERE cid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count:
                # value is not in the table, so it is a good id and we can add it
                break 
        elif idType == 2:
            retVal = str(random.randrange(1,9999)).zfill(4)
            cursor.execute('SELECT pid FROM moviePeople WHERE pid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count:
                # value is not in the table, so it is a good id and we can add it
                break 
        elif idType == 3:
            retVal = 'm' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT mid FROM movies WHERE mid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count0:
                # value is not in the table, so it is a good id and we can add it

                break 
        elif idType == 4:
            retVal = str(random.randrange(1,9999)).zfill(4)
            cursor.execute('SELECT sid FROM sessions WHERE sid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count:
                # value is not in the table, so it is a good id and we can add it
                break 
        elif idType == 5:
            retVal = 'e' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT eid FROM editors WHERE eid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count:
                # value is not in the table, so it is a good id and we can add it

                break 
    return retVal

def sessionStart(cid):
    sid = idGenerator(4)
    sdate = datetime.datetime.now()
    cursor.execute('INSERT INTO sessions VALUES (?,?,?,?)',(sid,cid,sdate,None))
    data.commit()

def sessionEnd(sid):
    # get sdate from the session
    cursor.execute('SELECT sdate FROM sessions WHERE sid = (?)',(sid,))
    queryVal = cursor.fetchone()

    # find the duration by subtracting the current time from the start time
    # help for the datetime arithemtic from here:
    # https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python

    duration = datetime.datetime.now() - datetime.datetime.strptime(queryVal[0],'%Y-%m-%d %H:%M:%S')
    duration = duration.total_seconds()
    minutes = divmod(duration,60)[0]
    
    # insert the duration time back into the database
    cursor.execute('UPDATE sessions SET duration = (?) WHERE sid = (?)', (minutes,sid))
    data.commit()

    ''' Still need to figure out how we track how long the user has been wathcing a movie'''

def main():
    while True:
        sessionOpen = False
        os.system('cls||clear')     # these commands clear the terminal to make it look nicer
        editor = False
        while True:
            os.system('cls||clear')
            ''' This loop allows the user to select wether they are an editor or a customer '''
            print('-' * 50)
            print('Please choose an option to Login')
            print('[1] Customer')
            print('[2] Editor ')
            choice = input('Please type your selection here: ')
            if choice == '1':
                loginReturn = loginScreen(1)
                if loginReturn[0] == True:
                    name = loginReturn[1]
                    cid = loginReturn[2]
                    print(name)
                    break

            elif choice == '2':
                loginReturn = loginScreen(2)
                if loginReturn[0] == True:
                    editor = True
                    eid = loginReturn[1]
                    break
            else:
                print("Invalid choice, please try again")
                time.sleep(1)
        while True:
            # main menu
            os.system('cls||clear')
            if editor == True:
                print(f'Welcome editor {eid}!\n')
                print('[1] Add a movie')
                print('[2] Update a reccomendation')
                print('[3] Register a new editor')
            else:
                cursor.execute('SELECT * FROM customers WHERE cid = (?)',(cid,))
                print(f'Welcome {name}!\n')
                if sessionOpen == True:
                    cursor.execute('SELECT * FROM sessions WHERE cid = (?)',(cid,))
                    session = cursor.fetchone()
                    sid = session[0]
                    print(f'Current session open: {sid}')
                print('Please select an option below')
                print('[1] Begin a new session')
                print('[2] Search for movies')
                print('[3] End watching movie')
                print('[4] End the current session')

            print('[0] Logout')

            option = input('Please type your choice: ')
            if option == '0':
                print('Logging out..')
                time.sleep(2)
                break
            elif option == '1' and editor == True:
                # add movie
                pass
            elif option == '2' and editor == True:
                # update recommendation
                pass
            elif option == '3' and editor == True:
                # register a new editor
                newUserScreen(2)
            elif option == '1':
                if sessionOpen == True:
                    print('You already have a session open!')
                else:
                    sessionStart(cid)
                    sessionOpen = True
                    print('Session started!')
            elif option == '2':
                print(sid)
                if sessionOpen:
                    select.handleMovies(cursor, data, cid, sid)
                else:
                    select.handleMovies(cursor, data, cid, None)
            elif option == '3':
                select.endOneMovie(cursor, data, cid, sid)
            elif option == '4':
                cursor.execute('SELECT * FROM sessions WHERE cid = (?)',(cid,))
                session = cursor.fetchone()
                sid = session[0]
                print('Closing your session...')
                sessionEnd(sid)
                sessionOpen = False
            
            else:
                print('Invalid option, Please Try again')
                time.sleep(2)
            
            time.sleep(1)
            os.system('cls||clear')

main()
