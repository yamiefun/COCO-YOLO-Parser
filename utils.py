from pycocotools.coco import COCO
import requests
import cv2
import os
from os import walk
import argparse

def env_set(args):
    try:
        #os.mkdir('train')
        os.makedirs(args.img_out)
    except Exception:
        print(Exception)
    try:
        os.makedirs(args.label_out)
        #os.mkdir('label')
    except Exception:
        print(Exception)


def create_obj_name_file(target):
    with open("obj.names", "w") as f:
        for cat in target:
            f.write(cat+'\n')


'''
def get_imageIds(catIds, mode='union'):
    # this function is not finished yet
    if mode == "union":
        imgIds = set()
        for catId in catIds:
            id_list = coco.getImgIds(catIds=catId)
            print(f"# of images with {target[target_map[catId]]} : {len(id_list)}")
            imgIds = imgIds.union(set(id_list))
        imgIds = list(imgIds)
    elif mode == "intersection":
        imgIds = coco.getImgIds(catIds=catIds)
    else:
        pass

    return imgIds
'''

def get_image_and_annotation(args):
    env_set(args)
    #coco = COCO('instances_train2017.json')
    coco = COCO(args.anno)

    # list of category that you want to train
    target = ['car', 'motorcycle']

    create_obj_name_file(target)
    # need a mapping table to find the correspondence between coco catId and custom catId
    target_map = {}
    for i, cat in enumerate(target):
        coco_catId = coco.getCatIds(catNms=[cat])[0]
        target_map[coco_catId] = i

    # get all coco catId
    catIds = coco.getCatIds(catNms=target)

    # get all image id contain the target category
    imgIds = coco.getImgIds(catIds=catIds)
    #imgIds = get_imageIds(catIds=catIds, mode='union')
    total_num = len(imgIds)
    count = 0

    # get all image information by image id
    images = coco.loadImgs(imgIds)

    for im in images:
        # download image
        img_data = requests.get(im['coco_url']).content

        # save image
        with open(args.img_out+im['file_name'], 'wb') as handler:
            handler.write(img_data)

        # get annotation
        annIds = coco.getAnnIds(imgIds=im['id'])
        anns = coco.loadAnns(annIds)
        
        # create yolo format label file
        label_file_name = f"{args.label_out}/{im['file_name'][:-4]}.txt"
        with open(label_file_name, 'w') as f:
            for inst in anns:
                if inst['category_id'] not in target_map:
                    continue
                line = f"{target_map[inst['category_id']]} " + \
                    f"{(inst['bbox'][0]+inst['bbox'][2]/2)/im['width']} " + \
                    f"{(inst['bbox'][1]+inst['bbox'][3]/2)/im['height']} " + \
                    f"{inst['bbox'][2]/im['width']} " + \
                    f"{inst['bbox'][3]/im['height']}\n"
                f.write(line)

        print("finish images id ", im['id'])
        print(f"Progress: {count*100/total_num:.2f}% ({count}/{total_num})")
        count += 1


def create_train_txtfile(args):
    _, _, filenames = next(walk(args.img_out))
    with open('train.txt', 'w') as f:
        for filename in filenames:
            line = f'data/obj/{filename}\n'
            f.write(line)


def arg_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument('--anno', help='path to COCO annotation file', default=f'instances_train2017.json')
    ap.add_argument('--img_out', help='path to store COCO images', default=f'image')
    ap.add_argument('--label_out', help='path to store label files', default=f'label')
    args = ap.parse_args()
    return args


if __name__ == "__main__":

    args = arg_parse()
    get_image_and_annotation(args)
    create_train_txtfile(args)
