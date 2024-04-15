## Accident Detection & Alert System

## Install & Dependencies
- python
- pytorch
- numpy
- opencv

  ## Installation

  ```
  pip install -r requirements.txt
  ```

## Use
- for train
  ```
  python train.py
  ```
- for test
  ```
  python test.py
  ```


## Directory Hierarchy
```
|—— .gitignore
|—— dataset
|    |—— annotations
|        |—— instances_default.json
|    |—— images
|        |—— accident_1.jpg
|        |—— accident_10.jpg
|        .
|        .
|        .
|    |—— info.txt
|    |—— train.json
|    |—— val.json
|—— dataset.py
|—— models
|    |—— loss.json
|    |—— model_22_loss_0.072028_val_loss_0.147941.torch
|    |—— model_39_loss_0.045951_val_loss_0.155342.torch
|—— requirements.txt
|—— static
|    |—— css
|    |   |—— home.css
|    |   |—— image.css
|    |   |—— progressCCTV.css
|    |—— resources
|    |   |—— videos
|    |   |    |—— Accident_Test_Videos
|    |   |    |—— Output_Videos
|    |   |        |—— Output_Videos
|    |   |        |—— Singly_Processed_Videos
|    |   |            |—— ProcessedVideos
|    |   |            |—— BrowserVideos
|    |   |        |—— Collectively_Processed_Videos
|    |   |            |—— ProcessedVideos
|    |   |            |—— BrowserVideos
|    |   |—— images
|    |        |—— Input_Images
|    |        |—— Output_Images
|    |—— scripts
|        |—— cctvProgress.js
|        |—— Home.js
|        |—— image.js
|—— src
|    |—— constants.py
|    |—— converter.py
|    |—— loss_curve.py
|    |—— test_utils.py
|    |—— train_utils.py
|    |—— utils.py
|    |—— __init__.py
|—— TelegramAlertVideos_CCTV
|—— templates
|    |—— HomePage.html
|    |—— ImageOutput.html
|    |—— ProgressPage.html
|—— test.py
|—— train.py
|—— flaskServer.py
|—— saveLossDiagram.py
```
