import sys
import getopt
# import logging
from distutils.util import strtobool
sys.path.append('../')

from yt_concate.settings import VENV_PATH
sys.path.append(VENV_PATH)

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'  # supercar blondie


def print_usage():
    print('python main.py OPTIONS')
    print('OPTIONS:')
    print('{:>6} {:<16}{}'.format('-c', '--channel', '<str>: channel id for video downloading, must be assigned'))
    print('{:>6} {:<16}{}'.format('-s', '--search', '<str>: search word in the downloaded videos, must be assigned'))
    print('{:>6} {:<16}{}'.format('-l', '--limit', '<int>: limitation of the amount of the editing videos'))
    print('{:>6} {:<16}{}'.format('', '--cleanup', '<True/False>: remove downloads folders after editing'))
    print('{:>6} {:<16}{}'.format('', '--loglevel', '<DEBUG/INFO/WARNING/ERROR/CRITICAL>: level of logging function'))


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'cleanup': True,
        'log_level': 'WARNING'
    }

    short_opts = 'hc:s:l:'
    long_opts = 'help channel= search= limit= cleanup= loglevel='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--search'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            try:
                inputs['limit'] = int(arg)
            except ValueError:
                print_usage()
                sys.exit(2)
        elif opt == '--cleanup':
            try:
                inputs['cleanup'] = bool(strtobool(arg))
            except ValueError:
                print_usage()
                sys.exit(2)
        elif opt == 'loglevel':
            inputs['log_level'] = arg
            level = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if inputs['log_level'] not in level:
                print_usage()
                sys.exit(2)

    if not inputs['channel_id'] or not inputs['search_word']:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    #if utils.output_video_file_exists(inputs['channel_id'], inputs['search_word']):
    #    ans = input('Output video file for the channel and the search term already exists. \n Continue downloading captions and videos? (y/n)')

    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
