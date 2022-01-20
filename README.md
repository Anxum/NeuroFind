# NeuroFind
**A solution to the to the Task given by the Oberseminar of Messtechnik Institute of TU Dresden in 2021**

## Installation
_please install on a linux operating system_


### Install both Faster R-CNN and Yolov5

```
git clone https://github.com/Anxum/NeuroFind.git
cd NeuroFind
git clone https://github.com/ultralytics/yolov5.git temp
mv temp/.git yolov5/.git
mv temp/* yolov5
rm -rf temp
cd yolov5
pip3 install -r requirements.txt
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
cp object_detection/packages/tf2/setup.py .
python3 -m pip install --use-feature=2020-resolver .
```

### Only Install Yolov5
```
git clone https://github.com/Anxum/NeuroFind.git
cd NeuroFind
git clone https://github.com/ultralytics/yolov5.git temp
mv temp/.git yolov5/.git
mv temp/* yolov5
rm -rf temp
cd yolov5
pip3 install -r requirements.txt 
```

### Only Install Faster R-CNN
```
git clone https://github.com/Anxum/NeuroFind.git
cd NeuroFind/Faster_R-CNN
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
cp object_detection/packages/tf2/setup.py .
python3 -m pip install --use-feature=2020-resolver .
```
### Weights

In addition to the installation guide above please download the weights for the neuronal networks from: --_insert url_--

Standardized paths for YOLOv5 and Faster R-CNN:

| Neuronal Network | Put Weights to: |
|------------------|------------------|
| YOLOv5 | _NeuroFind/yolov5/runs/train/weights_ |
| Faster R-CNN | _NeuroFind/Faster_R-CNN/export_|

If you choose to put the weights into another folder you must refer to these paths if you wish to use the inference algorithms later.



## Inference
### YOLOv5
### Faster R-CNN

## Training
### YOLOv5
### Faster R-CNN

