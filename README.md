# NeuroFind
**A solution to the to the Task given by the Oberseminar of Messtechnik Institute of TU Dresden in 2021**

## Installation
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
pip3 install pillow
pip3 install lxml
pip3 install jupyter
pip3 install malplotlib

```

## Inference
### YOLOv5
### Faster R-CNN

## Training
### YOLOv5
### Faster R-CNN

