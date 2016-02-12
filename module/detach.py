import sys
from multiprocessing import Process
try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()


def daemon(*a, **ka):
    from time import sleep
    while True:
        with open('foo.alive', 'wb') as fw:
            fw.write("I'm alive!\n")
        print('d')
        sleep(3)

process = Process(target=daemon)
process.daemon = False
TUBY.stdout.write('detaching')
process.start()

sys.exit(0)
