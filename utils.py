import pathlib
from PIL import Image, ImageChops
import os
import datetime
from typing import List
import cv2
from scipy  import stats
import numpy as np

class SampleGroup:
    def __init__(self, sample_name, max_pilling_stage=8, file_location="."):
        self.sample_name = sample_name
        self.images: List[List[Image]] = []
        self.differences: List[List[Image]] = []
        self.histograms = []
        self.fill_images(max_pilling_stage=max_pilling_stage)
        self.file_location = file_location
        self.features=[]

    def fill_images(self, max_pilling_stage=8):
        """
        Todo
        write doumentation
        :param max_pilling_stage:
        :return:
        """
        # os.chdir(self.file_location)
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

    def create_diffs(self):
        """
        creates diffs of images in reference to the first image of the group
        :return:
        """
        for image_group in self.images:
            base_image = image_group[0]
            self.differences.append([])
            for image in image_group[1:]:
                self.differences[-1].append(ImageChops.difference(base_image, image))

    def create_histograms(self):
        """
        creates histograms of differences
        :return:
        """

        for dif_group in self.differences:
            self.histograms.append([])
            for dif in dif_group:
                cv2.hi# todo
        raise NotImplementedError

    def create_features(self):
        """

        :return:
        """
        for diff_group in self.images:
            self.features.append([])
            for diff in diff_group:
                feature_list = []
                diff = np.array(diff)

                mean = np.mean(diff).item(),
                std = np.std(diff).item(),
                size = len(diff) * len(diff),
                min = np.min(diff).item(),
                max = np.max(diff).item()
                print("Mean = {:.1f}, standard deviation = {:.1f}, Count = {:.0f}, min = {:.0f}, max = {:.0f}".format(
                    np.mean(diff).item(),
                    np.std(diff).item(),
                    len(diff) * len(diff),
                    np.min(diff).item(),
                    np.max(diff).item()
                ))
                feature_list=[mean,std,size,min,max]
                self.features[-1].append(feature_list)

    def create_recall(self):
        raise NotImplementedError  # tbd

    def __repr__(self):
        return f"sample name : {self.sample_name}, number of image_groups = {len(self.images)}"


if __name__ == '__main__':
    workdir = "./input_pictures/Gruppe1"
    os.chdir(workdir)
    s = SampleGroup("125")
    print(s)
    # s.images[0][0].show()
    s.create_diffs()
    print(len(s.images), len(s.images[0]))
    print(len(s.differences), len(s.differences[0]))
    s.create_features()
    print(s.features)