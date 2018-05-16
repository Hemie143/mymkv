import os
import sys
from ctypes import *

if os.name == "nt" or os.name == "dos" or os.name == "os2" or os.name == "ce":
    _file = 'MediaInfo.dll'
    _path = os.path.abspath(os.path.join(os.path.dirname(__file__), _file))
    print(_path)
    # TODO: get _mod out of if-else
    DLL_Handler = CDLL(_path)
    MustUseAnsi = 0
elif sys.platform == "darwin":
    _file = 'libmediainfo.0.dylib'
    _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
    DLL_Handler = CDLL(_path)
    MustUseAnsi = 1
else:
    _file = 'libmediainfo.so.0'
    _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
    DLL_Handler = CDLL(_path)
    MustUseAnsi = 1


class Stream:
    General, Video, Audio, Text, Other, Image, Menu, Max = list(range(8))


class Info:
    Name, Text, Measure, Options, Name_Text, Measure_Text, Info, HowTo, Max = list(range(9))


class InfoOption:
    ShowInInform, Reserved, ShowInSupported, TypeOfValue, Max = list(range(5))


class FileOptions:
    Nothing, Recursive, CloseAll, xxNonexx_3, Max = list(range(5))


class MediaInfo:

    def __init__(self):
        mediainfo__new = DLL_Handler.MediaInfo_New
        mediainfo__new.argtypes = []
        mediainfo__new.restype = c_void_p   # int or None
        self._handle = mediainfo__new()
        self.option('CharSet', 'UTF-8')

    def open(self, mediafilename):
        self.mediafilename = mediafilename
        mediainfo_open = DLL_Handler.MediaInfo_Open
        mediainfo_open.argtypes = [c_void_p, c_wchar_p]     # int, string
        mediainfo_open.restype = c_size_t                   # int
        return mediainfo_open(self._handle, self.mediafilename)

    def get(self, StreamKind, StreamNumber, Parameter, InfoKind=Info.Text, SearchKind=Info.Name):
        mediainfo_get = DLL_Handler.MediaInfo_Get
        mediainfo_get.argtypes = [c_void_p, c_size_t, c_size_t, c_wchar_p, c_size_t, c_size_t]
        # int, int, int, string, int, int
        mediainfo_get.restype = c_wchar_p       # string
        return mediainfo_get(self._handle, StreamKind, StreamNumber, Parameter, InfoKind, SearchKind)

    def option(self, Option, Value=""):
        mediainfo_option = DLL_Handler.MediaInfo_Option
        mediainfo_option.argtypes = [c_void_p, c_wchar_p, c_wchar_p]    # int, string, string
        mediainfo_option.restype = c_wchar_p                            # string
        return mediainfo_option(self._handle, Option, Value)

    def close(self):
        # TODO: MediaInfo close
        pass



'''
print("Get with Stream=General and Parameter='FileSize'")
print(MI.Get(Stream.General, 0, "FileSize"))
'''


# test = MediaInfo('../FPS_test_1080.mkv')
# print(test._mod)


'''
General
Unique ID                                : 188981347969821827778605787854438640345 (0x8E2C7BD3AB7617ADBB3D933F32D7AAD9)
Complete name                            : F:\Development\mymkv\FPS_test_1080.mkv
Format                                   : Matroska
Format version                           : Version 4 / Version 2
File size                                : 15.8 MiB
Duration                                 : 10 min 5 s
Overall bit rate mode                    : Variable
Overall bit rate                         : 219 kb/s
Encoded date                             : UTC 2014-09-18 20:01:03
Writing application                      : mkvmerge v7.2.0 ('On Every Street') 32bit built on Sep 13 2014 15:42:11
Writing library                          : libebml v1.3.0 + libmatroska v1.4.1

Video
ID                                       : 1
Format                                   : AVC
Format/Info                              : Advanced Video Codec
Format profile                           : High@L4.1
Format settings                          : CABAC / 3 Ref Frames
Format settings, CABAC                   : Yes
Format settings, RefFrames               : 3 frames
Codec ID                                 : V_MPEG4/ISO/AVC
Duration                                 : 10 min 5 s
Bit rate mode                            : Variable
Bit rate                                 : 217 kb/s
Maximum bit rate                         : 40.0 Mb/s
Width                                    : 1 920 pixels
Height                                   : 1 080 pixels
Display aspect ratio                     : 16:9
Frame rate mode                          : Constant
Frame rate                               : 25.000 FPS
Color space                              : YUV
Chroma subsampling                       : 4:2:0
Bit depth                                : 8 bits
Scan type                                : Progressive
Bits/(Pixel*Frame)                       : 0.004
Stream size                              : 15.6 MiB (99%)
Writing library                          : x264 core 142 r2431 ac76440
Encoding settings                        : cabac=1 / ref=4 / deblock=1:-1:-1 / analyse=0x3:0x133 / me=umh / subme=10 / psy=1 / psy_rd=1.00:0.15 / mixed_ref=1 / me_range=24 / chroma_me=1 / trellis=2 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=1 / chroma_qp_offset=-3 / threads=6 / lookahead_threads=1 / sliced_threads=0 / slices=4 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=1 / constrained_intra=0 / bframes=3 / b_pyramid=1 / b_adapt=2 / b_bias=0 / direct=3 / weightb=1 / open_gop=1 / weightp=1 / keyint=25 / keyint_min=1 / scenecut=40 / intra_refresh=0 / rc_lookahead=25 / rc=crf / mbtree=1 / crf=18.0 / qcomp=0.60 / qpmin=0 / qpmax=69 / qpstep=4 / vbv_maxrate=40000 / vbv_bufsize=30000 / crf_max=0.0 / nal_hrd=vbr / filler=0 / ip_ratio=1.40 / aq=1:1.00
Language                                 : English
Default                                  : Yes
Forced                                   : No
Color range                              : Limited
Color primaries                          : BT.709
Transfer characteristics                 : BT.709
Matrix coefficients                      : BT.709

Audio
ID                                       : 2
Format                                   : MPEG Audio
Format version                           : Version 1
Format profile                           : Layer 3
Format settings                          : Joint stereo / MS Stereo
Codec ID                                 : A_MPEG/L3
Codec ID/Hint                            : MP3
Duration                                 : 1 s 56 ms
Bit rate mode                            : Variable
Bit rate                                 : 32.0 kb/s
Minimum bit rate                         : 32.0 kb/s
Channel(s)                               : 2 channels
Sampling rate                            : 48.0 kHz
Frame rate                               : 41.667 FPS (1152 SPF)
Compression mode                         : Lossy
Stream size                              : 4.03 KiB (0%)
Writing library                          : LAME3.99r
Encoding settings                        : -m j -V 1 -q 0 -lowpass 19.5 --vbr-new -b 32
Language                                 : English
Default                                  : Yes
Forced                                   : No
'''