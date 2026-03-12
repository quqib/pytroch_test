import os
import json
import random
import shutil

# 原始数据
img_dir = "dataset_raw/images"
json_dir = "dataset_raw/labels_json"

# 训练数据
train_img = "dataset/images/train"
val_img = "dataset/images/val"

train_label = "dataset/labels/train"
val_label = "dataset/labels/val"

os.makedirs(train_img, exist_ok=True)
os.makedirs(val_img, exist_ok=True)
os.makedirs(train_label, exist_ok=True)
os.makedirs(val_label, exist_ok=True)

imgs = os.listdir(img_dir)

# 划分 80% 训练 20% 验证
val_imgs = random.sample(imgs, int(len(imgs)*0.2))

for img in imgs:

    img_path = os.path.join(img_dir, img)
    json_name = os.path.splitext(img)[0] + ".json"
    json_path = os.path.join(json_dir, json_name)

    if not os.path.exists(json_path):
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    w = data["imageWidth"]
    h = data["imageHeight"]

    txt_lines = []

    for shape in data["shapes"]:

        label = shape["label"]
        points = shape["points"]

        x1, y1 = points[0]
        x2, y2 = points[1]

        x_center = ((x1 + x2) / 2) / w
        y_center = ((y1 + y2) / 2) / h
        bw = abs(x2 - x1) / w
        bh = abs(y2 - y1) / h

        class_id = 0

        txt_lines.append(
            f"{class_id} {x_center} {y_center} {bw} {bh}"
        )

    txt_name = os.path.splitext(img)[0] + ".txt"

    if img in val_imgs:

        shutil.copy(img_path, os.path.join(val_img, img))

        with open(os.path.join(val_label, txt_name), "w") as f:
            f.write("\n".join(txt_lines))

    else:

        shutil.copy(img_path, os.path.join(train_img, img))

        with open(os.path.join(train_label, txt_name), "w") as f:
            f.write("\n".join(txt_lines))

print("数据准备完成")