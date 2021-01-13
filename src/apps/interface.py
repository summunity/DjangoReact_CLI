
from ..format_cmd import format_cmd_prompt


def launch_app( state, config ):
    """ launch app state """

    command_str = """
        Which application do you want to launch:
    """

    from .process import launch_app as launch_process


    apps = config[config['launch'] == True]
    for i in range(0, len(apps)):
        app_name = apps.loc[i]['title']
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
    if user_input > len(apps) :
        print( 'Invalid Input : %s' % user_input)
        return state, None


    app = launch_process( apps.loc[user_input] )

    # set the state to return to the main menu
    state = 0

    return state, app


def list_apps( state, active_threads ):
    """ prints a list of all active App threads """

    command_str = """
        Active Apps:
    """

    for i in range(0, len(active_threads)):
        app_name = active_threads[i].name
        command_str += '%s: %s\n' % (i+1, app_name)


    command_str = format_cmd_prompt(command_str)

    print( command_str)

    # set the state to return to the main menu
    state = 0

    return state


def kill_app( state, active_threads ):
    """ prints a list of all active App threads """

    from ..thread import kill_process

    command_str = """
        Active Apps:
    """

    for i in range(0, len(active_threads)):
        app_name = active_threads[i].name
        command_str += '%s: %s\n' % (i+1, app_name)

    command_str += 'b: back\n'

    command_str = format_cmd_prompt(command_str)

    user_input = input(command_str)

    try : user_input = int(user_input) - 1
    except:
        if user_input == 'b' or user_input == 'back': state = 0
        else: print( 'Invalid Input : %s' % user_input)
        return state, active_threads

    # catch error when supplied value is greater than # of apps
    if user_input > len(active_threads) :
        print( 'Invalid Input : %s' % user_input)
        return state, active_threads

    proc = active_threads.pop(user_input)
    kill_process(proc)

    # set the state to return to the main menu
    state = 0

    return state, active_threads
