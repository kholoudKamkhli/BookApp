//using local storage to get the username of logged in user and show it in the navBar
const navBar = document.getElementById("nav-admin");
const navBar2 = document.getElementById("nav-user");
const username = localStorage.getItem("email");
const new_item = document.createElement("li");
new_item.innerText = username;
new_item.className = "nav-item text-white justify-content-center mt-2";
if (navBar2!=null){
    navBar2.appendChild(new_item);
}
else if (navBar!=null){
    navBar.appendChild(new_item);
}
const btn = document.getElementById("btn");
btn.addEventListener('click', (event) => {
    localStorage.setItem("email","");

});