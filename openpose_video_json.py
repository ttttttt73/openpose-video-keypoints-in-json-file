import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import json

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# Flags
#I didn't use this part
#parser = argparse.ArgumentParser()
#parser.add_argument("--image_dir", default="C:\\Users\\han006\\Documents\\GitHub\\openpose\\examples\\video\\video.avi", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
#args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["model_pose"]="COCO"
params["face"] = True
params["number_people_max"] = 1
params["write_json"] = "./output_jsons/"


# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1])-1: next_item = args[1][i+1]
    else: next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-','')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-','')
        if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

#just file information, you can change it to achieve your goal
for i in range(10,100,1):
    path="E:\\Sign Language Dataset\\Chinese SL Dataset (Sentences)\\color\\0000{}".format(i)
    filepath="C:\\Users\\ECE-ML\\Desktop\\video_json\\0000{}".format(i)
    os.mkdir(filepath)
    path_name=[]
    file_name_json=[]
    name=0
    for paths, dirs, files in os.walk(path):
        print(paths)
        for file in files:
            path_video_file_name=os.path.join(paths, file)
            path_name.append(path_video_file_name)
            basename=os.path.basename(path_video_file_name)
            video_name_json=os.path.splitext(basename)[0]+'.json'
            file_name_json.append(video_name_json)

    for file in path_name:
        keypointlist = []
        keypointdict = {}
        try:
        # Starting OpenPose
            opWrapper = op.WrapperPython()
            opWrapper.configure(params)
            opWrapper.start()
    # Process Image
            datum = op.Datum()
        #datum.fileName=file
            cap = cv2.VideoCapture(file)
            while (cap.isOpened()):
                hasframe, frame= cap.read()
                if hasframe== True:

                    datum.cvInputData = frame
                    opWrapper.emplaceAndPop([datum])

    # Display Image
                    keypointdict['body keypoint'] = np.array(datum.poseKeypoints).tolist()
                    keypointdict['Face keypoint'] = np.array(datum.faceKeypoints).tolist()
                    keypointdict['Left hand keypoint'] = np.array(datum.handKeypoints[0]).tolist()
                    keypointdict['right hand keypoint'] = np.array(datum.handKeypoints[1]).tolist()
                    keypointlist.append(keypointdict.copy())#must be the copy!!!
                    cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)
                    cv2.waitKey(1)
                else:
                    break
        except Exception as e:
            # print(e)
            sys.exit(-1)

        with open(os.path.join(filepath,file_name_json[name]),"a") as f:
            json.dump(keypointlist, f, indent=0)
        name+=1
