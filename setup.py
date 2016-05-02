#!/usr/bin/env python

from distutils.core import setup

from distutils.core import setup, Extension

# Router extension module
extension_mod = Extension("AlljoynRouter",
                           define_macros = [('QCC_OS_GROUP_POSIX', '1')],
                           sources = ["AllJoynPy/Router.c"],
                           libraries = ['alljoyn', 'ajrouter'])

setup(name='AllJoynPy',
      version='1.0',
      description='Python AllJoyn Wrapper',
      author='Glenn Pierce',
      author_email='glennpierce@gmail.com',
      url='https://github.com/glennpierce/alljoyn_python',
      ext_modules=[extension_mod],
      packages = ['AllJoynPy'],
     )
