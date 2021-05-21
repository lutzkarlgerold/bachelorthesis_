import datetime

from pypylon import pylon
from pypylon import genicam

import sys
import cv2
import rpyc
import platform
import os
import logging


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


def get_image_from_cam(camera, target_path, save_file=True, file_name="Test-ref.jpg"):
    camera.StartGrabbing()
    with camera.RetrieveResult(2000) as result:

        # Calling AttachGrabResultBuffer creates another reference to the
        # grab result buffer. This prevents the buffer's reuse for grabbing.
        img.AttachGrabResultBuffer(result)

        if platform.system() == 'Windows':
            # The JPEG format that is used here supports adjusting the image
            # quality (100 -> best quality, 0 -> poor quality).
            ipo = pylon.ImagePersistenceOptions()
            quality = 100
            ipo.SetQuality(quality)

            # Verzeichnis der Referenzbilder
            os.chdir(target_path)

            if save_file:
                filename = file_name  # % quality
                img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
        else:
            raise Exception("Platform not supported")


        # In order to make it possible to reuse the grab result for grabbing
        # again, we have to release the image (effectively emptying the
        # image object).
        img.Release()
        camera.StopGrabbing()


if __name__ == '__main__':
    # Dateiname
    probenname = "041-2"
    # The name of the pylon file handle
    nodeFile1 = "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/camera settings/2021-04-22_acA4600-10uc_23004624_bay8.pfs"
    nodeFile2 = "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/camera settings/2021-05-21 acA4600-10uc_23004624_ET4200.pfs"
    logging.basicConfig(level=logging.INFO)
    num_img_to_save = 1
    img = pylon.PylonImage()
    tlf = pylon.TlFactory.GetInstance()

    cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()
    pylon.FeaturePersistence.Load(nodeFile1, cam.GetNodeMap(), True)

    for i in range(num_img_to_save):
        color_dir = "C:/Users/lg/Dokumente/BA/bachelorthesis/reference pictures"
        ensure_directory(color_dir)

        picture_name = f"{probenname}-ref.jpg"
        get_image_from_cam(cam, color_dir, file_name=picture_name)

    cam.Close()

    i = 0

    for x in range(0, 9):
        img_count = str(i)
        i = i + 1
        # Number of images to be grabbed.
        countOfImagesToGrab = 1
        logging.info(f"creating image {x} at {datetime.datetime.now()} ")
        # The exit code of the sample application.
        exitCode = 0

        try:

            # Create an instant cam object with the cam device found first.
            cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            cam.Open()
            pylon.FeaturePersistence.Load(nodeFile2, cam.GetNodeMap(), True)
            # Print the model name of the cam.

            logging.info(f"Using device  {cam.GetDeviceInfo().GetModelName()}")

            # Just for demonstration, read the content of the file back to the cam's node map with enabled validation.
            # demonstrate some feature access
            new_width = cam.Width.GetValue() - cam.Width.GetInc()
            if new_width >= cam.Width.GetMin():
                cam.Width.SetValue(new_width)

            # The parameter MaxNumBuffer can be used to control the count of buffers
            # allocated for grabbing. The default value of this parameter is 10.
            cam.MaxNumBuffer = 5

            # Start the grabbing of c_countOfImagesToGrab images.
            # The cam device is parameterized with a default configuration which
            # sets up free-running continuous acquisition.
            sw_dir = "C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures"
            ensure_directory(sw_dir)
            save_image = x != 0  # False für 0, True für alle anderen
            logging.info(f"save_image = {save_image}")

            picture_name = f"{probenname}-{x}.png"
            get_image_from_cam(cam, sw_dir, save_file=save_image, file_name=picture_name)


        except genicam.GenericException as e:
            # Error handling.
            logging.error("An exception occurred.")
            logging.error(e.GetDescription())
            exitCode = 1

        finally:
            cam.Close()

        conn = rpyc.connect('192.168.178.175', port=18812)
        conn.root.run_motor_degrees(20, 45)
        conn.root.speak_message(img_count)

    sys.exit(exitCode)
