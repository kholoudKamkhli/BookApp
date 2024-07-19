console.log("index.js");
if (localStorage.getItem("email") == null || localStorage.getItem("email") == "") {
    console.log("entered here");
    window.location.href = '/'; 
}
else{
    fetch(`/home`, {
        method: "GET",
    });
}
