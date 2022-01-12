from concurrent import futures

from pytube import YouTube
import time

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        with futures.ThreadPoolExecutor(max_workers=30) as executor:
            for yt in data:
                if utils.caption_file_exists(yt):
                    print('found existing caption file')
                    continue
                print('downloading caption for', yt.id)
                try:
                    executor.submit(self.download_captions, yt)
                except (AttributeError, KeyError, TypeError):
                    continue
        end = time.time()

        print(f'Elapsed time = {end-start} seconds')
        return data

    def download_captions(self, yt):
        source = YouTube(yt.url)
        try:
            en_caption = source.captions.get_by_language_code('a.en')
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
        except (AttributeError, KeyError) as e:
            print(e)
            return e

        text_file = open(yt.caption_filepath, "w", encoding='utf-8')
        text_file.write(en_caption_convert_to_srt)
        text_file.close()
