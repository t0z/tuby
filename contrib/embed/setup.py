from distutils.core import setup, Extension

module1 = Extension('emby',
                    define_macros=[('MAJOR_VERSION', '1'),
                                   ('MINOR_VERSION', '0')],
                    include_dirs=['/usr/include'],
                    libraries=['python2.7', 'ssl', 'curl'],
                    library_dirs=['.', '/usr/local/lib'],
                    sources=['main.c', 'http.c', 'text.c'])

setup(name='emby',
      version='1.0',
      description='tuby embeded',
      author='t0z',
      author_email='t0z',
      url='https://github.com/t0z/tuby',
      long_description='''pipe thing''',
      ext_modules=[module1])
