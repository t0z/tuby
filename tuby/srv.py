from os import path as Path
from flask import Flask
from tuby.core import modpath, readfile
import base64
import binascii
import ast

debug = True
app = Flask(__name__)
methods = ['GET', 'POST']


class Err(object):

    file_not_found = ('File not found', 404)


@app.route("/<modname>", methods=methods)
def serv_module(modname):
    path = Path.join(modpath, '%s.py' % modname)
    # print('path: %s' % path)
    if not Path.exists(path):
        return Err.file_not_found
    tree = ast.parse(readfile(path))
    code = compile(tree, filename='<ast>', mode='exec')
    # return 'foo: %s' % type(txt), 200
    return base64.b64encode(code.co_code), 200

if __name__ == "__main__":
    app.run(debug=debug)
