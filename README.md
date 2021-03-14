# COCO Parser
[YOLOv4](https://github.com/AlexeyAB/darknet) is a famous and convenient tool for object detection, but the author only provides a pretrained model which is trained on [MS COCO](https://cocodataset.org/#home) dataset, which includes 80 categories of objects. 

Usually, we only need some specific categories in those 80 categories, let's say we're only interested in cars, motorcycles and pedestrians in a street scene video, the other 77 categories are unnecessary. If we use the pretrained YOLOv4 without retraining it, it will cost lots of extra memories and have a worse performance.

This repository has two purpose:
1. Download only specific categories images and labels in COCO dataset.
2. Convert the annotations format from COCO to YOLOv4 acceptable.

## Usage
1. Download [COCO annotations](https://cocodataset.org/#download) and place it in this repository. For example, [2014 Train/Val annotations [241MB]](http://images.cocodataset.org/annotations/annotations_trainval2014.zip). Please note that you don't keed to download images, only annotations are needed.
2. In function `get_image_and_annotation` in `utils.py`, you need to set the annotation file path correctly.
3. In function `get_image_and_annotation` in `utils.py`, you need to set the object categories that you want to download from COCO dataset as `target`. Note that this code will download only the images which have all object categories in `target` in it at the same time.
4. Images will be downloaded in `train` folder, labels will be generated in `label` folder. 
5. `train.txt` and `obj.names` will be generated. These two files are also necessary for training YOLOv4. 
