const email = document.getElementById("email");
const register = document.getElementById("register");

register.addEventListener("click",function(){
    const mail = email.value;
    localStorage.setItem("email",mail);
})