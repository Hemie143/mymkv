import os
import sys
from ctypes import *

class MediaInfo:

    def __init__(self, filename):
        self.filename = filename

        if os.name == "nt" or os.name == "dos" or os.name == "os2" or os.name == "ce":
            _file = 'MediaInfo.dll'
            _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
            print(_path)
            print(libname)
            # TODO: get _mod out of if-else
            MediaInfoDLL_Handler = CDLL(_path)
            #self._mod = cdll.LoadLibary(_path)
            self._mod = CDLL(_path)
            # MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 0
        elif sys.platform == "darwin":
            _file = 'libmediainfo.0.dylib'
            _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
            # TODO : use _mod ?
            MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 1
        else:
            _file = 'libmediainfo.so.0'
            _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
            # TODO : use _mod ?
            MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 1

    def open(self):

        MediaInfo_New = self._mod.MediaInfo_New
        MediaInfo_New.argtypes = []
        MediaInfo_New.restype = c_void_p

        self.Handle = MediaInfo_New

        MediaInfo_Open = self._mod.MediaInfo_Open
        MediaInfo_Open.argtypes = [c_void_p, c_wchar_p]
        MediaInfo_Open.restype = c_size_t
        return self._mod.MediaInfo_Open(self.Handle, self._path)

'''
print("Get with Stream=General and Parameter='FileSize'")
print(MI.Get(Stream.General, 0, "FileSize"))
'''


# test = MediaInfo('../FPS_test_1080.mkv')
# print(test._mod)