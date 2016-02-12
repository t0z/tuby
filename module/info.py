try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import json

TUBY.stdout.write(json.dumps({  # @UndefinedVariable
    'for': 'tuby:0.1',
    'module': 'info',
    'version': '0.1',
    'desc': 'help for tuby',
    'data': {
        'help': ''
    }
}) + '\n')
