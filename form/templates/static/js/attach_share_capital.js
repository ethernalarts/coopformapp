
// Get the fileupload field
var fileupload = document.getElementById("attach_share_capital");

// Get the radio tag that opens the fileupload field
var opentag = document.getElementById("id_nature_registration_0");

// Get the radio tag that closes the fileupload field
var closetag = document.getElementById("id_nature_registration_1");

// When the user clicks "opentag", open the fileupload field 
opentag.onclick = function () {
    fileupload.style.display = "block";
}

// When the user clicks "closetag", close the fileupload field
closetag.onclick = function () {
    fileupload.style.display = "none";
}