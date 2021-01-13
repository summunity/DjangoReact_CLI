
from ..thread import launch_thread


def launch_app( app ):
    """ launch application """

    if app['type'] == 'django':
        cmd = 'python manage.py runserver 0.0.0.0:%s' % app['port']
        return launch_thread(app, [cmd])


    if app['type'] == 'react':
        cmd = 'npm run export PORT=%s react-scripts start' % app['port']
        # subprocess.call(cmd)
        # subprocess.check_output(cmd)
        print( cmd )
