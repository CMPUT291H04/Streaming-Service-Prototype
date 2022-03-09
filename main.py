import os        # used for os.system('cls||clear') which clears the terminal
import random    # used for generating random id's
import time      # used for sleeps & date manipulation   
import sqlite3   # used for sql database manipulation
import datetime  # used for recording session times 
import select


while True:
    filename = input('Please enter the filename of your database: (ex: \'database.db\'): ')
    if os.path.exists(filename):
        data = sqlite3.connect(filename)
        cursor = data.cursor()
        break
    else:
        print('Sorry unable to connect to that database!')
        time.sleep(3)
        os.system('cls||clear')


def askScore(m1name, m2name):
    '''Keeps prompting user for a valid year until one is given.
    Args:
            None
    Returns:
            integer year
    '''             
    validscore = False
    while not validscore:
        validscore = True
        print("\nWhat score would you like to give", m1name, "|", m2name + '? ', end = '')
        score = input()
        try:
            score = float(score)
        except:
            print("ERROR: score must be a number between 0 and 1, please try again.")
            validscore = False
        else:
            if score < 0 or score > 1:
                print("ERROR: score must be a number between 0 and 1, please try again.")
                validscore = False                
    return score     


def handleRecommendations(watched):
    '''Handles the data returned from the recommendations table and displays it to the user in a presentable format.
     Args:
            a list of watched movies.
    Returns:
            None
    '''             
    if len(watched) == 0:
        print('Looks like there is nothing here!')
        input('\nPress enter to return...')
        return
    
    elif len(watched) == 1:
        print(watched[0][0], '-', watched[0][1])
        input('\nPress enter to return...')
        return        
    
    combs = []
    while len(watched) > 1:
        current = watched.pop(0)
        for item in watched:
            if item != current:
                combs.append([current[0], current[1], current[2], item[0], item[1], item[2]])
                combs.append([item[0], item[1], item[2], current[0], current[1], current[2]])
    
    reccomendlist = []
    for comb in combs:
        if comb[2] == comb[5] and comb not in reccomendlist:
            reccomendlist.append(comb)
    
    if len(reccomendlist) == 0:
        print("No two movies have been watched by the same user")
        input("\nPress enter to enter...")
    
    for i in range(len(reccomendlist)):
        reccomendlist[i] = (reccomendlist[i][0], reccomendlist[i][1], None, reccomendlist[i][3], reccomendlist[i][4], None)
        
    
    watched_count = {}
    for pair in reccomendlist:
        watched_count[pair] = watched_count.get(pair, 0) + 1        #Counts number of matches each hit got    
    
    pairs_sorted = select.dictToSortedList(watched_count)
    
    i = 1
    even = 1
    print("\nBelow is each pairing of movies watched in the same selected period of time, shown both ways. The last value is the recommened score ('NULL' if pair isn't in the database):\n")
    for pair in pairs_sorted:
        watched = pair[0]
        recommended = pair[3]
        cursor.execute("SELECT score from recommendations \
                        WHERE watched = :watched AND recommended = :recommended;", {'watched': watched, 'recommended': recommended})
        score = cursor.fetchone()

        if score != None:
            print(str(i) + '.', pair[1], pair[0], '|', pair[4], pair[3], '|', watched_count.get(pair, 0), "views", "|", score[0])
            pairs_sorted[i-1] = (pairs_sorted[i-1], score[0])
        else:
            print(str(i) + '.', pair[1], pair[0], '|', pair[4], pair[3], '|', watched_count.get(pair, 0), "views", "| NULL")
            pairs_sorted[i-1] = (pairs_sorted[i-1], score)
        
        if even % 2 == 0:
            print()
        even += 1
        i += 1
    
    choice = None
    while choice not in range(len(pairs_sorted)):
        choice = input("\nWhich one would you like to give a score (and add to database) / update its score / delete from database (if exists): ")      
        try:
                choice = int(choice) - 1
        except:
            print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.')   #If choice is a non-valid string.
        else:
            if choice not in range(len(pairs_sorted)):
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.')    #If choice is a non-valid integer.             
    
    m1name = pairs_sorted[choice][0][1]
    m2name = pairs_sorted[choice][0][4] 
    m1mid = pairs_sorted[choice][0][0]
    m2mid = pairs_sorted[choice][0][3]
    
    if pairs_sorted[choice][1] == None:
        score = askScore(m1name, m2name)
        cursor.execute("INSERT INTO recommendations VALUES (:m1, :m2, :score);", {"m1": m1mid, "m2": m2mid, "score": score})
        data.commit()
    else:
        choice = input("\nWould you like to delete this pair's score from the database, or update their score (d/u)? ").lower()
        while choice not in ['d', 'delete', 'u', 'update']:
            if choice not in ['d', 'delete', 'u', 'update']:
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding letter.')
                choice = input("\nWould you like to delete this pair's score from the database, or update their score (d/u)? ").lower()
        
        if choice in ['u', 'update']:
            score = askScore(m1name, m2name)
            cursor.execute("UPDATE recommendations \
                            SET score = :score \
                            WHERE watched = :m1 AND recommended = :m2;", {"m1": m1mid, "m2": m2mid, "score": score})
            data.commit()
        else:
            cursor.execute("DELETE FROM recommendations \
                            WHERE watched = :m1 AND recommended = :m2;", {"m1": m1mid, "m2": m2mid, "score": score})
            data.commit()            
    
    return
    
def updateRecommendation():
    ''' Updates recommendation for a movie.
     Args:
            None
    Returns:
            None
    '''             
    os.system('cls||clear')
    rtype = input("Would you like to see a daily, monthly, or annual report (d/m/a)? ").lower()
    while rtype not in ['d', 'daily', 'm', 'monthly', 'a', 'annual']:
        os.system('cls||clear')
        print('ERROR: Invalid selection, please try again and make sure you type just the corresponding letter.\n')
        rtype = input("Would you like to see a daily, monthly, or annual report (d/m/a)? ")
        
    if rtype in ['d', 'daily']:
        cursor.execute("SELECT w.mid, m.title, c.cid \
                    FROM sessions s, watch w, movies m, customers c \
                    WHERE w.sid = s.sid AND m.mid = w.mid \
                    AND w.cid = s.cid AND c.cid = w.cid \
                    AND s.sdate BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime');")
        watched = cursor.fetchall()
    
    elif rtype in ['m', 'monthly']:
        cursor.execute("SELECT w.mid, m.title, c.cid \
                    FROM sessions s, watch w, movies m, customers c \
                    WHERE w.sid = s.sid AND m.mid = w.mid \
                    AND w.cid = s.cid AND c.cid = w.cid \
                    AND s.sdate BETWEEN datetime('now', '-29 days') AND datetime('now', 'localtime');") 
        watched = cursor.fetchall()
    
    else:
        cursor.execute("SELECT w.mid, m.title, c.cid \
                    FROM sessions s, watch w, movies m, customers c \
                    WHERE w.sid = s.sid AND m.mid = w.mid \
                    AND w.cid = s.cid AND c.cid = w.cid \
                    AND s.sdate BETWEEN datetime('now', '-364 days') AND datetime('now', 'localtime');") 
        watched = cursor.fetchall()
    
    if len(watched) <= 1:
        print("Not enough movies to update recommendations.")
        input("Press enter to return...")
        return
    
    handleRecommendations(watched)


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
        If type = 2, function generates a pid (char(4) | pxxx)
        If type = 3, function generates a mid (int | xxxx)
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
            retVal = 'p' + str(random.randrange(1,999)).zfill(3)
            cursor.execute('SELECT pid FROM moviePeople WHERE pid = (?)',(retVal,))
            row_count = cursor.fetchone()
            if not row_count:
                # value is not in the table, so it is a good id and we can add it
                break 
        elif idType == 3:
            retVal = str(random.randrange(1,9999)).zfill(3)
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
    return sid

def sessionEnd(sid):
    # get sdate from the session
    cursor.execute('SELECT sdate FROM sessions WHERE sid = (?)',(sid,))
    queryVal = cursor.fetchone()

    # find the duration by subtracting the current time from the start time
    # help for the datetime arithemtic from here:
    # https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
    
    duration = datetime.datetime.now() - datetime.datetime.strptime(queryVal[0][:-7],'%Y-%m-%d %H:%M:%S')
    duration = duration.total_seconds()
    minutes = divmod(duration,60)[0]
    
    # insert the duration time back into the database
    cursor.execute('UPDATE sessions SET duration = (?) WHERE sid = (?)', (minutes,sid))
    data.commit()

    ''' Still need to figure out how we track how long the user has been wathcing a movie'''

def main():

    # change database name as needed
    # opens data base one folder up
    
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
                    #cursor.execute('SELECT * FROM sessions WHERE cid = (?)',(cid,))
                    #session = cursor.fetchone()
                    #sid = session[0]
                    print(f'Current session open: {sid}')
                print('Please select an option below')
                print('[1] Begin a new session')
                print('[2] Search for movies')
                print('[3] End watching movie')
                print('[4] End the current session')

            print('[0] Logout')

            option = input('Please type your choice: ')
            if option == '0':
                if sessionOpen == True:
                    sessionEnd(sid)
                    select.endAllMovies(cursor,data,cid,sid)
                print('Logging out..')
                time.sleep(2)
                break

            elif option == '1' and editor == True:
                select.addMovie(cursor, data)

            elif option == '2' and editor == True:
                updateRecommendation()

            elif option == '3' and editor == True:
                # register a new editor
                newUserScreen(2)

            elif option == '1':
                # open session
                if sessionOpen == True:
                    print('You already have a session open!')
                else:
                    sid = sessionStart(cid)
                    sessionOpen = True
                    print('Session started!')

            elif option == '2':
                if sessionOpen:
                    select.handleMovies(cursor, data, cid, sid)
                else:
                    select.handleMovies(cursor, data, cid, None)

            elif option == '3':
                if sessionOpen:
                    select.endMovie(cursor, data, cid, sid)
                else:
                    select.endMovie(None, None, None, None)
                    
                
            elif option == '4':
                if sessionOpen == True:
                    print(sid)
                    print('Closing your session...')
                    sessionEnd(sid)
                    sessionOpen = False
                    select.endAllMovies(cursor,data,cid,sid)
                else:
                    print('You do not currently have an open session!')
            
            else:
                print('Invalid option, Please Try again')
                time.sleep(2)
            
            time.sleep(1)
            os.system('cls||clear')

main()