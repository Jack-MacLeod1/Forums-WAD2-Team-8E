const dropArea = document.getElementsByTagName("p")[1];
const inputFile = document.getElementById("id_image");
const imageView = document.getElementById("id_image");

// Credit to https://www.youtube.com/watch?v=5Fws9daTtIs

inputFile.addEventListener("change", uploadImage);

function uploadImage(){
    
    imageView.parentNode.querySelectorAll("img").forEach(img => img.remove()); // Used in the "swapping" of images if more than one is uploaded - we only want 1
    let imgLink = URL.createObjectURL(inputFile.files[0]);

    let img = document.createElement("img");
    img.src = imgLink;
    img.style.maxWidth = "500px"; // Ensure the image fits in the space
    img.style.maxHeight = "190px";
    img.style.objectFit = "contain";

    imageView.parentNode.appendChild(img);
}

dropArea.addEventListener("dragover", function(e){
    e.preventDefault();
});

dropArea.addEventListener("drop", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    uploadImage(); 
});