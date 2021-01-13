

from time import sleep

def TestFunction( test1, test2 ):
    print( 'these are the props', test1, test2)

    while True:
        print( 'we are looping' )
        sleep(1)
    return



if __name__ == "__main__":

    import multiprocessing
    proc = multiprocessing.Process(target=TestFunction, args=({'test':1, 'test2':2}))

    proc.name = 'proc 1'
    proc.start()


    sleep(5)
    print( proc.name)
    # Terminate the process
    proc.terminate()  # sends a SIGTERM

    while True:

        try:
            var = input(""" What do you want to do?: """
            )

            print( var )
            if var == 'q':
                print( 'do we raise exception??')
                thread.raise_exception()

        except KeyboardInterrupt:
            break



    print( 'finished')
