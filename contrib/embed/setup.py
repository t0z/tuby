from distutils.core import setup, Extension

module1 = Extension('emby',
                    define_macros=[('MAJOR_VERSION', '1'),
                                   ('MINOR_VERSION', '0')],
                    include_dirs=['/usr/include'],
                    libraries=['python2.7'],
                    library_dirs=['.', '/usr/local/lib'],
                    sources=['main.c'])

setup(name='emby',
      version='1.0',
      description='This is a demo package',
      author='t0z',
      author_email='t0z',
      url='https://docs.python.org/extending/building',
      long_description='''
This is really just a demo package.
''',
      ext_modules=[module1])
