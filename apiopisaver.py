from RPi import GPIO
import os
import time
import types
import getpass


class ApioPiSaver:

    def __init__(self, shutdown_time=3, custom_function=None):
        '''Class to check the Apio Pi Saver status
        The main function are:
        - check()
        - run()
        - shutdown()
        - close()
        '''
        if not isinstance(shutdown_time, int) and \
           not isinstance(shutdown_time, float):
            raise TypeError("inappropiate shutdown_time value type,"
                            "it must be int or float.")

        if not 30 > shutdown_time >= 0:
            raise ValueError("shutdown_time must be bethween 0 and 30.")

        if custom_function is None:
            custom_function = lambda: None
        else:
            if not isinstance(custom_function, types.FunctionType):
                raise TypeError("inappropiate custom_function value type,"
                                "it must be a function or `None`.")

        self.shutdown_time = shutdown_time
        self.custom_function = custom_function

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(23, GPIO.IN)

        GPIO.output(22, GPIO.HIGH)

    def shutdown(self):
        '''Shutdown the Raspberry Pi
        '''
        print("{WARNING}Shutdowning...{ENDC}".format(
            WARNING='\033[93m', ENDC='\033[0m'))
        time.sleep(self.shutdown_time)
        if not self.check():
            try:
                self.custom_function()
            except:
                pass
            GPIO.output(22, GPIO.LOW)
            os.system("shutdown -h now")

    def check(self):
        '''Check input status of the Apio Pi Saver pin
        '''
        return GPIO.input(23)

    def run(self):
        '''Run a loop that check the input status of the Apio Pi Saver and \
 if the Apio Pi Saver does not receive power input, shutdown the Raspberry Pi
        '''
        while True:
            if not self.check():
                self.shutdown()

    def close(self):
        '''Clean up by resetting all GPIO channels
        '''
        GPIO.cleanup()


if __name__ == '__main__':
    if getpass.getuser() == 'root':
        apio = ApioPiSaver(
            shutdown_time=1,
            custom_function=lambda: print("Shutdowing Raspberry Pi..."))
        print("{OKGREEN}Starting...{ENDC}".format(
            OKGREEN='\033[92m', ENDC='\033[0m'))
        try:
            apio.run()
        except:
            apio.close()
    else:
        print(
            "{FAIL}ERROR: "
            "{WARNING}You {UNDERLINE}must{ENDC}{WARNING} start this script with"
            "{BOLD}root{ENDC}{WARNING} permissions!!{ENDC}".format(
                FAIL='\033[91m', WARNING='\033[93m', UNDERLINE='\033[4m',
                BOLD='\033[1m', ENDC='\033[0m'
            )
        )
