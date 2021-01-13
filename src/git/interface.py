
from ..format_cmd import format_cmd_prompt
from .process import *

def git( type, state, config ):
    """ launch app state """

    command_str = """
        Which application do you want to pull:
    """



    for i in range(0, len(config)):
        app_name = config.loc[i]['title']
        command_str += '%s: %s\n' % (i+1, app_name)

    command_str += 'b: back\n'

    command_str = format_cmd_prompt(command_str)

    user_input = input(command_str)

    try : user_input = int(user_input) - 1
    except:
        if user_input == 'b' or user_input == 'back': state = 0
        else: print( 'Invalid Input : %s' % user_input)
        return state, None

    # catch error when supplied value is greater than # of apps
    if user_input > len(config) :
        print( 'Invalid Input : %s' % user_input)
        return state, None

    if type == 'pull':
        app = git_pull( config.loc[user_input] )

    elif type == 'push':
        app = git_push( config.loc[user_input] )

    else:
        print( 'Invalid type : %s' % type)
        return state, None

    # set the state to return to the main menu
    state = 0

    return state, app
