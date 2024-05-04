var detectedDiv = document.getElementById("detected");
var countDiv = document.getElementById("count");
var intervalId = setInterval(fetchProgress, 2000);

function displayHiddenInfo(count) 
{
    document.getElementById("countResult").innerText = count;
    if (count == 0)
      document.getElementById("positiveResult").style.display = "block";
    else 
        document.getElementById("alertResult").style.display = "block";
}
var count = 0;
function fetchProgress() 
{
    fetch("/getCompletionStatus")
      .then((response) => response.json())
      .then((data) => 
      {
        console.log(data);
        count = data.count;
        if (count) 
        {
          countDiv.innerHTML = count;
          detectedDiv.innerText = "Accident Detected";
          detectedDiv.style.color = "Red";
        }
        if (data.status == "complete") 
        {
          clearInterval(intervalId);
          document.getElementById("processStatus").innerHTML = "Completed";
          document.getElementById("result").style.display = "block";
          document.getElementById("processStatus").style.color = " #4caf50;";
        } 
      })
      .catch((error) => {
        console.log("Error fetching Progress: ", error);
      });
}


