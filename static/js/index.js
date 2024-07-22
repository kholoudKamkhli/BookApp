if (localStorage.getItem("email") == null || localStorage.getItem("email") == "") {
    window.location.href = '/'; 
}
else{
    fetch(`/home`, {
        method: "GET",
    });
}
