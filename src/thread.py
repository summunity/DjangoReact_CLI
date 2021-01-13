

from time import sleep

def launching_func( app, commands ):

    import os
    import subprocess

    os.chdir(app['path'])

    for cmd in commands:
        print( 'command', cmd)
        subprocess.call(cmd)
        sleep(1)



def launch_thread( app, commands ):

    import multiprocessing

    proc = multiprocessing.Process(
        target=launching_func,
        args=(app, commands))

    proc.name = app['title']
    proc.start()


    return proc
    # proc.terminate()

def kill_process( proc ):
    proc.terminate()
