function addToFavourite(bookId) {

    console.log("inside toggle function");
    console.log(bookId);
    fetch(`/add_to_favourite/${bookId}`, {
        method: "POST",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Book added to favourites successfully!');
            document.getElementById(`heartIcon_${bookId}`).classList.add('favorited');
        } else {
            alert('Failed to add book to favourites.');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
function deleteBook(bookId) {

    fetch(`/delete_book/${bookId}`, {
        method: "POST",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Book Deleted Successfully!');
            setTimeout(()=>window.location.reload(), 100)
            // set
        } else {
            alert('Failed to Delete Book');
        }
    })
    .catch(error => {
        console.error('There was a problem with the delete operation:', error);
    });
}