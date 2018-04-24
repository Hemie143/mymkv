import os
import sys
from ctypes import *

if os.name == "nt" or os.name == "dos" or os.name == "os2" or os.name == "ce":
    _file = 'MediaInfo.dll'
    _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
    _mod = ctypes.cdll.LoadLibary(_path)
    # MediaInfoDLL_Handler = CDLL(_path)
    MustUseAnsi = 0
elif sys.platform == "darwin":
    _file = 'libmediainfo.0.dylib'
    _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
    MediaInfoDLL_Handler = CDLL(_path)
    MustUseAnsi = 1
else:
    _file = 'libmediainfo.so.0'
    _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
    MediaInfoDLL_Handler = CDLL(_path)
    MustUseAnsi = 1


class MediaInfo:

    open = _mod.Open
    open.argtypes = ()
