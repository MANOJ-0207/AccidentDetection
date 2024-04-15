import matplotlib.pyplot as plt
import json

def saveLossGraph(lossJson:str,outPath:str="Loss.jpg"):
    assert outPath.endswith(".jpg") or outPath.endswith(".png"),"Output Image should ends with image extension. (i.e) Loss.jpg, Loss.png"
    with open(lossJson,"r") as f:
        info = json.load(f)

        plt.plot(info["trainLoss"],label="train")
        plt.plot(info["valLoss"],label="val")

        plt.title("Train Val Curve")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()
        plt.savefig(outPath)
        
        print(f"Loss Graph saved! : {outPath}")        