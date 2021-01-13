
import threading
import time
import ctypes


class CmdThread(threading.Thread):

    def __init__(self, app, commands):
        threading.Thread.__init__(self)

        self.app = app
        self.commands = commands


    def run(self):

        import subprocess
        import os

        os.chdir(self.app['path'])

        # target function of the thread class
        try:
            for cmd in self.commands:
                subprocess.call(cmd)

        finally:
            print('ended')

        return

    # def get_id(self):
    #     if hasattr(self, '_thread_id'):
    #         return self._thread_id
    #
    def get_id( self ):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id


    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        print('what is this', res)
        if res >= 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
