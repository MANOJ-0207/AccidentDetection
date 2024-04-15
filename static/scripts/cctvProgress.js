var fileName;

var count = 0;
var detectedDiv = document.getElementById("detected");
var intervalId = setInterval(fetchProgress, 2000);
var conversionInterval;
document
  .getElementById("outputButton")
  .addEventListener("click", function (e) {
    e.preventDefault();
    var outputVideo = document.getElementById("outputVideo");
    outputVideo.load();
    const sectionId = this.getAttribute("href");
    document.querySelector(sectionId).scrollIntoView({
      behavior: "smooth",
    });
  });

function displayHiddenInfo(count) {
  document.getElementById("countResult").innerText = count;
  document.getElementById("outputButton").style.display = "block";
  if (count == 0)
    document.getElementById("positiveResult").style.display = "block";
  else document.getElementById("alertResult").style.display = "block";
}

function hideProgressBar() {
  var progressBar = document.getElementById("progressBar");
  var completionText = document.createElement("h2");
  completionText.innerText = "Processing Completed";
  completionText.classList.add("completionText");
  progressBar.parentNode.appendChild(completionText);
  progressBar.parentNode.removeChild(progressBar);
}

function initiateConvert()
{
  fetch('/convert', {
    method: 'POST',
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse response body as JSON
  })
  .then((data) => {
    console.log(data); // Handle response data
  })
  .catch((error) => {
    console.error('There was a problem with the Starting Convert:', error);
  });
}

function updateProgress(data) {
  var countDiv = document.getElementById("count");
  var progress = document.getElementById("progress");
  console.log("Percentage:", data.percentage);
  console.log("Count:", data.count);
  countDiv.innerText = data.count;
  progress.style.width = data.percentage;
  document.getElementById("progressText").innerText = data.percentage;
}

function getConversionStatus()
{
  fetch("/conversionStatus")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if(data.status == "completed")
        {
          clearInterval(conversionInterval);
          document.getElementById("outputContainer").style.display = "block"
          var outputVideo = document.getElementById("outputVideo");
          outputVideo.load();
        }
      })
      .catch((error) => {
        console.log("Error fetching Progress: ", error);
      });
}
var completed = false;
function fetchProgress() 
{
    fetch("/getProgressPercentage")
      .then((response) => response.json())
      .then((data) => 
      {
        if (count == 0) {
          count = data.count;
          if (count) {
            detectedDiv.innerText = "Accident Detected";
            detectedDiv.style.color = "Red";
          }
        }
        if (data.percentage == "100%") 
        {
          if(!completed)
          {
            completed = true;
            console.log("End");
            clearInterval(intervalId);
            hideProgressBar();
            displayHiddenInfo(count);
            initiateConvert();
            conversionInterval = setInterval(getConversionStatus, 2000);
          }
        } else 
        {
          updateProgress(data);
        }
      })
      .catch((error) => {
        console.log("Error fetching Progress: ", error);
      });
}
