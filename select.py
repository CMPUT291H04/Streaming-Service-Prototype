import	sqlite3
import os


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
    
    
    print('You are now in \"' + selectedtitle + '\'s\" ' + 'movie screen, please select one of the following:\n[1]Follow a member of the cast\n[2]Watch movie\n')
    mchoice = input('Please type choice here: ')    
    while mchoice not in ['1', '2']:
        os.system('cls||clear')
        print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number.\n')
        print('You are now in \"' + selectedtitle + '\'s\" ' + 'movie screen, please select one of the following:\n[1]Follow a member of the cast\n[2]Watch movie\n')
        mchoice = input('Please type choice here: ')
    
    if mchoice == '1':
        os.system('cls||clear')
        followCastMenu(movies, selection, cursor, data, cid)
    
    else:
        
        if sid == None:
            print("\nERROR: You can't watch a movie without starting a session first. Please start a session and attempt this action again.")
            input('\nPress enter to return...')
        
        else:
            pass
              
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
    choice = -1
    while choice not in range(len(matches)):
        
        print('Search has returned', len(matches), 'results.\n')
        
        for i in range(len(matches)):
            print(str(i+1) + '. ' + matches[i][0], '| Year: ' + str(matches[i][1]), '| Runtime: ' + str(matches[i][2]) + ' minutes')             
        
        choice = input('\nPlease choose a movie by typing its corresponding number: ')
        os.system('cls||clear')
        try:
                choice = int(choice) - 1
        except:
            print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')   #If choice is a non-valid string.
        else:
            if choice not in range(len(matches)):
                print('ERROR: Invalid selection, please try again and make sure you type just the corresponding number or scroll letter.\n')    #If choice is a non-valid integer.              
    
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
    sorted_values_list = []
    sorted_values = sorted(hitDict.values(), reverse=True)
    for value in sorted_values:
        for key in hitDict.keys():
            if hitDict.get(key, 0) == value:
                sorted_values_list.append(key)
                hitDict.pop(key)
                break
    
    return sorted_values_list



def searchWordsMenu(cursor):
    '''Searches for specified data from a given database based on user-inputted keywords.
        Args:
            None.
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



def searchMovies(cursor, data, cid, sid):
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

