import os
import threading
from .telegram_api import send_video
from .utils import isColab,save_video,MyVideoCapture
import cv2
from os.path import join,isfile
import torch
from src import constants
from torchvision import transforms

# if isColab():
#     from tqdm.notebook import tqdm
# else:
#     from tqdm import tqdm
# from tqdm.autonotebook import tqdm
from tqdm import tqdm


transform = transforms.Compose([
    transforms.ToPILImage(),  # Convert to PIL Image
    transforms.Resize((600, 600)),  # Resize to 600x600
    transforms.ToTensor()  # Convert to PyTorch tensor
])

def VideoPrediction(model,device,classes,videoFolder,outFolder):
    assert os.path.isdir(videoFolder), "Video folder path is not valid."
    assert os.path.isdir(outFolder), "Output folder path is not valid."
    
    # List all files in the video folder
    video_files = [f for f in os.listdir(videoFolder) if f.endswith('.mp4')]
    
    for video_file in video_files:
        video_path = os.path.join(videoFolder, video_file)
        out_path = os.path.join(outFolder, f"processed_{video_file}")
        
        singleVideoPrediction(model, device, classes, video_path, out_path)
        

def singleVideoPrediction(model,device,classes:str,videoPath:str,outPath:str=""):
    assert isfile(videoPath) and videoPath.endswith("mp4"),"Video is not Supported, Check is that filename is proper, and File Must be mp4 format"
    assert outPath.endswith("mp4"),"Video is not Supported, Check is that filename is proper, and File Must be mp4 format"
    
    accident_index = []
    
    # Load video file
    Idlecap = cv2.VideoCapture(videoPath)
    
    length = int(Idlecap.get(cv2.CAP_PROP_FRAME_COUNT))
    del Idlecap
    
    Bar = tqdm(total=length,desc=videoPath.split("/")[-1])
    
    
    cap = MyVideoCapture(videoPath)
    
    
    # Define the output video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outPath, fourcc, 20.0, constants.RESIZE_FACTOR)
    model.eval()
    
    framecount = 1
    noAccidentFrameCount = 0


    def process(cap,index):
        cap = MyVideoCapture(videoPath)
        start_frame = index[0]
        end_frame = index[-1]
        
        
        def get_video_frame():
            frames = cap.get_frames_within_range(start_frame,end_frame)
            if len(frames) > 1:
                file_name = f"video_{start_frame}_{end_frame}.mp4"
                save_video(frame_list=frames,dst=os.path.join("TelegramAlertVideos_CCTV",file_name))
                resp = send_video(file_name=file_name)
                if resp == 200:
                    print("Sent Successfully")
                    pass
                else:
                    print("Sending Failed!")
            else:
                print("frame list is lesser than 1")
            
        my_thread2 = threading.Thread(target=get_video_frame,)
        my_thread2.start()
        
        # del index
        
       

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = torch.Tensor(cv2.resize(frame,constants.RESIZE_FACTOR)/255).permute(2,0,1)

        frame = torch.tensor(img*255, dtype=torch.uint8)

        with torch.no_grad():
            prediction = model([img.to(device)])

        pred = prediction[0]
        boxes = pred["boxes"].cpu().numpy()
        labels = pred["labels"].cpu()
        scores = pred["scores"].cpu()

        frame = frame.permute(1,2,0).numpy()
        
        isAccident = False
        
        for bbox,label,score in zip(boxes,labels,scores):
            if score > constants.CONFIDENCE_THRESHOLD:
                xmin,ymin,xmax,ymax = list(map(int,(bbox)))
                className = classes[label.item()]
                if className == "Accident":
                    isAccident = True
                
                    if round(score.item(),2)*100 <= 95:
                        continue
                else:
                    isAccident = False
                        
                color1 = (0, 255, 255)
                color2 = (10, 0, 255)

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color1, 2)
                cv2.putText(frame, f"{className} :{round(score.item(),2)*100}%", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color2, 1)
        
        if isAccident:
            accident_index.append(framecount)
            noAccidentFrameCount = 0
        
        else:
            noAccidentFrameCount += 1
        
        if noAccidentFrameCount >=10 and len(accident_index) > 1 :
            tmp_accident_index = accident_index.copy()
            accident_index.clear()
            
            if len(tmp_accident_index) > 1:
                my_thread = threading.Thread(target=process,args=[cap,tmp_accident_index,])
                my_thread.start()
            
            noAccidentFrameCount = 0
            

            
        # Write the processed frame to the output video
        out.write(frame)
        Bar.update(1)
        framecount += 1
    
    # Release video capture and writer objects
    cap.release()
    out.release()




def singleImagePrediction(model,device,classes:str,imagePath:str,outPath:str=""):
    assert isfile(imagePath) and imagePath.endswith("jpg"),"Video is not Supported, Check is that filename is proper, and File Must be jpg format"
    assert outPath.endswith("jpg"),"Image is not Supported, Check is that filename is proper, and File Must be jpg format"
    
    # Load video file
    length = 1
    Bar = tqdm(total=length,desc=imagePath.split("/")[-1])
    imageData = cv2.imread(imagePath)
    img = cv2.resize(imageData,constants.RESIZE_FACTOR)
    frame = img.copy()
    img = img/255
    img = torch.as_tensor(img, dtype=torch.float32)
    img = img.permute(2,0,1)
    
    with torch.no_grad():
        prediction = model([img.to(device)])

    # You can access the predictions, which include bounding boxes, labels, and scores
    boxes = prediction[0]['boxes']
    labels = prediction[0]['labels']
    scores = prediction[0]['scores']


    for bbox,label,score in zip(boxes,labels,scores):
        if score > constants.CONFIDENCE_THRESHOLD:
            xmin,ymin,xmax,ymax = list(map(int,(bbox)))
            className = classes[label.item()]
            if className == "Accident":
                
                if round(score.item(),2)*100 <= 95:
                    continue
            color1 = (0, 255, 255)
            color2 = (10, 0, 255)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color1, 2)
            cv2.putText(frame, f"{className} :{round(score.item(),2)*100}%", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color2, 1)
    Bar.update(1)
    cv2.imwrite(outPath,frame)
    print(f"\nPrediction Saved : {outPath}")
    