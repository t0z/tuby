import os
from os.path import expanduser, abspath
from multiprocessing import Pool, Queue, Process, Event, Value
from multiprocessing.queues import Empty
from random import randint
from time import sleep, time

try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()


DEBUG = True
lf = '\n'
__numproc_resolve__ = 3


def clean_word(word):
    pos = len(word) - 1
    if word[pos] in [':', '=']:
        word = word[0:pos]
        pos -= 1
    for o, e in (('[', ']'), ('(', ')'), ('{', '}'), ('<', '>')):
        if word[0] == o and word[pos] == e:
            word = word[1, pos]
            pos -= 1
    return word.strip()


def readfile(path, filename):
    global result, stat_files
    aw = {}
    stat_files.value += 1

    try:
        with open(os.path.join(path, filename), 'rb') as fh:
            lw = None
            for line in fh:
                for word in line.split():
                    word = clean_word(word.strip().encode('utf8',
                                                          errors='replace'))
                    lw = len(word)
                    if lw < 3 or lw > 8:
                        continue
                    try:
                        if word in aw:
                            aw[word] += 1
                        else:
                            aw[word] = 1
                    except Exception:
                        TUBY.log(u'Error word: %s', word)
    except Exception as e:
        TUBY.log(u'Exception: %s', e)
    for k in aw.keys():
        TUBY.stdout.write(str(aw[k]) + u' ' + k + '\n')


def resolve():
    global alive
    retry = 3
    while alive.is_set():
        try:
            readfile(*queue.get(True, 1))
            retry = 3
        except Empty:
            retry -= 1
            if retry < 0:
                break


def fill(dirin):
    global queue
    dirin = abspath(expanduser(dirin))
    for dirpath, _dirnames, filenames in os.walk(dirin):
        for fn in filenames:
            queue.put((dirpath, fn))


def genpid(size=8):
    return ''.join([str(randint(0, 9)) for _n in range(0, size)])


def itstime(timeout=5):
    started_on = time()

    def wakeup(reset=False):
        if reset:
            reset = False
            started_on = time()
        if time() - timeout > started_on:
            return True
        return False
    return wakeup

"""Main
"""
pool = Pool()
queue = Queue()
alive = Event()
alive.set()
count = 0
done = 0
process = []
started_on = time()
stat_files = Value('i', 0)

"""Listing file to read"""
for dirin in TUBY.stdin:
    TUBY.log(u'+ input directory: %s', dirin.strip())
    p = Process(target=fill, args=(dirin.strip(),))
    p.daemon = False
    p.start()
    process.append(p)
    fill(dirin)

sleep(0.1)

"""Reading files"""
for _i in range(0, __numproc_resolve__):
    p = Process(target=resolve)
    p.daemon = False
    p.start()
    process.append(p)

"""Join our processes"""
[p.join() for p in process]
