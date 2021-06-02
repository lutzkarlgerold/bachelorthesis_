
import pathlib
from PIL import Image, ImageChops
import os
import datetime
from typing import List

class SampleGroup:
    def __init__(self, sample_name, max_pilling_stage=8, file_location="."):
        self.sample_name = sample_name
        self.images: List[List[Image]] = []
        self.differences: ListList[[Image]] = []
        self.histograms = []
        self.fill_images(max_pilling_stage=max_pilling_stage)
        self.file_location = file_location

    def fill_images(self, max_pilling_stage=8):
        #os.chdir(self.file_location)
        pil_stage_name_format = "{}-{}-"
        pil_stage_names = []

        for p_stage in range(max_pilling_stage + 1):
            pil_stage_names.append(pil_stage_name_format.format(self.sample_name, p_stage))
        images = []

        first_image_of_sample = True
        for pil_stage_name in pil_stage_names:
            first_image_in_stage = True
            for i in range(0, 8):
                img_count = str(i + 1)
                try:
                    image = Image.open(pil_stage_name + img_count + ".png")
                    if first_image_in_stage:
                        images.append([])
                    first_image_in_stage = False
                    first_image_of_sample = False
                    images[-1].append(image)
                except FileNotFoundError as F_e:
                    if first_image_of_sample:
                        raise F_e
                    else:
                        break

        self.images = images

        """
        for j, image in enumerate(images[1:]):
            diff = ImageChops.fill_images(images[0], image)

            if diff.getbbox():  # hier ist irgendwas falsch

                ensure_directory("./diff")
                print(pil_stage_names[j + 1] + str(i) + "-diff.png")
                diff.save("./diff/" + pil_stage_names[j + 1] + str(i) + "-diff.png")
        """

    def create_diffs(self):
        raise NotImplementedError  # Todo

    def create_histograms(self):
        raise NotImplementedError

    def create_features(self):
        raise NotImplementedError
        return [1,2,3]

    def create_recall(self):
        raise NotImplementedError  # tbd

    def __repr__(self):
        return f"sample name : {self.sample_name}, number of images = {len(self.images)}"
