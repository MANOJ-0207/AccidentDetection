from flask import Flask, render_template, request, Response, redirect, url_for, jsonify
import subprocess
import re
import os
from src import clear_folder
from src import convert_to_browser_friendly_mp4
from pyngrok import ngrok

ngrok.set_auth_token("2f8N7x3HnRhSNIDqfkzMM9GD79e_6Ly7Ea79QGn8FxiZmMxf4")
public_url=ngrok.connect(5000).public_url
print(public_url)

app = Flask(__name__)


previousProgress = "0%"
fileName = "1.mp4"
process = None
started = False
def extract_progress(line):
    match = re.search(r'\d+%|\d+\.\d+%', line)
    if match:
        return match.group()
    return None



@app.route("/convert",  methods=['POST'])
def convert():
    global fileName
    convert_to_browser_friendly_mp4(fileName)
    return jsonify({"message": "Conversion process started successfully."}), 200
    
    
@app.route("/conversionStatus", methods=['GET'])
def getConversionStatus():
    directory = 'static/resources/videos/Output_Videos/Singly_Processed_Videos/BrowserVideos'
    search_file = "Browser"+fileName
    file_path = os.path.join(directory, search_file)
    if(os.path.isfile(file_path)):
        return jsonify({"status" : "completed"})
    else:
        return jsonify({"status" : "pending"})

@app.route("/getProgressPercentage" , methods=['GET'])
def generate_progress():
    global process
    count = len(os.listdir("TelegramAlertVideos_CCTV")) - 1
    if(process is not None):
        if(process.poll()):
            return jsonify({"percentage": "100%", "count" : count})
        global started
        global previousProgress
        global progress_output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                percentage = extract_progress(output)
                if percentage:
                    started = True
                    previousProgress = percentage
                    return jsonify({"percentage": percentage, "count": count })
    return jsonify({"percentage": previousProgress, "count" : count})

@app.route("/getCompletionStatus", methods=['GET'])
def getProcessStatus():
    global process
    count = len(os.listdir("TelegramAlertVideos_CCTV")) -1 
    if(process is None):
        return jsonify({"status" : "none","count" : count})
    elif(process.poll() is None):
        return jsonify({"status" : "running", "count" : count})
    return jsonify({"status" : "complete", "count" : count})    

@app.route("/image")
def image():
    global fileName
    return render_template('ImageOutput.html' , imageUrl = fileName)           

@app.route("/imageProgress")
def imageProgress():
    global process
    if process and process.poll() is None:
        return jsonify({'status': 'running'})
    else:
        return jsonify({'status': 'completed'})
    
# @app.route("/cctvFileName", methods = ['GET'])
# def cctvFileName():
#     return jsonify({"fileName": fileName})


@app.route("/videoProgress" )
def videoProgress():
    global fileName
    return render_template('ProgressPageCCTV.html' , videoUrl = fileName)

@app.route("/folderOutput" )
def folderOutput():
    return render_template('FolderProgress.html')

@app.route("/")
def home_page():
    clear_folder("TelegramAlertVideos_CCTV")
    return render_template('HomePage.html')


@app.route("/cctv", methods=['POST'])
def cctv():
    global process
    if(process is not None):
        if(process.poll() is not None):
            process.kill()
    global fileName
    runMode = request.form['runMode']
    inputType = request.form['inputType']
    fileName = request.form['fileInputCCTV']
    arguments = [runMode, inputType, fileName]
    process = subprocess.Popen(['python', 'test.py']+ arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if(inputType == "image"):
        return redirect(url_for('image'))
    else:
        return redirect(url_for('videoProgress'))





# @app.route("/values", methods = ['POST'])
# def values():
#     runMode = request.form['runMode']
#     inputType = request.form['inputType']
#     fileName = request.form['fileInputCCTV']
#     response_content = f"Run Mode: {runMode}\nInput Type: {inputType}\nFile Name: {fileName}"
#     return response_content


if __name__ == "__main__":
    app.run(port = 5000)

