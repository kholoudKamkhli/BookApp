title = document.getElementById("title");
isbn = document.getElementById("isbn");
pageCount = document.getElementById("pageCount");
thumbnailUrl = document.getElementById("thumbnailUrl");
shortDescription = document.getElementById("shortDescription");
longDescription = document.getElementById("longDescription");
statuss = document.getElementById("status");
authors = document.getElementById("authors");
categories = document.getElementById("categories");
document.addEventListener('DOMContentLoaded', (event) => {
    title.value = book.title;
    isbn.value = book.isbn;
    pageCount = book.pageCount;
    thumbnailUrl.value = book.thumbnailUrl;
    shortDescription.value = book.shortDescription ?book.shortDescription:"N/A";
    longDescription.value = book.longDescription;
    statuss.value = book.status;
    authors.value = book.authors;
    categories.value = book.categories;

});
function cancelEdit() {

    fetch(`/cancel_edit`, {
        method: "POST",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    })
}