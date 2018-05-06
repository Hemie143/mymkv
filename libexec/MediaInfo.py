import os
import sys
from ctypes import *


class Stream:
    General, Video, Audio, Text, Other, Image, Menu, Max = list(range(8))


class Info:
    Name, Text, Measure, Options, Name_Text, Measure_Text, Info, HowTo, Max = list(range(9))


class InfoOption:
    ShowInInform, Reserved, ShowInSupported, TypeOfValue, Max = list(range(5))


class FileOptions:
    Nothing, Recursive, CloseAll, xxNonexx_3, Max = list(range(5))


class MediaInfo:

    def __init__(self, mkvfilename):
        self.mkvfilename = mkvfilename

        if os.name == "nt" or os.name == "dos" or os.name == "os2" or os.name == "ce":
            _file = 'MediaInfo.dll'
            self._path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
            print(self._path)
            # TODO: get _mod out of if-else
            MediaInfoDLL_Handler = CDLL(self._path)
            #self._mod = cdll.LoadLibary(_path)
            self._mod = CDLL(self._path)
            # MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 0
        elif sys.platform == "darwin":
            _file = 'libmediainfo.0.dylib'
            self._path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
            # TODO : use _mod ?
            MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 1
        else:
            _file = 'libmediainfo.so.0'
            self._path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
            # TODO : use _mod ?
            MediaInfoDLL_Handler = CDLL(_path)
            MustUseAnsi = 1

        MediaInfo_New = self._mod.MediaInfo_New
        MediaInfo_New.argtypes = []
        MediaInfo_New.restype = c_void_p

        self._handle = MediaInfo_New()
        print('handle: {}'.format(self._handle))



    def Open(self, filename=None):
        # self.Handle = MediaInfo_New

        if filename:
            print('Open has been provided a filename')

        MediaInfo_Open = self._mod.MediaInfo_Open
        MediaInfo_Open.argtypes = [c_void_p, c_wchar_p]
        MediaInfo_Open.restype = c_size_t
        return MediaInfo_Open(self._handle, self._path)

    def Get(self, StreamKind, StreamNumber, Parameter, InfoKind=Info.Text, SearchKind=Info.Name):
        MediaInfo_Get = self._mod.MediaInfo_Get
        MediaInfo_Get.argtypes = [c_void_p, c_size_t, c_size_t, c_wchar_p, c_size_t, c_size_t]
        MediaInfo_Get.restype = c_wchar_p

        return MediaInfo_Get(self._handle, StreamKind, StreamNumber, Parameter, InfoKind, SearchKind)

'''
print("Get with Stream=General and Parameter='FileSize'")
print(MI.Get(Stream.General, 0, "FileSize"))
'''


# test = MediaInfo('../FPS_test_1080.mkv')
# print(test._mod)