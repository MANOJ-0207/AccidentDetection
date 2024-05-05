from tokenize import Token
import requests
import os



TOKEN_KEY = "6617892742:AAEyuXgIDrTSLGeVUdMN45Bx41lJuKo55dY"
chatid = "@AccidentMonitorControlRoom"


def send_image(file_name):
    
    path = os.path.join('TelegramAlertVideos_CCTV',file_name)
    if os.path.isfile(path):
        fil = {'photo':open(path,'rb')}
        if os.path.exists(path):
            resp = requests.post("https://api.telegram.org/bot{0}/sendPhoto?chat_id={1}".format(TOKEN_KEY,chatid),files=fil)
        return resp.status_code
    else:
        return 400

def send_video(file_name):
    path = os.path.join('TelegramAlertVideos_CCTV', file_name)
    video = {'video': open(path, 'rb')}
    
    if os.path.exists(path):
        url = f"https://api.telegram.org/bot{TOKEN_KEY}/sendVideo?chat_id={chatid}"
        resp = requests.post(url, files=video)
        return resp.status_code
    else:
        print(f"Error: File not found - {path}")
        return 400
    
def send_location(file_name):
    latitude, longitude = get_current_location()
    if latitude is not None and longitude is not None:    
        url = f"https://api.telegram.org/bot{TOKEN_KEY}/sendLocation?chat_id={chatid}&latitude={latitude}&longitude={longitude}"
        resp = requests.post(url, files=video)
        return resp.status_code
    else:
        print(f"Error: Unable to track Location.")
        return 400