from os import path as Path
from flask import Flask
from tuby.core import modpath, readfile, basepath
import base64
import binascii
import ast
from tuby.mini import mini

debug = True
app = Flask(__name__)
methods = ['GET', 'POST']


class Err(object):

    file_not_found = ('File not found', 404)


@app.route("/<modname>", methods=methods)
def serv_module(modname):
    modname = modname.decode('utf8').strip().replace(u'.', u'_')
    print modname
    for storepath in [modpath, Path.join(basepath, Path.pardir, 'smodule')]:
        path = Path.join(storepath, u'%s.py' % modname)
        # print('path: %s' % path)
        if not Path.exists(path):
            continue
        return mini(readfile(path))
    return Err.file_not_found

if __name__ == "__main__":
    app.run(debug=debug)
