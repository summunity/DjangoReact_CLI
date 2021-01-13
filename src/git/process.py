

from ..thread import launch_thread

def git_pull( app ):
    """ launch application """

    url = 'https://%s:%s@%s' % (
        app['username'],
        app['password'],
        app['git'],
    )

    cmd = 'git pull %s' % url

    return launch_thread(app, [cmd])


def git_push( app ):
    """ launch application """

    command_str = "Commit Message: \n"
    user_input = input(command_str)

    cmd = [
        'git config --global user.name "%s"' % app['username'],
        'git add -A',
        'git commit -m "%s"' % user_input,
        'git push'
        ]

    return launch_thread(app, cmd)
