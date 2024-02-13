
// Get the fileupload field
var byelawsupload = document.getElementById("attach_bye_laws");

// Get the radio tag that opens the fileupload field
var openbyelaw = document.getElementById("id_openbyelaw");

// Get the radio tag that closes the fileupload field
var closebyelaw = document.getElementById("id_closebyelaw");

// When the user clicks "opentag", open the fileupload field 
openbyelaw.onclick = function () {
    byelawsupload.style.display = "block";
}

// When the user clicks "closetag", close the fileupload field
closebyelaw.onclick = function () {
    byelawsupload.style.display = "none";
}