from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        print('in Postflight')
        if utils.output_video_file_exists(inputs['channel_id'], inputs['search_word']):
            if inputs['cleanup']:
                print('Removing downloaded captions and videos.')
                utils.delete_dirs(inputs['channel_id'])
                print('Finished.')
            else:
                print('Finished')