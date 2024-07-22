// function that fetches add to favourite in the backent
function addToFavourite(bookId) {

    fetch(`/add_to_favourite/${bookId}`, {
        // specify the method to be POST
        method: "POST",
    })
    .then(response => {
        // if error occured, throw it 
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // if the book added succcessfully to favourites, alert the user
        if (data.success) {
            alert('Book added to favourites successfully!');
            setTimeout(()=>window.location.reload(), 100);
        } else {
            //if book is not added to favourites, alert the user
            alert('Failed to add book to favourites.');
        }
    });
}
// function that fetches add to favourite in the backent
function removeFavourite(bookId) {

    fetch(`/remove_favourite/${bookId}`, {
        // specify the method to be POST
        method: "POST",
    })
    .then(response => {
        // if error occured, throw it 
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // if the book added succcessfully to favourites, alert the user
        if (data.success) {
            alert('Book removed from favourites successfully!');
            setTimeout(()=>window.location.reload(), 100);
        } else {
            //if book is not added to favourites, alert the user
            alert('Failed to remove book from favourites.');
        }
    });
}
//function to fetch delete book from backend
function deleteBook(bookId) {

    fetch(`/delete_book/${bookId}`, {
        //specify the method 
        method: "POST",
    })
    .then(response => {
        //if an error has occured, throw it
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            //if the book was deleted successfully, alert the user
            alert('Book Deleted Successfully!');
            //refresh the page so that the book is deleted from it.
            setTimeout(()=>window.location.reload(), 100)
            
        } else {
            //if failed to delete book, notify the user,
            alert('Failed to Delete Book');
        }
    });
}