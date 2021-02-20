from pytube import YouTube

from yt_concate.pipeline.steps.step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        for url in data:
            print("downloading caption for", url)
            if utils.caption_file_exists(url):
                print("found existing caption file")
                continue
            try:
                source = YouTube(url)
                en_caption = source.captions['a.en']
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                print("Error when downloading caption for", url)
                continue

            text_file = open(utils.get_caption_filepath(url), "w", encoding="utf-8")
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        return data

