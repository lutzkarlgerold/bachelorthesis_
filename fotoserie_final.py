from pypylon import pylon
from pypylon import genicam

import sys
import cv2
import rpyc
import platform
import os

# Dateiname
datei = "Test-"

# The name of the pylon file handle
nodeFile1 = "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/cam settings/2021-04-22_acA4600-10uc_23004624_bay8.pfs"
nodeFile2 = "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/cam settings/2021-05-21 acA4600-10uc_23004624_ET4200.pfs"

num_img_to_save = 1
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

cam = pylon.InstantCamera(tlf.CreateFirstDevice())
cam.Open()
pylon.FeaturePersistence.Load(nodeFile1, cam.GetNodeMap(), True)


def get_image_from_cam(camera, target_path):
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

            filename = datei + "ref.jpeg"  # % quality
            img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
        else:
            filename = "saved_pypylon_img_%d.png" % i
            img.Save(pylon.ImageFileFormat_Png, filename)

        # In order to make it possible to reuse the grab result for grabbing
        # again, we have to release the image (effectively emptying the
        # image object).
        img.Release()
        camera.StopGrabbing()


for i in range(num_img_to_save):
    get_image_from_cam(cam, "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/reference pictures")

cam.Close()

i = 0

for x in range(0, 8):
    img_count = str(i)
    i = i + 1
    # Number of images to be grabbed.
    countOfImagesToGrab = 1

    # The exit code of the sample application.
    exitCode = 0

    try:

        # Create an instant cam object with the cam device found first.
        cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        cam.Open()
        pylon.FeaturePersistence.Load(nodeFile2, cam.GetNodeMap(), True)
        # Print the model name of the cam.

        print("Using device ", cam.GetDeviceInfo().GetModelName())

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
        get_image_from_cam(cam, "C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/color_pictures")
        cam.Close()

    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.")
        print(e.GetDescription())
        exitCode = 1

    conn = rpyc.connect('192.168.178.175', port=18812)
    conn.root.run_motor_degrees(20, 90)
    conn.root.speak_message(img_count)

sys.exit(exitCode)
