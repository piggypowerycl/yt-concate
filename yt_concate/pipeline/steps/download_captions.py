import logging
from concurrent import futures

from pytube import YouTube
import time

from .step import Step

logger = logging.getLogger(__name__)


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        print('captions to download =', len(data))
        with futures.ThreadPoolExecutor(max_workers=30) as executor:
            for yt in data:
                if utils.caption_file_exists(yt):
                    logger.info(f'Found existing caption file {yt.id}')
                    continue
                logger.info(f'Downloading caption for {yt.id}')
                try:
                    executor.submit(self.download_captions, yt)
                except (AttributeError, KeyError, TypeError):
                    continue
        end = time.time()

        print(f'caption downloading elapsed time = {end-start} seconds')
        return data

    def download_captions(self, yt):
        source = YouTube(yt.url)
        try:
            en_caption = source.captions.get_by_language_code('a.en')
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
        except (AttributeError, KeyError) as e:
            logger.warning(e)
            return e

        text_file = open(yt.caption_filepath, "w", encoding='utf-8')
        text_file.write(en_caption_convert_to_srt)
        text_file.close()
