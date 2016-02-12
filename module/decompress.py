TUBY = TUBY  # @UndefinedVariable
TUBY['__version__'] = '0.0.1'

import zlib

TUBY['stdout'].write(zlib.decompress(''.join([l for l in TUBY['stdin']])))
