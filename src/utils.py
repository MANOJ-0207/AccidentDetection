import cv2
import torch
import os
def isColab():
    try:
        import google.colab 
        return True
    except ModuleNotFoundError:
        return False
    
def collate_fn(batch):
    return tuple(zip(*batch))

def clear_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # Check if the file is a video file (assuming mp4 format)
        if os.path.isfile(file_path) and file_name.endswith('.mp4'):
            # Delete the video file
            os.remove(file_path)
    print("Folder Cleared")
            
def save_video(frame_list:list,dst:str):
    try:
        if not frame_list:
            print("Error: Empty frame list.")
            return

        # Get the height and width of the frames from the first frame
        height, width, _ = frame_list[0].shape
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(dst, fourcc, 25.0, (width, height))

        if not out.isOpened():
            print("Error: Unable to open the output video file.")
            return

        # Write frames to the video
        for frame in frame_list:
            out.write(frame)

        # Release the VideoWriter
        out.release()
        print(" File_Saved!")
    except Exception:
        print("Error occured while saving!")
        
class MyVideoCapture:
    
    def __init__(self, source):
        self.filename = source
        self.cap = cv2.VideoCapture(source)
        self.idx = -1
        self.end = False
        self.stack = []
        
    def read(self):
        self.idx += 1
        ret, img = self.cap.read()
        if ret:
            self.stack.append(img)
        else:
            self.end = True
        return ret, img
    
    def to_tensor(self, img):
        img = torch.from_numpy(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return img.unsqueeze(0)
        
    def get_video_clip(self):
        assert len(self.stack) > 0, "clip length must large than 0 !"
        self.stack = [self.to_tensor(img) for img in self.stack]
        clip = torch.cat(self.stack).permute(-1, 0, 1, 2)
        del self.stack
        self.stack = []
        return clip
    
    def release(self):
        self.cap.release()

    def get_frames_within_range(self, start_frame, end_frame):
        frames = []

        if not self.cap.isOpened():
            print("Error: VideoCapture object is not initialized.")
            return frames

        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if start_frame < 0 or end_frame >= total_frames or start_frame >= end_frame:
            print("Error: Invalid start or end frame indices.")
            return frames

        buffer_size = 5  # Define the size of the buffer

        # Determine the actual start and end indices considering the buffer
        actual_start = max(0, start_frame - buffer_size)
        actual_end = min(total_frames - 1, end_frame + buffer_size)

        for i in range(actual_start, actual_end + 1):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = self.cap.read()
            if ret:
                frames.append(frame)
            else:
                print(f"Error reading frame {i}")

        # Trim the frames to fit within the specified range
        frames = frames[start_frame - actual_start:end_frame - actual_start + 1]

        return frames
