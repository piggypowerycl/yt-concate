import logging

from .step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(__name__)
        logger.info('In preflight')
        utils.create_dirs()
