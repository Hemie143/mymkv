import libexec.MediaInfo as MediaInfo


test1 = MediaInfo.MediaInfo()


print(test1.open('FPS_test_1080.mkv'))

print(test1.get(0, 0, "UniqueID"))
print(test1.get(0, 0, "Encoded_Date"))


'''
MI = MediaInfo()
    def __init__(self):
        self.Handle=self.MediaInfo_New()
        self.MediaInfo_Option(self.Handle, "CharSet", "UTF-8")


MI.Open("Example.ogg")
    def Open(self, File):
        if MustUseAnsi:
            return self.MediaInfoA_Open (self.Handle, File.encode("utf-8"));
        else:
            return self.MediaInfo_Open (self.Handle, File);


MI.Option_Static("Complete")
print(MI.Inform())

print(MI.Get(Stream.General, 0, "FileSize"))
    def Get(self, StreamKind, StreamNumber, Parameter, InfoKind=Info.Text, SearchKind=Info.Name):
        if MustUseAnsi:
            return self.MediaInfoA_Get(self.Handle, StreamKind, StreamNumber, Parameter.encode("utf-8"), InfoKind, SearchKind).decode("utf_8", 'ignore')
        else:
            return self.MediaInfo_Get(self.Handle, StreamKind, StreamNumber, Parameter, InfoKind, SearchKind)

MI.Close()
    def Close(self):
        return self.MediaInfo_Close(self.Handle)


'''