

# Simple custom functions to save and load the workspace in Python
# using pickle.

# Based on
# https://stackoverflow.com/questions/2960864/how-to-save-all-the-variables-in-the-current-python-session
# but modified to use pickle instead of shelve, as shelve seems to be leading to errors on my mac, see also
# https://github.com/dedupeio/csvdedupe/issues/67

# Let's do it with pickle now
import pickle
import os

storedir = '/Users/m.wehrens/Desktop/Workspace2024/'

def save_workspace(storedir, names_of_spaces_to_save, dict_of_values_to_save):
    '''
        filename = location to save workspace.
        names_of_spaces_to_save = use dir() from parent to save all variables in previous scope.
            -dir() = return the list of names in the current local scope
        dict_of_values_to_save = use globals() or locals() to save all variables.
            -globals() = Return a dictionary representing the current global symbol table.
            This is always the dictionary of the current module (inside a function or method,
            this is the module where it is defined, not the module from which it is called).
            -locals() = Update and return a dictionary representing the current local symbol table.
            Free variables are returned by locals() when it is called in function blocks, but not in class blocks.

        Example of globals and dir():
            >>> x = 3 #note variable value and name bellow
            >>> globals()
            {'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', 'x': 3, '__doc__': None, '__package__': None}
            >>> dir()
            ['__builtins__', '__doc__', '__name__', '__package__', 'x']
    '''
    
    for key, value in dict_of_values_to_save.items():
        filename = storedir + key + '.pickle'
        
        if isinstance(value, (type(np), type(lambda: None))) or key.startswith('__'):
            print('Skipping saving: {0}'.format(key))
            continue
        
        try:
            with open(filename, 'wb') as file:
                pickle.dump(value, file)
            print('Saved: {0}'.format(key))
        except:
            print('Failed saving: {0}'.format(key))
            os.remove(filename)
            
    print('Done.')
    

def load_workspace(storedir, parent_globals):
    '''
        filename = location to load workspace.
        parent_globals use globals() to load the workspace saved in filename to current scope.
    '''
    dict_of_values_to_load = {}

    for file in os.listdir(storedir): # file=os.listdir(storedir)[0]
        if file.endswith(".pickle"):
            filename = os.path.join(storedir, file)
            try:
                with open(filename, 'rb') as f: # f=open(filename, 'rb')
                    value = pickle.load(f)
                    key = file.split("/")[-1].split(".")[0]
                    dict_of_values_to_load[key] = value
                    print('Loaded: {0}'.format(key))
            except:
                print('Failed loading: {0}'.format(key))

    parent_globals.update(dict_of_values_to_load)

# Example:
if False:
    MYSTOREDIR = '/Users/m.wehrens/Desktop/Workspace2024/'
    save_workspace(MYSTOREDIR, dir(), globals())
    load_workspace(MYSTOREDIR, globals())
