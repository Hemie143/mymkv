import sys
import os.path
import subprocess
import re
import progress
from libexec.MediaInfo import *
from libexec.LSMASHSource import *

class VideoMKV:

    def __init__(self, mkvfilename):
        self.mkvfilename = mkvfilename
        self.mkvfolder = os.path.dirname(mkvfilename)
        self.mediainfo = MediaInfo()
        self.mediainfo.open(mkvfilename)
        self.filesize = int(self.mediainfo.get(Stream.General, 0, 'FileSize'))
        self.videocount = int(self.mediainfo.get(Stream.General, 0, 'VideoCount'))
        self.audiocount = int(self.mediainfo.get(Stream.General, 0, 'AudioCount'))
        self.duration = float(self.mediainfo.get(Stream.General, 0, 'Duration'))

        self.avsfilename = '{}.avs'.format(os.path.splitext(self.mkvfilename)[0])
        self.libexecfolder = os.path.join(os.path.dirname(__file__), 'libexec')
        # Video
        # self.framerate = float(self.mediainfo.get(Stream.General, 0, 'Framerate'))
        # self.framecount = int(self.mediainfo.get(Stream.General, 0, 'FrameCount'))

        # Audio
        self.audio = {}
        self.audio['streamcount'] = int(self.mediainfo.get(Stream.Audio, 0, 'StreamCount'))
        self.audio['id'] = int(self.mediainfo.get(Stream.Audio, 0, 'ID'))
        self.audio['streamorder'] = int(self.mediainfo.get(Stream.Audio, 0, 'StreamOrder'))

        # self.mediainfo.Option_Static("Complete", "1")
        # self.info = self.mediainfo.Inform()

    def createAVS(self):
        with open(self.avsfilename, 'wt') as f:
            lsmash_dllfile = os.path.join(self.libexecfolder, 'LSMASHSource.dll')
            f.write('LoadPlugin("{}")\n'.format(lsmash_dllfile))
            f.write('LWLibavVideoSource("{}")\n'.format(self.mkvfilename))
            # NO resize for now
            # LanczosResize(1280,548)

    def extractAudio(self):
        # https://mkvtoolnix.download/doc/mkvextract.html
        # Assumes there is one audio track only, format is DTS and language is en
        toolfile = os.path.join(self.libexecfolder, 'mkvextract.exe')
        audiofile = '{}.dts'.format(os.path.splitext(self.mkvfilename)[0])
        cmd = [toolfile, self.mkvfilename, 'tracks', '{}:{}'.format(self.audio['id'] - 1, audiofile)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        bar = progress.ProgressBar('Extracting DTS: [{progress}] {percentage:.2f}%', width=50)
        bar.show()
        while True:
            output = process.stdout.readline()
            if output == '':
                    break
            if output and output.startswith('Progress'):
                # print(output.strip())
                r = re.match('Progress: (\d+)%', output)
                if r:
                    perc = int(r.group(1))
                    bar.reset()
                    bar.update(perc)
                    bar.show()


        rc = process.poll()
        return rc
        '''
        "E:\DVD\tools\megui\tools\mkvmerge\mkvextract.exe" tracks "E:\Videos\Movies\Toni.Erdmann.2016.720p.BluRay.x264-SADPANDA-Obfuscated\218554260e274868a8d1c6976ca27b0f.mkv" --ui-language en 1:"E:\Videos\Movies\Toni.Erdmann.2016.720p.BluRay.x264-SADPANDA-Obfuscated\218554260e274868a8d1c6976ca27b0f - [0] German.dts"
        "E:\DVD\tools\megui\tools\mkvmerge\mkvextract.exe" tracks "E:\Videos\Movies\Star.Trek.I.The.Motion.Picture.1979.MULTi.1080p.BluRay.x264-UKDHD\star.trek.the.motion.picture.1979.multi.1080p.bluray.x264-ukdhd.mkv" --ui-language en 1:"E:\Videos\Movies\Star.Trek.I.The.Motion.Picture.1979.MULTi.1080p.BluRay.x264-UKDHD\star.trek.the.motion.picture.1979.multi.1080p.bluray.x264-ukdhd - [0] French.ac3" 2:"E:\Videos\Movies\Star.Trek.I.The.Motion.Picture.1979.MULTi.1080p.BluRay.x264-UKDHD\star.trek.the.motion.picture.1979.multi.1080p.bluray.x264-ukdhd - [1] English.ac3"
        "E:\DVD\tools\megui\tools\mkvmerge\mkvextract.exe" "E:\Videos\Movies\Test\61b1800dc4794b6aa9a164a1e76cd4f4.mkv" tracks 1:"E:\Videos\Movies\Test\61b1800dc4794b6aa9a164a1e76cd4f4 - [0] English.dts" --ui-language en
        '''

    def LWI_index(filename):
        return LSMASHSource.LWLibavVideoSource(filename)


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description='Encode my MKV')
    parser.add_argument('-f', dest='filename', action='store')
    options = parser.parse_args(args)
    print(options.filename)
    if not os.path.isfile(options.filename):
        print('File does not exist')
        exit(1)
    mkv_input = VideoMKV(options.filename)      # Initialize
    print(mkv_input.audio)

    # Create AviSynth file
    mkv_input.createAVS()
    # Extract audio if DTS
    mkv_input.extractAudio()
    # Create LWI LSmash Index
    mkv_input.LWI_index(options.filename)

    # Convert DTS to AC3
    # mediainfo test = knowit.know(options.filename, {'provider': 'mediainfo'})
    # print(test)
    # main(args.filename)

    '''
    1. Create AVS & LWSMASH index
    2. Extract Audio (handle case of multiple tracks) if not AC3
    3. Convert Audio to AC3
    4. Re-encode Video to size of 4480MB or multiple of 1120MB (combined with Audio) - Compute arguments
    5. Mux files
    '''


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
