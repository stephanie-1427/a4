# state.py

# Error codes and input statements

# Module to control bulk of what is printed to the screen

# Purpose of this module is for maintainability and organization

# Stephanie Lee
# stephl25@uci.edu
# 79834162

# INPUT STATEMENTS
MAIN_MENU = '''\nWhat would you like to do?
 C: Create a file\n O: Open a file
 D: Delete a file\n R: Print a file
 E: Edit data from a file\n P: Print data from a file
 PUB: Publish a post/bio online'''
GUIDE = '''Things to note:
 > Numerical values must be entered as integers
 > Press "Q" to quit\n'''
INPUT_PATH = '\nEnter the directory (path) to create the file in (without quotes):\n'
INPUT_FILE_NAME = '\nEnter the name of the new file (without quotes):\n'
INPUT_OPTION = '\nOPTIONS:\n -n: name a new file\n\nEnter a valid option: '
INPUT_DELETE = '\nEnter the path of the file to DELETE (without quotes):\n'
INPUT_READ = '\nEnter the path of the file to READ (without quotes):\n'
INPUT_OPEN = '\nEnter the path of the file to OPEN (without quotes):\n'
INPUT_EDITS = '''\nEdit Menu:
U: edit username
P: edit password
B: edit bio
A: add a post
D: delete a post
E: exit editing mode
Enter an option: '''
INPUT_PRINT = '''\nPrint Menu
U: print username
P: print password
B: print bio
POST: print a post
POSTS: print all posts
A: print all info from the profile
E: exit printing mode
Enter an option: '''

# ERROR CODES:
DSU_PROFILE_ERROR = 'ERROR: Only .dsu files that follow Profile format supported'
DSU_FILE_ERROR = 'ERROR: In processing the DSU file, or invalid DSU file path or type.'
DSU_TYPE_ERROR = 'ERROR: Only .dsu file types are supported.'
INVALID_PATH = 'ERROR: Enter a valid path.'
FILE_DNE = 'ERROR: File does not exist.'
NO_FILE_LOADED = 'ERROR: No file has been loaded.'
QUOTATION_MISUSE = 'ERROR: Paths must be enclosed in quotations.'
INVALID_COMMAND = 'ERROR: Invalid command.'
INVLAID_OPTION = 'ERROR: An invalid option was entered. Terminating mode...'
INVALID_EDIT = 'ERROR: Entries with only whitespace or empty entries are not allowed.'
INT_ERROR = 'ERROR: An invalid int value was entered'
INVALID_INDEX = 'ERROR: An invalid index was entered.'
BAD_COMMAND_LINE = 'ERROR: Misuse of command line. Check argument count and quotations.'
UNDEFINED_ERROR = 'ERROR: Try block of main() in a2.py is triggering an Exception.'
MISSING_PROFILE_ATTRIBUTES = 'ERROR: Missing username and password; interrupt by "Q". File not created.'
