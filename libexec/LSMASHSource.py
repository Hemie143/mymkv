import os
import sys
from ctypes import *

if os.name == "nt" or os.name == "dos" or os.name == "os2" or os.name == "ce":
    _file = 'LSMASHSource.dll'
    _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
    print(_path)
    DLL_Handler = CDLL(_path)


class LSMASHSource:

    def __init__(self):
        return

    def open(self, mediafilename):
        self.mediafilename = mediafilename
        mediainfo_open = DLL_Handler.MediaInfo_Open
        mediainfo_open.argtypes = [c_void_p, c_wchar_p]  # int, string
        mediainfo_open.restype = c_size_t  # int
        return mediainfo_open(self._handle, self.mediafilename)

    @staticmethod
    def LWLibavVideoSource(source):
        """
                    LWLibavVideoSource(string source, int stream_index = -1, int threads = 0, bool cache = true,
                               int seek_mode = 0, int seek_threshold = 10, bool dr = false,
                               int fpsnum = 0, int fpsden = 1, bool repeat = false, int dominance = 0,
                               bool stacked = false, string format = "", string decoder = "")
                * This function uses libavcodec as video decoder and libavformat as demuxer.

        :return:
        """
        libav_video = DLL_Handler.LWLibavVideoSource
        libav_video.argtypes = c_wchar_p  # int, string
        libav_video.restype = c_size_t  # int
        return libav_video(source)

