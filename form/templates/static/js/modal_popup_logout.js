// Get the modal
var modal = document.getElementById("modal");

// Get the button that opens the modal
var btn = document.getElementById("openmodal");

// Get the X <button> element that closes the modal
var button = document.getElementById("closemodal1");

// Get the second <button> element, 'No, Cancel' that closes the modal
var button2 = document.getElementById("closemodal2");

// When the user clicks the button, open the modal 
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <button> (x), close the modal
button.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks on 'No, Cancel' button, close the modal
button2.onclick = function () {
    modal.style.display = "none";
}