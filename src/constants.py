TRAIN_ANNOTATIONS_FILE = r"dataset/train.json"
VAL_ANNOTATIONS_FILE = r"dataset/val.json"
IMAGES = r"dataset/images"

EPOCHS = 40
BATCH_SIZE = 8
DEVICE = "cpu" #"cuda","cpu"

RESIZE_FACTOR = (600,600)


INPUTDATATYPE = "videos" #image,video,videos



MODEL_PATH = r"models/model_39_loss_0.045951_val_loss_0.155342.torch"
IMAGE_PATH = [r"static/resources/images/Input_Images/","static/resources/images/Output_Images/"]
VIDEO_PATH = [r"static/resources/videos/Accident_Test_Videos/","static/resources/videos/Output_Videos/Singly_Processed_Videos/ProcessedVideos/Processed"]
FOLDER_OF_VIDEO = [r"static/resources/videos/Accident_Test_Videos","static/resources/videos/Output_Videos/Collective_Processed_Videos"]

OUTPUT_VIDEOS_PATH = r"static/resources/videos/Output_Videos/"

CONFIDENCE_THRESHOLD = 0.6


classes = [
  "__background__",
  "Accident",
  "Car",
  "Bike"
]