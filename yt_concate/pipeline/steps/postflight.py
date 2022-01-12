import time

from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        print('in Postflight')
        if utils.output_video_file_exists(inputs['channel_id'], inputs['search_word']) and utils.video_list_file_exists(inputs['channel_id']):
            if inputs['cleanup']:
                time.sleep(5)
                print('Removing downloaded captions and videos.')
                utils.delete_dirs(inputs['channel_id'])


