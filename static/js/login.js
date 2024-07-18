const email = document.getElementById("email");
const login = document.getElementById("login");

register.addEventListener("click",function(){
    const mail = email.value;
    localStorage.setItem("email",mail);
})