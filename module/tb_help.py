try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

TUBY.stdout.write('''
  ____  ____  ___________  ____  ____  _______  ___  ___  ____  ____  
 ))_ ")))_ ")("     _   ")("  _||_ " ||   _  "\|"  \/"  |))_ ")))_ ") 
(____((____(  )__/  \\__/ |   (  ) : |(. |_)  :)\   \  /(____((____(  
 _____ _____     \\_ /    (:  |  | . )|:     \/  \\  \/  _____ _____  
 ))_ ")))_ ")    |.  |     \\ \__/ // (|  _  \\  /   /   ))_ ")))_ ") 
(____((____(     \:  |     /\\ __ //\ |: |_)  :)/   /   (____((____(  
                  \__|    (__________)(_______/|___/                  
                                                    t0z@2016
    tuby module pipe stdin to stdout

    syntax: tuby <module> [file|-] [module parameters]

    ```
    URL="https://raw.githubusercontent.com/t0z/tuby/master/README.md"
    tuby get - $URL | tuby hash - sha256
    ```
    > 5aafcedf8b8f61c27826dccb84b59896e8288d8c16cd70a736a85b936e427b46

    ```
    toby pcap | tee out.pcap | toby pcap-filter
    ```
''')
