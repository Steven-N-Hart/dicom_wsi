* LibVIPS

`OSError: cannot load library 'libvips-42.dll': error 0x7e.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'libvips-42.dll`
 * Make sure this file is in your PATH. If you have to, try:

.. highlight:: python

vipshome = 'D:\\Downloads\\vips-dev-w64-all-8.8.3\\vips-dev-8.8\\bin'
# set PATH
import os
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
# and now pyvips will pick up the DLLs in the vips area
import pyvips



