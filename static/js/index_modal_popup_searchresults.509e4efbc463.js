
// Get the modal
var index_search_modal = document.getElementById("index-search-modal");

// Get the button that opens the modal
var open_index_result_modal = document.getElementById("open-index-results-modal");

// Get the button (X) element that closes the modal
var close_index_result_modal = document.getElementById("close-index-results");

// When the user clicks the button, open the modal 
open_index_result_modal.onclick = function () {
    index_search_modal.style.display = "block";
}

// When the user clicks on <button> (x), close the modal
close_index_result_modal.onclick = function () {
    index_search_modal.style.display = "none";
}