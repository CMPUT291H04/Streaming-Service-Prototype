import	sqlite3
import os
from time import perf_counter

global watchingList
watchingList = []

def printMovieInfo(movies, selection, cursor):
    '''Displays more information about a selected movie.
     Args:
            -matches: A list containing tuples.
            -selection: A list containing info about a selected movie.
    Returns:
            None
    '''
    
    selectedtitle = movies[selection][0]
    selectedyear = movies[selection][1]
    selectedruntime = movies[selection][2]
    selectedmid = movies[selection][3]
    
    cursor.execute('SELECT mp.pid, mp.name, c.role \
                    FROM movies m, moviePeople mp, casts c \
                    WHERE mp.pid = c.pid AND m.mid = c.mid \
                    AND m.mid = :selectedmid', {"selectedmid": selectedmid})     
    castinfo = cursor.fetchall()            
    
    cursor.execute('SELECT COUNT(*) \
                    FROM movies m, watch w \
                    WHERE m.mid = w.mid AND w.duration >= (m.runtime/2) \
                    AND m.mid = :selectedmid', {"selectedmid": selectedmid})
    numwatched = cursor.fetchone()[0]       
    
    print('Movie information - \'' + selectedtitle + '\':\n')
    print('Release year:', selectedyear)
    print('       Views:', numwatched)
    print('     Runtime:', selectedruntime, 'minutes')
    print('        Cast:')
    for actor in castinfo:
        actorname = actor[1]
        actorrole = actor[2]
        print('\t\t' + actorname, 'as', actorrole)
    
    
    input('\n Press enter to return...')    
    
    return



def checkIfFollowing(cursor, cid, pid):
    '''Returns True if the given cid is already following the given pid, False otherwise.
         Args:
                -cid: A string containing the logged-in customer's id.
                -pid: A string containing a cast member's id.
        Returns:
                None
    ''' 
    
    cursor.execute('SELECT COUNT(*) FROM follows \
                    WHERE cid = :cid AND pid = :pid', {"cid": cid, "pid": pid})
    
    following = cursor.fetchone()[0]
    
    return following



def followCastMenu(movies, selection, cursor, data, cid):
    '''Displays cast from a selected movie to choose to follow one from.
     Args:
            -matches: A list containing tuples.
            -selection: A list containing info about a selected movie.
            -cid: A string containing the logged-in customer's id.
    Returns:
            None
    '''    
    
    selectedtitle = movies[selection][0]
    selectedmid = movies[selection][3]
    
    cursor.execute('SELECT mp.pid, mp.name, c.role \
                    FROM movies m, moviePeople mp, casts c \
                    WHERE mp.pid = c.pid AND m.mid = c.mid \
                    AND m.mid = :selectedmid', {"selectedmid": selectedmid})     
    castinfo = cursor.fetchall()                    
    
    print(selectedtitle + '\'s\" cast:')  
    for i in range(len(castinfo)):
        actorname = castinfo[i][1]
        actorrole = castinfo[i][2]
        print('\t\t[' + str(i+1) + ']', actorname, 'as', actorrole)            
    
    cchoice = -1
    try:      
        cchoice = int(input('Please choose one of the following cast members to follow: ')) - 1
    
    except:
        cchoice = -1
    
    while cchoice not in range(len(castinfo)):
        os.system('cls||clear')
        print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')
        print(selectedtitle + '\'s\" cast:')
        for i in range(len(castinfo)):
            actorname = castinfo[i][1]
            actorrole = castinfo[i][2]
            print('\t\t[' + str(i+1) + ']', actorname, 'as', actorrole)            
        try:
            cchoice = int(input('Please choose one of the following cast members to follow: ')) - 1
        except:
            cchoice = -1
    
    pid = castinfo[cchoice][0]
    actorname = castinfo[cchoice][1]
    
    alreadyFollowing = checkIfFollowing(cursor, cid, pid)
    
    if not alreadyFollowing:
        cursor.execute("INSERT INTO follows \
                        VALUES (:cid, :pid);", {"cid": cid, "pid": pid})
        data.commit()
    
    else:
        print("\nYou are already following", actorname)
        input('\nPress enter to return...')
    
    return



def endOneMovie(cursor, data, cid, sid, movieindex):
    '''Ends a single movie and adds it to the database.
    Args:
            -The cid of a user.
            -The sid of a session.
            -index of a movie in the current watchlist.
    Returns:
            None
    '''                    
    
    mid = watchingList[movieindex][0]
    title = watchingList[movieindex][1]
    runtime = watchingList[movieindex][2]
    timestarted = watchingList[movieindex][3] 
    
    duration = int((perf_counter() - timestarted)/60)        #Current time - time started, and converted to integer minutes (rounded down, design choice).
    if duration > runtime:
        duration = runtime
    
    cursor.execute("INSERT INTO watch VALUES (:sid, :cid, :mid, :duration);", {"sid": sid, "cid": cid, "mid": mid, "duration": duration})
    data.commit()
    
    watchingList.pop(movieindex)      #Remove movie being watched from the watching list.
        
    return



def endOneMovieFromGT5(cursor, data, cid, sid):
    '''Handles the sub-functionality of deleting a movie while more than 5 movies are being played.
    Args:
            -The cid of a user.
            -The sid of a session.
    Returns:
            None
    '''                    
    
    scroll_pos = 0
    choice = -1
    while choice not in range(len(watchingList)):
        
        print("You are currently watching", len(watchingList), "movies, please select which one you want to stop watching:\n")
        
        for i in range(5):
            print(str(i+1+scroll_pos) + '. ' + str(watchingList[i+scroll_pos][1]))
        
        choice = input("\nPlease choose a movie by typing its corresponding number, or scroll down and up with 'S' or 'W' respectively: ")     
        os.system('cls||clear')
        
        if choice in ['s', 'S']:
            if (5 + scroll_pos) >= len(watchingList):
                print('You are at the end of the results, can not scroll down any further.\n')
            else:
                scroll_pos += 1
        
        elif choice in ['w', 'W']:
            if scroll_pos == 0:
                print('Already at the top of the results, can not scroll up any further.\n')
            else:
                scroll_pos -= 1
        
        else:
            try:
                choice = int(choice) - 1
            except:
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')   #If choice is a non-valid string.
            else:
                if choice not in range(len(watchingList)):
                    print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')    #If choice is a non-valid integer.                   
    
    endOneMovie(cursor, data, cid, sid, choice)
 
    return



def endOneMovieFromLE5(cursor, data, cid, sid):
    '''Handles the sub-functionality of deleting a movie while 5 or less movies are being played.
    Args:
            -The cid of a user.
            -The sid of a session.
    Returns:
            None
    '''             
    
    choice = None
    while choice not in range(len(watchingList)):
        
        print("You are currently watching", len(watchingList), "movie(s), please select which one you want to stop watching:\n")
        
        for i in range(len(watchingList)):
            print(str(i+1) + '. ' + watchingList[i][1])      
        
        choice = input('\nPlease choose a movie by typing its corresponding number: ')
        
        os.system('cls||clear')
        
        try:
                choice = int(choice) - 1
        except:
            print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')   #If choice is a non-valid string.
        else:
            if choice not in range(len(watchingList)):
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')    #If choice is a non-valid integer.              
    
    endOneMovie(cursor, data, cid, sid, choice)  
    
    return



def endMovie(cursor, data, cid, sid):
    '''Ends a movie(s) currently being played in the session.
    Args:
            -The cid of a user.
            -The sid of a session.
    Returns:
            None
    '''            
    
    os.system('cls||clear') 
    if len(watchingList) == 0:
        input("You aren't currently watching any movies.\n\nPress enter to return...")
        
    elif len(watchingList) <= 5:
        endOneMovieFromLE5(cursor, data, cid, sid)
    
    else:
        endOneMovieFromGT5(cursor, data, cid, sid)
     
    return



def endAllMovies(cursor, data, cid, sid):
    '''Ends all movies currently being played in the session.
    Args:
            -The cid of a user.
            -The sid of a session.
    Returns:
            None
    '''             
    
    while len(watchingList) != 0:
        endOneMovie(cursor, data, cid, sid, 0)
    
    return


    
def movieScreenMenu(movies, selection, cursor, data, cid, sid):
    '''Displays the movie screen.
     Args:
            -matches: A list containing tuples.
            -selection: A list containing info about a selected movie.
            -cid: A string containing the logged-in customer's id.
    Returns:
            None
    '''        
    selectedtitle = movies[selection][0]
    selectedyear = movies[selection][1]
    selectedruntime = movies[selection][2]
    selectedmid = movies[selection][3]
    
    
    print('You are now in \"' + selectedtitle + '\'s\" ' + 'movie screen, please select one of the following:\n[1] Follow a member of the cast\n[2] Watch movie\n')
    mchoice = input('Please type choice here: ')    
    while mchoice not in ['1', '2']:
        os.system('cls||clear')
        print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')
        print('You are now in \"' + selectedtitle + '\'s\" ' + 'movie screen, please select one of the following:\n[1] Follow a member of the cast\n[2] Watch movie\n')
        mchoice = input('Please type choice here: ')
    
    if mchoice == '1':
        os.system('cls||clear')
        followCastMenu(movies, selection, cursor, data, cid)
    
    else:
        
        if sid == None:
            print("\nERROR: You can't watch a movie without starting a session first. Please start a session and attempt this action again.")
            input('\nPress enter to return...')
        
        else:
            global watchingList
            for movie in watchingList:
                if selectedtitle == movie[1]:
                    print("You are already watching this movie in this session")
                    input("\nPress enter to enter...")
                    return
            watchingList.append((selectedmid, selectedtitle, selectedruntime, perf_counter()))          #perfcounter records the current CPU time.
            
        return
    
    
    
def askMovieMenu(movies, selection, cursor, data, cid, sid):
    '''Displays options the users can go through after choosing a movie.
     Args:
            -matches: A list containing tuples.
            -selection: A list containing info about a selected movie.
            -cid: A string containing the logged-in customer's id.
    Returns:
            None
    '''     
    print('Would you like to:\n[1] Find out more information about \'' + movies[selection][0] + '\'\n[2] Proceed to the screen')
    uchoice = input('Please type choice here: ')
    
    while uchoice not in ['1', '2']:
        os.system('cls||clear')
        print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')
        print('Would you like to:\n[1] Find out more information about \'' + movies[selection][0] + '\'\n[2] Proceed to the screen')
        uchoice = input('Please type choice here: ')
    
    os.system('cls||clear')
    
    
    if uchoice == '1':
        printMovieInfo(movies, selection, cursor)     
    
    else:
        movieScreenMenu(movies, selection, cursor, data, cid, sid)
       
    return



def displayMatchesLE5(matches):
    '''Displays matches when the search returns less than or equal to 5 results.
    Args:
            -matches: A list containing tuples.
    Returns:
            Users's movie selection.
    '''   
    choice = None
    while choice not in range(len(matches)):
        
        print('Search has returned', len(matches), 'result(s).\n')
        
        for i in range(len(matches)):
            print(str(i+1) + '. ' + matches[i][0], '| Year: ' + str(matches[i][1]), '| Runtime: ' + str(matches[i][2]) + ' minutes')             
        
        choice = input('\nPlease choose a movie by typing its corresponding number: ')
        
        os.system('cls||clear')
        
        try:
                choice = int(choice) - 1
        except:
            print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')   #If choice is a non-valid string.
        else:
            if choice not in range(len(matches)):
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')    #If choice is a non-valid integer.              
    
    return choice



def displayMatchesGT5(matches):
    '''Displays matches when the search returns more than 5 results.
    Args:
            -matches: A list containing tuples.
    Returns:
            Users's movie selection.
    ''' 
    
    scroll_pos = 0
    choice = -1
    while choice not in range(len(matches)):
        
        print('Search has returned', len(matches), 'results.\n')
        
        for i in range(5):
            print(str(i+1+scroll_pos) + '. ' + str(matches[i+scroll_pos][0]), '| Year: ' + str(matches[i+scroll_pos][1]), '| Runtime: ' + str(matches[i+scroll_pos][2]) + ' minutes')
        
        choice = input("\nPlease choose a movie by typing its corresponding number, or scroll down and up with 'S' or 'W' respectively: ")     
        os.system('cls||clear')
        
        if choice in ['s', 'S']:
            if (5 + scroll_pos) >= len(matches):
                print('You are at the end of the results, can not scroll down any further.\n')
            else:
                scroll_pos += 1
        
        elif choice in ['w', 'W']:
            if scroll_pos == 0:
                print('Already at the top of the results, can not scroll up any further.\n')
            else:
                scroll_pos -= 1
        
        else:
            try:
                choice = int(choice) - 1
            except:
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')   #If choice is a non-valid string.
            else:
                if choice not in range(len(matches)):
                    print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')    #If choice is a non-valid integer.                   

    return choice



def displayMatches(matches):
    '''Displays a selection of movies that the user can choose from.
        Args:
            -matches: A list containing tuples.
        Returns:
            Users selection in integer form.
    '''
    if len(matches) == 0:
        print('Search has returned', len(matches), 'results.\n')
        print('Looks like there is nothing here!')
        input('\nPress enter to return...')
        choice = -1
    
    elif len(matches) <= 5:    
        choice = displayMatchesLE5(matches) 
    
    else:
        choice = displayMatchesGT5(matches)       
 
    return choice




def dictToSortedList(hitDict):
    '''Sorts a dictionary by value and stores the key into a list.
        Args:
            -hitDict: Any dictionary.
        Returns:
            A list containing keys from the dictionary, sorted.
    ''' 
    dictCopy = hitDict.copy()
    sorted_values_list = []
    sorted_values = sorted(dictCopy.values(), reverse=True)
    for value in sorted_values:
        for key in dictCopy.keys():
            if dictCopy.get(key, 0) == value:
                sorted_values_list.append(key)
                dictCopy.pop(key)
                break
    
    return sorted_values_list



def searchWordsMenu(cursor):
    '''Searches for specified data from a given database based on user-inputted keywords.
        Args:
            None
        Returns:
            A list containing matching hits from the database, in sorted order based on how many keywords each hit matched with.
    ''' 
    #NOTE: I chose this search algorithm because it helps return more accurate search results when the user enters a very specific
    #input (inputs that include the whole title of a movie or name of cast). 
    
    #First, look for hits, and include duplicates (will use duplicates to determine order):
    keys = input('What are you searching for today: ')
    keys = keys.split(" ")
    hits = []
    for key in keys:
        if key != '':   #Makes sure no results are returned if user inputs nothing.
            key = '%' + key + '%'
            cursor.execute("SELECT DISTINCT title, year, runtime, m.mid \
                            FROM movies m, casts c, moviePeople mp \
                            WHERE m.mid = c.mid AND c.pid = mp.pid \
                            AND (m.title LIKE :key OR mp.name LIKE :key OR c.role LIKE :key);", {"key": key})
            hits = hits + cursor.fetchall()
    
    #Second, count duplicates to determine order:
    hits_count = {}
    for hit in hits:
        hits_count[hit] = hits_count.get(hit, 0) + 1        #Counts number of matches each hit got
    
    hits_sorted = dictToSortedList(hits_count)
    
    return hits_sorted

 

def handleMovies(cursor, data, cid, sid):
    '''Manages the movie search section.
    Args:
            None
    Returns:
            None
    ''' 
    
    os.system('cls||clear')
    hits_sorted = searchWordsMenu(cursor)
    
    os.system('cls||clear')
    movie_selected = displayMatches(hits_sorted)
    
    if movie_selected != -1:
        os.system('cls||clear')
        askMovieMenu(hits_sorted, movie_selected, cursor, data, cid, sid)
    
    return



def midExists(cursor, mid):
    '''Checks wether a given mid already exists in a database.
    Args:
            The mid of a movie.
    Returns:
            Wether the mid exists or not.
    '''         
    
    mid = (mid,)
    cursor.execute("SELECT mid FROM movies;")
    mids = cursor.fetchall()
    if mid in mids:
        print("ERROR: another movie already has this mid, please try again.\n")
        return True
    else:
        return False



def pidExists(cursor, pid):
    '''Checks wether a given pid already exists in a database.
    Args:
            The mid of a movie.
    Returns:
            Wether the mid exists or not.
    '''   
    
    pid = (pid,)
    cursor.execute("SELECT pid FROM casts;")
    pids = cursor.fetchall()
    if pid in pids:
        return True
    else:
        return False



def addCast(cursor, data, mid):
    '''Handles the sub-functionality of adding a cast member.
    Args:
            The mid of a movie.
    Returns:
            None
    '''         
    
    validpid = False   
    while not validpid:
        validpid = True
        
        pid = input("\nPlease provide the pid of a cast member. The pid should follow the format pxxx (where xxx is a 3-digit integer): ")    
        if pid[0] != 'p' or len(pid) != 4:
            print("ERROR: pid is not valid, please try again.")
            validpid = False
        try:
            int(pid[1:4])
        except:
            print("ERROR: pid is not valid, please try again.")
            validpid = False
    
    if pidExists(cursor, pid):
        print("ERROR: This pid already exists, please try another one.")
        addCast(cursor, data)
    
    else:
        validyear = False
        while not validyear:
            validyear = True
            year = input("\nPlease provide the birthyear of the actor: ")      #Didn't give year time constraints because movie might be coming out in the future.
            try:
                year = int(year)
            except:
                print("ERROR: year must be an integer, please try again.")
                validyear = False
        name = input("\nPlease provide the actor name: ")
        role = input("\nPlease provide the actor role: ")
        cursor.execute("INSERT INTO moviePeople VALUES (:pid, :name, :year);", {"pid": pid, "name": name, "year": year})
        data.commit()     
        cursor.execute("INSERT INTO casts VALUES (:mid, :pid, :role);", {"mid": mid, "pid": pid, "role": role})
        data.commit()
        print("Added", name, "as a member of the cast!")
        input('\n Press enter to return...')  
    
    return



def askCast(cursor, data, mid):
    '''Supporting function for addMovie() that asks for cast to be added to movie.
    Args:
            The mid of a movie.
    Returns:
            None
    '''         
    
    validpid = False   
    while not validpid:
        validpid = True
        
        pid = input("\nPlease provide the pid of a cast member. The pid should follow the format pxxx (where xxx is a 3-digit integer): ")    
        if pid[0] != 'p' or len(pid) != 4:
            print("ERROR: pid is not valid, please try again.")
            validpid = False
        try:
            int(pid[1:4])
        except:
            print("ERROR: pid is not valid, please try again.")
            validpid = False
            
    if pidExists(cursor, pid):
        cursor.execute("SELECT mp.name, mp.birthYear \
                FROM moviePeople mp, casts c \
                WHERE mp.pid = c.pid AND c.pid = :pid", {"pid": pid})
        nameyear = cursor.fetchone()
        name, year = nameyear[0], nameyear[1]
        
        print("The cast member you chose is:\n\tName:", name, "\n\tBirthyear:", year)
        role = input("Type the role that this actor will play: ")
    
        cursor.execute("INSERT INTO casts VALUES (:mid, :pid, :role);", {"mid": mid, "pid": pid, "role": role})
        data.commit()
        
    
    else:
        choice = input("\nCast member does not exist. Would you like to insert a cast member and add him as part of the cast (y/n)? ")
        if choice.lower in ['n', 'no']:
            return
        else:
            addCast(cursor, data, mid)
            return



def askMid(cursor):
    '''Keeps prompting user for a valid mid until one is given.
    Args:
            None
    Returns:
            integer mid
    '''      
    
    validmid = False 
    while not validmid:  
        validmid = True 
        mid = input("Please provide a unique integer id for the movie: ")   
        try:
            mid = int(mid)
        except:
            validmid = False
            print("ERROR: mid is not valid, please try again.\n")
        else:
            validmid = not midExists(cursor, mid)    
    return mid



def askYear():
    '''Keeps prompting user for a valid year until one is given.
    Args:
            None
    Returns:
            integer year
    '''  
    
    validyear = False
    while not validyear:
        validyear = True
        year = input("\nPlease provide a year for the movie: ")      #Didn't give year time constraints because movie might be coming out in the future.
        try:
            year = int(year)
        except:
            print("ERROR: year must be an integer, please try again.")
            validyear = False
    return year       
        
            
       
def askRuntime():
    '''Keeps prompting user for a valid runtime until one is given.
    Args:
            None
    Returns:
            integer runtime
    '''          
    
    validruntime = False
    while not validruntime:
        validruntime = True
        runtime = input("\nPlease provide a runtime for the movie: ")      #Didn't give year time constraints because movie might be coming out in the future.
        try:
            runtime = int(runtime)
        except:
            print("ERROR: runtime must be an integer, please try again.")
            validruntime = False
    return runtime



def addMovie(cursor, data):
    '''Handles the functionality of adding movies to the database for editors.
    Args:
            None
    Returns:
            None
    '''     
    
    os.system('cls||clear')
    
    mid = askMid(cursor)     
    title = input("\nPlease provide a title for the movie: ") 
    year = askYear()
            
    validruntime = False
    while not validruntime:
        validruntime = True
        runtime = input("\nPlease provide a runtime for the movie: ")      #Didn't give year time constraints because movie might be coming out in the future.
        try:
            runtime = int(runtime)
        except:
            print("ERROR: runtime must be an integer, please try again.")
            validruntime = False
    
    print("Are you sure you want to add:\n\tMid:", str(mid), "\n\tTitle:", title, "\n\tYear:", str(year), "\n\truntime", str(runtime))
    choice = input("to the database (y/n)?: ")
    if choice.lower() in ['n', 'no']:
        return
    
    cursor.execute("INSERT INTO movies VALUES (:mid, :title, :year, :runtime);", {"mid": mid, "title": title, "year": year, "runtime": runtime})
    data.commit()
    
    askCast(cursor, data, mid)
    choice = input("\nAdd another cast member (y/n)? ")
    while True:
        if choice.lower() in ['y', 'yes']:
            askCast(cursor, data, mid)
            choice = input("\nAdd another cast member (y/n)? ")   
        elif choice.lower() in ['n', 'no']:
            break  
        else:
            print('ERROR: Invalid selection, please try again')
            choice = input("\nAdd another cast member (y/n)? ")
