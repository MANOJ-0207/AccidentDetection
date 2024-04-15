from pycocotools.coco import COCO
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN
import numpy as np
import cv2
import torch
import os
from torch.utils.data import DataLoader
import json
import torchvision
import warnings
warnings.filterwarnings("ignore")

from src import CustomDataset,constants,Training,saveLossGraph,collate_fn



custom_train_data = CustomDataset(annotationFile=constants.TRAIN_ANNOTATIONS_FILE,root_dir=constants.IMAGES)
custom_val_data = CustomDataset(annotationFile=constants.VAL_ANNOTATIONS_FILE,root_dir=constants.IMAGES)

train_loader = DataLoader(custom_train_data, batch_size=constants.BATCH_SIZE, shuffle=True, num_workers=4, collate_fn=collate_fn)
val_loader = DataLoader(custom_val_data, batch_size=constants.BATCH_SIZE, shuffle=False, num_workers=4, collate_fn=collate_fn)


# classes
with open(constants.TRAIN_ANNOTATIONS_FILE,"r") as f:
  classes = [cat["name"] for cat in json.load(f)["categories"]]
  classes.insert(0,"__background__")


# model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, len(classes))



device = torch.device(constants.DEVICE) if constants.DEVICE == "cuda" and  torch.cuda.is_available() else torch.device(constants.DEVICE)
model.to(device)

params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, nesterov=True, weight_decay=1e-4)

Training(traindataloader=train_loader,
         valdataloader=val_loader,
         epochs=constants.EPOCHS,
         model=model,
         optimizer=optimizer,
         device=device,
         save_model=True,
         save_loss=True).run()

# save loss curve
saveLossGraph(lossJson="models/loss.json",outPath="loss.jpg")
