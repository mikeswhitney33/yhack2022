// sample upload method from 260 - may need to update to get functional
/*
async upload() {
  try {
    const formData = new FormData();
    formData.append('photo', this.file, this.file.name);
    formData.append('title', this.title);
    formData.append('description', this.description);
    await axios.post("/api/photos", formData);
    this.file = null;
    this.url = "";
    this.title = "";
    this.description = "";
    this.$emit('uploadFinished');
  } catch (error) {
    this.error = "Error: " + error.response.data.message;
  }
} */
//import axios from 'axios';

function yes() {
  // indicate that the image was liked
  var x = document.getElementById("toast");
  x.className = "show";
  var text = document.getElementById("text");
  text.innerHTML = "The yes button was clicked";
  //alert("Hello World");
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

}

function no() {
  // indicate that the image was disliked
  var x = document.getElementById("toast");
  x.className = "show";
  var text = document.getElementById("text");
  text.textContent = "The no button was clicked";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

}
/*
<input type="file" id="imageInput" name="imageInput" accept="image/png, image/jpg">
<label for="imageInput">Select Image</label>
<div id="imagePreview"><img src="" alt="" id="uploadedImage"></div>
<button type="submit" onclick="upload" id=uploadButton>Upload</button><br>

window.addEventListener('load', function() {
  document.querySelector('input[type="file"]').addEventListener('change', function() {
      if (this.files && this.files[0]) {
          var img = document.querySelector('img');
          img.onload = () => {
              URL.revokeObjectURL(img.src);  // no longer needed, free memory
          }

          img.src = URL.createObjectURL(this.files[0]); // set src to blob url
      }
  });
});
*/
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
if(imageInput != null) {
  alert("testing");
  imageInput.addEventListener("change", function () {
    alert("image changed");
    getImgData();
  });
} else {
  alert("error: not getting image Input");
}

function getImgData() {
  const files = imageInput.files[0];
  if(files) {
    const fileReader = new fileReader();
    fileReader.readAsDataURL(files);
    fileReader.addEventListener("load", function () {
      alert("image loaded");
      imgPreview.style.display = "block";
      imgPreview.innerHTML = '<img src="' + this.result + '" />';
    });
  }
}

function upload() {

  document.getElementById("imageInput").addEventListener('change', function() {
    if(this.files && this.files[0]) {
      var img = document.getElementById("uploadedImage")
      //img.onload = () => {
        //URL.revokeObjectURL(img.src);
        // supposed to free memory, not certain if it is creating a race condition
      //}
      img.src = URL.createObjectURL(this.files[0]);
    }
  })
}
