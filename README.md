# COCO YOLO Parser
[YOLOv4](https://github.com/AlexeyAB/darknet) is a famous and convenient tool for object detection, but the author only provides a pretrained model which is trained on [MS COCO](https://cocodataset.org/#home) dataset, which includes 80 categories of objects. 

Usually, we only need some specific categories in those 80 categories, let's say we're only interested in cars, motorcycles and pedestrians in a street scene video, the other 77 categories are unnecessary. If we use the pretrained YOLOv4 without retraining it, it will cost lots of extra memories and have a worse performance.

This repository has two purposes:
1. Download only specific categories images and labels in COCO dataset.
2. Convert the annotations format from COCO to YOLOv4 acceptable.

## Usage
0. Install python environment by `pip3 install -r requestents.txt`
1. Download [COCO annotations](https://cocodataset.org/#download) and place it in this repository. For example, [2014 Train/Val annotations [241MB]](http://images.cocodataset.org/annotations/annotations_trainval2014.zip). Please note that you don't need to download images, only annotations are needed.
2. In function `get_image_and_annotation` in `utils.py`, you need to set the object categories that you want to download from COCO dataset as [target](https://github.com/yamiefun/COCO-YOLO-Parser/blob/5573b9408628a39e69b73d4ace3a91d1bd434b93/utils.py#L51). Note that this code will download only the images which have all object categories in `target` in it at the same time. If you're not sure if a category is included in COCO dataset, please take a look at the [category list](https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/).
3. After setting the target, you can run `utils.py`. 
    ### Parameters
    + `--anno`: path to COCO annotation file, default is `instances_train2017.json`
    + `--img_out`: path to store the downloaded COCO images, default is `./image/`
    + `--label_out`: path to store the labels for training YOLO, default is `./label/`
    
    For example, if you download and put `instances_train2014.json` in the same directory as `utils.py`, you can just simply run 
    ```
    $ python3 utils.py --anno instances_train2014.json
    ```
    If you want to put images and labels in a same folder called `obj` which meets the requirement in the training YOLO [tutorial](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects), you can run
    ```
    $ python3 utils.py --img_out obj/ --label_out obj/
    ```
4. `train.txt` and `obj.names` will be generated as well. These two files are necessary for training YOLOv4. 
