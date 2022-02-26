import	sqlite3
import os

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


def searchWords(cursor):
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
            cursor.execute("SELECT DISTINCT title, year, runtime \
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
        choice = -1
    
    elif len(matches) <= 5:    
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
    
    else:
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


def searchMovies(cursor):
    os.system('cls||clear')
    hits_count = searchWords(cursor)
    os.system('cls||clear')
    movie_selected = displayMatches(hits_count)
    return

