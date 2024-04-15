function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  function completionCheck() {
    fetch("/imageProgress")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.status === "completed") 
        {
          wait(3000);
          clearInterval(intervalId);;
          document.getElementById("output").style.display = "flex";
          document.getElementById("customSpinner").style.display = "none";
          var outputImage = document.getElementById("outputImage");
          outputImage.src = outputImage.src;
        }
      })
      .catch((error) => {
        console.log("Error fetching File Name :", error);
      });
  }
  var intervalId = setInterval(completionCheck, 100);