document.getElementById('fileInputBtnCCTV').addEventListener('click', function() {
    document.getElementById('fileInputCCTV').click();
  });

  document.addEventListener('DOMContentLoaded', function() 
  {
    var selectInputCCTV = document.getElementById('inputType');
    var infoButton = document.getElementById('fileInputBtnCCTV');
  
    // Add event listener to select element
    selectInputCCTV.addEventListener('change', function() 
    {
      if (selectInputCCTV.value === 'videos') {
        // Hide the info button
        infoButton.style.display = 'none';
        selectInputCCTV.style.width = '100%';
      } else {
        // Show the info button
        infoButton.style.display = 'inline-block';
        selectInputCCTV.style.width = '75%';
      }
    });
  });



  const loginText = document.querySelector(".title-text .cctv");
  const loginForm = document.querySelector("form.cctv");
  const loginBtn = document.querySelector("label.cctv");
  const dashCamBtn = document.querySelector("label.dashCam");
  const dashCamLink = document.querySelector("form .dashCam-link a");
  dashCamBtn.onclick = (() => {
    loginForm.style.marginLeft = "-50%";
    loginText.style.marginLeft = "-50%";
  });
  loginBtn.onclick = (() => {
    loginForm.style.marginLeft = "0%";
    loginText.style.marginLeft = "0%";
  });
  
function formValidation()
{
  var fileName = document.getElementById("fileInputCCTV").value;
  var inputType = document.getElementById('inputTypeCCTV').value;
  if(fileName == '' && inputType != 'videos')
  {
    Swal.fire({
      title: "No File Chosen!!",
      text: "Choose a file to check and process!",
      icon: "question"
    });
    return false;
  }
  return true;
}