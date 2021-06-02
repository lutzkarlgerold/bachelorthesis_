# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
import pathlib
from PIL import Image, ImageChops
import os
import datetime
from typing import List


def ensure_directory(target_folder: [str, os.path], recursive=False) -> None:
    """
    generates directories if they do not exist recursively if desired
    :param target_folder:
    :param recursive:
    :return:
    """
    if recursive:
        subfolders = target_folder.split("/")
        for f_n in range(len(subfolders)):
            folder = "/".join(subfolders[:f_n + 1])
            if not os.path.exists(folder):
                try:
                    os.mkdir(folder)
                except OSError:
                    logging.error(f"failed to create folder {folder}")
    else:
        if not os.path.exists(target_folder):
            try:
                os.mkdir(target_folder)
            except OSError:
                logging.error(f"failed to create folder {target_folder}")


# Verzeichnis der Bilder

class SampleGroup:
    def __init__(self, sample_name, max_pilling_stage=8):
        self.sample_name = sample_name
        self.images: List[List[Image]] = []
        self.differences: ListList[[Image]] = []
        self.fill_images(max_pilling_stage=max_pilling_stage)

    def fill_images(self, max_pilling_stage=8):
        pil_stage_name_format = "{}-{}-"
        pil_stage_names = []

        for p_stage in range(max_pilling_stage + 1):
            pil_stage_names.append(pil_stage_name_format.format(self.sample_name, p_stage))
        images = []

        first_image_of_sample = True
        for pil_stage_name in pil_stage_names:
            first_image_in_stage = True
            for i in range(0, 8):
                img_count = str(i+1)
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
        raise NotImplementedError # Todo

    def __repr__(self):
        return f"sample name : {self.sample_name}, number of images = {len(self.images)}"


def difference(Probe="004", n_images_max=8):
    bild_format = "{}-{}-"
    bilder = []

    for i in range(n_images_max + 1):
        bilder.append(bild_format.format(Probe, i))

    i = 1

    for x in range(0, 8):
        img_count = str(i)
        i = i + 1
        images = []
        first = True
        for image_name in bilder:
            try:
                images.append(Image.open(image_name + img_count + ".png"))
                first = False
            except FileNotFoundError as F_e:
                if first:
                    raise F_e
                else:
                    break

        for j, image in enumerate(images[1:]):
            diff = ImageChops.difference(images[0], image)

            if diff.getbbox():  # hier ist irgendwas falsch

                ensure_directory("./diff")
                print(bilder[j + 1] + str(i) + "-diff.png")
                diff.save("./diff/" + bilder[j + 1] + str(i) + "-diff.png")


if __name__ == '__main__':
    workdir = "./input_pictures/Gruppe1"
    os.chdir(workdir)

    probe = SampleGroup("125")
    print(probe)
    print(probe.images)

    """
    
    # fill_images("005")
    min_number = 1
    max_number = 150
    workdir_path = pathlib.Path(".")
    print(workdir_path.iterdir())
    path_content = [x for x in workdir_path.iterdir()]
    number_format = "{:03}"

    for i_p in range(min_number, max_number):
        try:
            fill_images(number_format.format(i_p))
            print(f"Probe {i_p} bearbeitet um: {datetime.datetime.now()}")
        except FileNotFoundError as F_e:
            print(f"Probe {i_p} existiert nicht ")
    print(number_format.format(max_number))
    print(number_format.format(min_number))
    """
