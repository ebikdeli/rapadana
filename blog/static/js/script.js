var full = false;
var darkmode = false;
var page = document.getElementById("page");
var content = document.getElementById("Content");

function toggle() {
  full = !full;
  if (full) {
    page.style.maxWidth = "100%";
    page.style.borderRadius = "0";
    page.style.fontSize = "25px";
    content.style.maxWidth = "100%";
    $("i").removeClass("fa-solid fa-magnifying-glass-plus").addClass("fa-solid fa-magnifying-glass-minus");
  } else {
    page.style.maxWidth = "900px";
    page.style.borderRadius = "3em";
    page.style.fontSize = "16px";
    $("i").removeClass("fa-solid fa-magnifying-glass-minus").addClass("fa-solid fa-magnifying-glass-plus");
  }
}
function myFunction() {
  darkmode = !darkmode;
  if (darkmode) {
    page.style.backgroundColor = "black";
    page.style.color = "white";
    document.body.style.backgroundColor = "black";
    element.classList.toggle("dark-mode");
    element.classList.toggle;
  } else {
    page.style.backgroundColor = "white";
    page.style.color = "black";
    document.body.style.backgroundColor = "white";
  }
}

// var backgrounds = {
//   spring: "linear-gradient(-20deg, #00cdac 0%, #8ddad5 100%)",
//   summer: "linear-gradient(120deg, #f6d365 0%, #fda085 100%)",
//   autumn: "linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%)",
//   winter: "linear-gradient(120deg, #89dafe 0%, #66a6ff 100%)",
//   celebrate: "linear-gradient(217deg, rgba(255,0,0,.8), rgba(255,0,0,0) 70.71%),linear-gradient(127deg, rgba(0,255,0,.8), rgba(0,255,0,0) 70.71%),linear-gradient(336deg, rgba(0,0,255,.8), rgba(0,0,255,0) 70.71%)",
// };

// function selectBackground(value) {
//   document.body.style.backgroundImage = backgrounds[value];
//   document.body.style.backgroundAttachment = "fixed";
// }

// var fonts = {
//   Lato: "Lato, sans-serif",
//   "Source Sans Pro": "Source Sans Pro, sans-serif",
// };

// function selectFont(value) {
//   document.documentElement.style.fontFamily = fonts[value];
// }

// // Get the modal
// var modal = document.getElementById("myModal");

// // Get the image and insert it inside the modal - use its "alt" text as a caption
// var img = document.getElementById("myImg");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
// img.onclick = function () {
//   modal.style.display = "block";
//   modalImg.src = this.src;
//   modalImg.alt = this.alt;
//   captionText.innerHTML = this.alt;
// };

// // When the user clicks on <span> (x), close the modal
// modal.onclick = function () {
//   img01.className += " out";
//   setTimeout(function () {
//     modal.style.display = "none";
//     img01.className = "modal-content";
//   }, 400);
// };
