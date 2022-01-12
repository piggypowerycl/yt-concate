from concurrent import futures
import time

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        yt_set = set([found.yt for found in data])
        print('videos to download=', len(yt_set))

        with futures.ThreadPoolExecutor(max_workers=30) as executor:
            for yt in yt_set:
                if utils.video_file_exists(yt):
                    print(f'found existing video file for {yt.url}, skipping')
                    continue
                executor.submit(self.download_videos, yt.url, yt.id)
        end = time.time()
        print(f'Elapsed time = {end-start} seconds')
        return data

    def download_videos(self, url, film_id):
        print('downloading', url)
        YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=film_id + '.mp4')
