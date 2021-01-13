
def format_cmd_prompt( cmd ):
    """ formats the command prompt """
    formatted = ''
    for line in cmd.split('\n'):
        formatted += line.lstrip() + '\n'
    return formatted
