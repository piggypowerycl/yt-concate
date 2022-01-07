from .step import Step


class ReadCaption(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exists(yt):
                continue
            captions = {}
            with open(yt.caption_filepath, 'r') as f:
                timeline = False
                time = None
                caption = None
                for line in f:
                    line = line.strip()
                    if '-->' in line:
                        timeline = True
                        time = line
                        continue
                    if timeline:
                        caption = line
                        captions[caption] = time
                        timeline = False
            yt.captions = captions
        return data
