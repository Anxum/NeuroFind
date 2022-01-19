# NeuroFind
**A solution to the to the Task given by the Oberseminar of Messtechnik Institute of TU Dresden in 2021**

## Installation
please install on a linux operating system

```
git clone https://github.com/Anxum/NeuroFind.git
cd NeuroFind
git clone https://github.com/ultralytics/yolov5.git temp
mv temp/.git yolov5/.git
mv temp/* yolov5
rm -rf temp
cd yolov5
pip3 install -r requirements.txt  # install
cd ../Faster_R-CNN
git clone https://github.com/tensorflow/models.git
pip3 install lxml
mkdir models/protoc
mv protoc-3.19.3-linux-x86_64.zip models/protoc
cd models/protoc
unzip protoc-3.19.3-linux-x86_64.zip
rm -r protoc-3.19.3-linux-x86_64.zip
cd ../research
../protoc/bin/protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```

## Inference
### YOLOv5
### Faster R-CNN

## Training
### YOLOv5
### Faster R-CNN

