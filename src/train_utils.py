from pycocotools.coco import COCO
import cv2
import torch
import os
import json
import numpy as np 
from os import makedirs
from os.path import join
from src import constants

from .utils import isColab
# if isColab():
#   from tqdm.notebook import tqdm
# else:
#   from tqdm import tqdm
  
# from tqdm.autonotebook import tqdm
from tqdm import tqdm
  
class CustomDataset():
  def __init__(self,annotationFile:str,root_dir:str):
    self.coco = COCO(annotationFile)
    self.root_images = root_dir
    self.x_train = self.coco.getImgIds()
  def readFile(self,annotationfile:str):
    with open(annotationfile,"r") as f:
      return json.load(f)

  def __len__(self):
    return len(self.x_train)

  def get_resized_annotations(self,image_dim:tuple,bbox:list,resize:tuple):
    """resize annotations
    Args:
        image_dim (tuple): image shape
        bbox (list): bbox coordinates [x,y,w,h]
        resize (tuple): resize dimension (x,y)

    Returns:
        list: [x,y,w,h]
    """
    width_ratio,height_ratio = [resize[idx]/image_dim[idx] for idx in range(len(resize))]
    return (bbox[0]*height_ratio,bbox[1]*width_ratio,bbox[2]*height_ratio,bbox[3]*width_ratio)

  def __getitem__(self,index):
    img_info = self.coco.loadImgs(self.x_train[index])[0]
    img_main = cv2.imread(os.path.join(self.root_images, img_info['file_name']))
    img = cv2.resize(img_main,constants.RESIZE_FACTOR)
    img = img/255
    annIds = self.coco.getAnnIds(imgIds=img_info['id'])
    anns = self.coco.loadAnns(annIds)
    num_objs = len(anns)
    boxes = torch.zeros([num_objs,4], dtype=torch.float32)
    labels = torch.zeros(num_objs, dtype=torch.int64)

    for i in range(num_objs):
        [x,y,w,h]=anns[i]["bbox"]
        [x,y,w,h] = self.get_resized_annotations(img_main.shape,[x,y,w,h],(600,600))
        boxes[i] = torch.tensor(list(map(int,(x,y,x+w,y+h))))
        labels[i] = torch.tensor([anns[i]["category_id"]])

    img = torch.as_tensor(img, dtype=torch.float32)
    img = img.permute(2,0,1)
    data = {}
    data["boxes"] =  boxes
    data["labels"] = labels
    return img, data
  def collate_fn(self,batch):
        return tuple(zip(*batch))

# custom training function
class Training():
    def __init__(self,
                traindataloader,
                valdataloader,
                epochs:int,
                model,
                optimizer,
                device,
                save_model:bool=True,
                save_model_per_epoch:int=5,
                save_loss:bool=True):

      self.traindataloader = traindataloader
      self.valdataloader = valdataloader
      self.epochs = epochs
      self.model = model
      self.optimizer = optimizer
      self.device = device
      self.save_model = save_model
      self.save_model_per_epoch = save_model_per_epoch
      self.save_loss = save_loss
      self.modelsPath = "models"
  
      print("---------------------------------------------------")      
      print("Device:",self.device)
      print("IsColab:",isColab())
      print(f"Epochs: {self.epochs}")
      print(f"Save Model: {self.save_model_per_epoch}")
      print(f"Save Model Per Epoch: {self.save_loss}")
      print(f"Models Path: {self.modelsPath}")
      print("---------------------------------------------------")      



    def one_epoch_train(self,
                        dataloader,
                        epoch:int,
                        model,
                        optimizer,
                        device):
            total_train_loss=[]
            total_train_loss_dict=[]
            one_epoch_bar = tqdm(total=len(dataloader),desc=f"Train",leave=True)
            model.train()
            for batch,(images,targets) in enumerate(dataloader):
                images = [image.to(device) for image in images]
                targets = [{k:torch.tensor(v).to(device) for k, v in t.items()} for t in targets]
                # print(len(images),images[0].shape,targets)
                loss_dict = model(images,targets)
                train_loss = sum([loss for loss in loss_dict.values()])
                train_loss_dict = [{k:v.item()} for k,v in loss_dict.items()]

                optimizer.zero_grad()
                train_loss.backward()
                optimizer.step()

                total_train_loss.append(train_loss.item())
                total_train_loss_dict.append(train_loss_dict)

                one_epoch_bar.update(1)


            return total_train_loss,total_train_loss_dict

    def one_epoch_validation(self,
                             dataloader,
                             model,
                             device):
        total_val_loss = []
        total_val_loss_dict = []
        one_epoch_bar = tqdm(total=len(dataloader),desc=f"validation ",leave=True)

        with torch.no_grad():
          for batch,(images,targets) in enumerate(dataloader):
              images = [torch.tensor(image).to(device) for image in images]
              targets = [{k:torch.tensor(v).to(device) for k, v in t.items()} for t in targets]

              loss_dict = model(images,targets)
              val_loss = sum([loss for loss in loss_dict.values()])
              val_loss_dict = [{k:v.item()} for k,v in loss_dict.items()]

              total_val_loss.append(val_loss.item())
              total_val_loss_dict.append(val_loss_dict)
              one_epoch_bar.update(1)
        return total_val_loss,total_val_loss_dict


    def updateLoss(self,epoch,trainLoss,valLoss):
        if epoch == 1:
            info = {
                "epoch":[],
                "trainLoss":[],
                "valLoss":[],
                  }

            info["epoch"].append(epoch)
            info["trainLoss"].append(trainLoss)
            info["valLoss"].append(valLoss)

            makedirs(self.modelsPath,exist_ok=True)
            with open(join(self.modelsPath,"loss.json"),"w") as f:
                data = json.dump(info,f)
        else:
            with open(join(self.modelsPath,"loss.json"),"r") as f:
                data = json.load(f)
            data = data.copy()
            data["epoch"].append(epoch)
            data["trainLoss"].append(trainLoss)
            data["valLoss"].append(valLoss)

            with open(join(self.modelsPath,"loss.json"),"w") as f:
                data = json.dump(data,f)



    def run(self):
        epoch_progressbar = tqdm(total=self.epochs,desc=f"epochs : ")

        for epoch in range(1,self.epochs+1):
            epoch_progressbar.update(1)

            total_train_loss,total_train_loss_dict = self.one_epoch_train(
                                                        self.traindataloader,
                                                        self.epochs,
                                                        self.model,
                                                        self.optimizer,
                                                        self.device)
            total_val_loss,total_val_loss_dict = self.one_epoch_validation(
                                                        self.valdataloader,
                                                        self.model,
                                                        self.device
                                                        )

            print(f"epoch: {epoch} | train loss: {np.mean(total_train_loss)} | val loss: {np.mean(total_val_loss)}")
            if self.save_loss:
                self.updateLoss(epoch=epoch,trainLoss=np.mean(total_train_loss),valLoss=np.mean(total_val_loss))

            if self.save_model:
                makedirs(self.modelsPath,exist_ok=True)
                if epoch % self.save_model_per_epoch == 0:
                    torch.save(self.model.state_dict(), join(self.modelsPath,f"model_{str(epoch)}_loss_{np.mean(total_train_loss):2f}_val_loss_{np.mean(total_val_loss):2f}.torch"))
