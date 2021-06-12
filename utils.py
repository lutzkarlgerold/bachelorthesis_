import csv
import pathlib
from PIL import Image, ImageChops
import os
import datetime
from typing import List
import cv2
from scipy import stats
import numpy as np


class SampleGroup:
    def __init__(self, sample_name, max_pilling_stage=8, file_location="."):
        self.sample_name = sample_name
        self.images: List[List[Image]] = []
        self.differences: List[List[Image]] = []
        self.histograms = []
        self.fill_images(max_pilling_stage=max_pilling_stage)
        self.file_location = file_location
        self.features = []
        self.create_diffs()
        self.create_features()
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
                cv2.hi  # todo
        raise NotImplementedError

    def create_features(self,verbose=True):
        """

        :return:
        """

        for n_diff_group, diff_group in enumerate(self.images):
            self.features.append([])
            for n_diff, diff in enumerate(diff_group):
                feature_list = []
                diff = np.array(diff)

                mean = np.mean(diff)

                std = np.std(diff)
                size = len(diff) * len(diff)
                _min = np.min(diff)
                _max = np.max(diff)
                if verbose:
                    print(
                        "Sample {}, group {},difference {}  Mean = {:.1f}, standard deviation = {:.1f}, Count = {:.0f}, min = {:.0f}, max = {:.0f}".format(
                            self.sample_name, n_diff_group, n_diff, mean, std, size, _min, _max))
                feature_list = [mean, std, size, _min, _max]
                self.features[-1].append(feature_list)
    def write_features(self,out_file,header=False):
        writemode = "a"
        if header:
            writemode="w"
        with open(out_file,writemode,newline="")as o_file:
            writer = csv.writer(o_file)
            head = ["sample_name", "n_diff_group", "n_diff", "mean", "std", "size", "min", "max"]
            if header:
                writer.writerow(head)
            for n_feature_group, feature_group in enumerate(self.features):
                for n_feature, feature in enumerate(feature_group):
                    writer.writerow([self.sample_name,n_feature_group,n_feature,*feature])

    def create_recall(self):
        raise NotImplementedError  # tbd
    def aggregate_group(self):
        raise NotImplementedError
    def __repr__(self):
        return f"sample name : {self.sample_name}, number of image_groups = {len(self.images)}"


if __name__ == '__main__':
    workdir = "./input_pictures/Gruppe1"
    os.chdir(workdir)
    s = SampleGroup("125")
    print(s)
    # s.images[0][0].show()
    print(len(s.images), len(s.images[0]))
    print(len(s.differences), len(s.differences[0]))
    print(s.features)
    s.write_features("../../test,csv",header=True)

    # create all sample files
    samples=[]
    number_format = "{:03}"
    for i_sample in range(128):
        try:
            s = SampleGroup(sample_name=number_format.format(i_sample))
        except FileNotFoundError:
            print(f"sample {i_sample} not in folder")
            continue
        samples.append(s)
    first =True
    for s in samples:
        s.write_features(out_file="../../test,csv",header=first)
        first=False
