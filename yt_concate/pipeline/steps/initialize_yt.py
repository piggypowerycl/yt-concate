from .step import Step
from yt_concate.model.yt import Yt


class InitializeYT(Step):
    def process(self, data, inputs, utils):
        return [Yt(url) for url in data]
