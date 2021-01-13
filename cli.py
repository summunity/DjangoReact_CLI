"""
Diamond Cronjob
=================

Event Detection based on data stored in Diamond

:Author: Nik Sumikawa
:Date: Nov 3, 2020
"""


import logging
log = logging.getLogger(__name__)


import pandas as pd

from src.apps.interface import *
from src.git.interface import *

import os


class CLI:

    def __init__(self):
        self.state = 0
        self.active_threads = []

        path = os.path.dirname(os.path.realpath(__file__))
        self.config = pd.read_json('%s/config.json' % path)

        self.run()

    def run( self ):

        while True:

            try:
                if self.state == -1 : break
                if self.state == 0 : self.initial_state()

                if self.state == 1 :
                    self.state, app = launch_app(self.state, self.config)
                    if app != None: self.active_threads.append( app )

                if self.state == 2 : self.state = list_apps(self.state, self.active_threads)

                if self.state == 3 :
                    self.state, self.active_threads = kill_app(self.state, self.active_threads)


                if self.state == 4 :
                    self.state, app = git('pull', self.state, self.config)

                if self.state == 5 :
                    self.state, app = git('push', self.state, self.config)


            except KeyboardInterrupt:
                break


    def initial_state( self ):

        command_str = """
            What do you want to do:
            1: Launch app
            2: Active apps
            3: disable app
            4: Update project (git pull)
            5: Commit project (git push)
            q: quit
        """

        command_str = self.format_cmd_prompt(command_str)

        user_input = input(command_str)

        try : user_input = int(user_input)
        except:
            if user_input == 'q' or user_input == 'quit': self.state = -1
            else: print( 'Invalid Input : %s' % user_input)
            return

        if user_input >5:
            print( 'Invalid Input : %s' % user_input)
            return

        self.state = user_input


    # def launch_state( self ):
    #     """ launch app state """
    #
    #     command_str = """
    #         Which application do you want to launch:
    #     """
    #
    #     apps = self.config[self.config['launch'] == True]
    #     for i in range(0, len(apps)):
    #         app_name = apps.loc[i]['title']
    #         command_str += '%s: %s\n' % (i+1, app_name)
    #
    #     command_str += 'b: back\n'
    #
    #     command_str = self.format_cmd_prompt(command_str)
    #
    #     user_input = input(command_str)
    #
    #     try : user_input = int(user_input) - 1
    #     except:
    #         if user_input == 'b' or user_input == 'back': self.state = 0
    #         else: print( 'Invalid Input : %s' % user_input)
    #         return
    #
    #     # catch error when supplied value is greater than # of apps
    #     if user_input > len(apps) :
    #         print( 'Invalid Input : %s' % user_input)
    #         return
    #
    #     self.launch_app( apps.loc[user_input] )
    #
    #     # set the state to return to the main menu
    #     self.state = 0
    #
    #
    # def active_state( self ):
    #     """ prints a list of all active App threads """
    #
    #     command_str = """
    #         Active Apps:
    #     """
    #
    #     apps = self.config[self.config['launch'] == True]
    #     for i in range(0, len(self.active_threads)):
    #         app_name = self.active_threads[i].getName()
    #         command_str += '%s: %s\n' % (i+1, app_name)
    #
    #     # command_str += 'b: back\n'
    #
    #     command_str = self.format_cmd_prompt(command_str)
    #
    #     print( command_str )
    #
    #
    #     # set the state to return to the main menu
    #     self.state = 0
    #
    # def disable_state( self ):
    #     """ prints a list of all active App threads """
    #
    #     command_str = """
    #         Active Apps:
    #     """
    #
    #     apps = self.config[self.config['launch'] == True]
    #     for i in range(0, len(self.active_threads)):
    #         app_name = self.active_threads[i].getName()
    #         command_str += '%s: %s\n' % (i+1, app_name)
    #
    #     command_str += 'b: back\n'
    #
    #     command_str = self.format_cmd_prompt(command_str)
    #
    #     user_input = input(command_str)
    #
    #     try : user_input = int(user_input) - 1
    #     except:
    #         if user_input == 'b' or user_input == 'back': self.state = 0
    #         else: print( 'Invalid Input : %s' % user_input)
    #         return
    #
    #     # catch error when supplied value is greater than # of apps
    #     if user_input > len(apps) :
    #         print( 'Invalid Input : %s' % user_input)
    #         return
    #
    #     thread = self.active_threads.pop(user_input)
    #     thread.raise_exception()
    #
    #     # set the state to return to the main menu
    #     self.state = 0


    # def launch_app( self, app ):
    #     """ launch application """
    #
    #     from cmd_thread import CmdThread
    #
    #     if app['type'] == 'django':
    #         cmd = 'python manage.py runserver 0.0.0.0:%s' % app['port']
    #         thread = CmdThread(app, [cmd])
    #         thread.start()
    #         thread.setName('Launch-%s' % app['title'])
    #         self.active_threads.append( thread )
    #
    #     if app['type'] == 'react':
    #         cmd = 'npm run export PORT=%s react-scripts start' % app['port']
    #         # subprocess.call(cmd)
    #         # subprocess.check_output(cmd)
    #         print( cmd )


    def git_pull( self, app ):
        """ launch application """

        import subprocess
        import os
        from cmd_thread import CmdThread

        cmd = 'git pull'
        thread = CmdThread(app, [cmd])
        thread.start()
        thread.setName('Launch-%s' % app['title'])
        self.active_threads.append( thread )


    def git_push( self, app ):
        """ launch application """

        import subprocess
        import os
        from cmd_thread import CmdThread

        command_str = "Commit Message: \n"
        user_input = input(command_str)

        cmd = [
            'git add -A',
            'git commit -m %s' % user_input,
            'git push'
            ]

        thread = CmdThread(app, cmd)
        thread.start()
        thread.setName('Launch-%s' % app['title'])
        self.active_threads.append( thread )


    def format_cmd_prompt( self, cmd ):
        """ formats the command prompt """
        formatted = ''
        for line in cmd.split('\n'):
            formatted += line.lstrip() + '\n'
        return formatted



if __name__ == "__main__":

    # from django_config.logger import initialize_logging
    # initialize_logging()

    CLI()

    #
    # from cmd_thread import CmdThread
    # thread = CmdThread(
    #     {'path': 'C:/Users/nxa18331/Desktop/websites/bitbucket/restapi'},
    #     ['python manage.py runserver 0.0.0.0:8000']
    #     )
    #
    # thread.start()
    # #
    # #
    # while True:
    #
    #     try:
    #         var = input(""" What do you want to do?: """
    #         )
    #
    #         print( var )
    #         if var == 'q':
    #             print( 'do we raise exception??')
    #             thread.raise_exception()
    #
    #     except KeyboardInterrupt:
    #         break



    # Cronjob(timeframe=2, filter=False)

    #
    # Cronjob(mask='N06G', timeframe=7, filter=False)
    # Cronjob(
    #     backfill = True,
    #     start_date = '2020-11-01',
    #     stepsize=2 )
    # debug()

    # import argparse
    #
    # parser = argparse.ArgumentParser(description='Event Detection Cronjob - Diamond')
    # parser.add_argument(
    #     '--backfill',
    #     required=False,
    #     help='When True, the data is backfilled'
    #     )
    #
    # parser.add_argument(
    #     '--startdate',
    #     required=False,
    #     help='start of the backfill window in %Y-%m-%d format'
    #     )
    #
    # parser.add_argument(
    #     '--enddate',
    #     required=False,
    #     help='end of the backfill window in %Y-%m-%d format'
    #     )
    #
    # parser.add_argument(
    #     '--threads',
    #     required=False,
    #     help='number of threads to execute in parallel'
    #     )
    #
    #
    # args = parser.parse_args()
    #
    # if args.backfill  == 'True' :
    #     log.debug('Backfill')
    #
    #     # extract the startdate from command line. default to 30 day window
    #     startdate = args.startdate
    #     if startdate == None:
    #         from datetime import datetime, timedelta
    #         startdate = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    #
    #     # extract the startdate from command line. default to 30 day window
    #     enddate = args.enddate
    #     if enddate == None:
    #         from datetime import datetime, timedelta
    #         enddate = (datetime.now()).strftime('%Y-%m-%d')
    #
    #     kwargs = {
    #         'backfill': True,
    #         'start_date': startdate,
    #         'end_date': enddate,
    #         'stepsize': 1,
    #     }
    #
    #     threads = args.threads
    #     if threads != None: kwargs['threads'] = threads
    #
    #     Cronjob(**kwargs)
    #
    #
    # else:
    #     log.debug('Standard cronjob')
    #
    #     kwargs = {
    #         'filter': False,
    #         'timeframe': 1,
    #     }
    #
    #     threads = args.threads
    #     if threads != None: kwargs['threads'] = threads
    #
    #     Cronjob(**kwargs)


    # log.debug('finished....')
