# Jetson-Object-Detection
### Using Jetson-Inference to do cars, persons, bikes and road signs detection
### This demo runs on Nvidia Jetson Nano and using a CSI camera

### Pull the docker image for deepstream python version
$ docker pull ryagi997/deepstream-6.0-python:samples

### run the docker image and map the workspace dir and the camera
$ docker images

$ docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/argus_socket:/tmp/argus_socket --device /dev/video0 -v ~/Documents/GStreamer:/opt/nvidia/deepstream/deepstream-6.0/sources/deepstream_python_apps/apps/GStreamer [the docker image ID]

### for caffe model, the dir is like this:
=============================================================================================
drwxr-xr-x 2 root root    4096 Oct  5  2021 ./
drwxr-xr-x 9 root root    4096 Oct  5  2021 ../
-rw-r--r-- 1 root root    1126 Oct  5  2021 cal_trt.bin
-rw-r--r-- 1 root root      28 Oct  5  2021 labels.txt
-rw-r--r-- 1 root root 6244865 Oct  5  2021 resnet10.caffemodel
-rw-r--r-- 1 root root    7605 Oct  5  2021 resnet10.prototxt
root@saturn-nano:/opt/nvidia/deepstream/deepstream-6.0/samples/models/Primary_Detector#
=============================================================================================

### for the config file, dstest1_pgie_config.txt uses official deepstream sample's configuration
### go to /opt/nvidia/deepstream/deepstream-6.0/sources/deepstream_python_apps/apps/GStreamer
### put the dstest1_pgie_config.txt and camera_jetson_infer.py in the Gstream dir
$ python3 camera_jetson_infer.py

### This will generate the TensorRT engine file with .engine, then Open your /dev/video0 camera and push the stream to your local network
### The Nvidia Jestson Nano is the server(192.168.8.115), my Win10 PC is the client(192.168.8.121)


<img width="1063" alt="WX20230416-094143@2x" src="https://user-images.githubusercontent.com/56700281/232261635-89c8264b-86f7-4bd7-bf9f-87c20496812f.png">

![IMG_3592](https://user-images.githubusercontent.com/56700281/232261462-05804b7d-7e44-4775-8717-c7fcc68b7878.PNG)



