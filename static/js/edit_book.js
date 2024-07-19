// select the input elments from the html to pre-fill them with the book's old data
let title = document.getElementById("title");
let isbn = document.getElementById("isbn");
let pageCount = document.getElementById("pageCount");
let thumbnailUrl = document.getElementById("thumbnailUrl");
let shortDescription = document.getElementById("shortDescription");
let longDescription = document.getElementById("longDescription");
let statuss = document.getElementById("status");
let authors = document.getElementById("authors");
let categories = document.getElementById("categories");
//when the html loads, put values inside the text fields.
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
