import logging
import time
from concurrent import futures

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR

logger = logging.getLogger(__name__)

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        yt_set = set([found.yt for found in data])
        print('videos to download =', len(yt_set))

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            for yt in yt_set:
                if utils.video_file_exists(yt):
                    logger.info(f'found existing video file for {yt.url}, skipping')
                    continue
                executor.submit(self.download_videos, yt.url, yt.id)
        end = time.time()
        print(f'video downloading elapsed time = {end-start} seconds')
        return data

    @staticmethod
    def download_videos(url, film_id):
        logger.info('downloading', url)
        YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=film_id + '.mp4')
