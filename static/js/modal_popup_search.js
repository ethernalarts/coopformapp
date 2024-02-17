// Get the modal
var search_modal = document.getElementById("search-modal");

// Get the button that opens the modal
var open_search_modal = document.getElementById("open-search-modal");

// Get the button (X) element that closes the modal
var close_search_x = document.getElementById("closesearch-x");

// When the user clicks the button, open the modal 
open_search_modal.onclick = function () {
    search_modal.style.display = "block";
}

// When the user clicks on <button> (x), close the modal
close_search_x.onclick = function () {
    search_modal.style.display = "none";
}