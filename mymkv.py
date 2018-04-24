import sys
import os.path
# import knowit
import libexec.MediaInfoDLL3 as mediainfo

class videoMKV:

    def __init__(self, mkvfilename):
        self.mkvfilename = mkvfilename
        self.mkvfolder = os.path.dirname(mkvfilename)
        self.mediainfo = mediainfo.MediaInfo()
        self.mediainfo.Open(mkvfilename)
        self.mediainfo.Option_Static("Complete", "1")
        self.info = self.mediainfo.Inform()


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description='Encode my MKV')
    parser.add_argument('-f', dest='filename', action='store')
    options = parser.parse_args(args)
    print(options.filename)
    if not os.path.isfile(options.filename):
        print('File does not exist')
        exit(1)
    mkv_input = videoMKV(options.filename)      # Initialize
    print(mkv_input.info)

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
