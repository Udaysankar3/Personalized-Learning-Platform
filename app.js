
function validateUsername(username) {
    const usernameError = document.getElementById("username-error");


    if (!username.includes("@")) {
        usernameError.textContent = "Username must contain '@'.";
        return false;
    }

    usernameError.textContent = "";  
    return true;
}

function validatePassword(password) {
    const passwordError = document.getElementById("password-error");


    if (password === "") {
        passwordError.textContent = "Password cannot be empty.";
        return false;
    }

    passwordError.textContent = ""; 
    return true;
}

document.getElementById("login-btn").addEventListener("click", function () {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;


    if (validateUsername(username) && validatePassword(password)) {
        alert("Login successful");
    } else {
        alert("Please check the username and password.");
    }
});

document.getElementById("register-btn").addEventListener("click", function () {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

 
    if (validateUsername(username) && validatePassword(password)) {
        alert("Registration successful");
    } else {
        alert("Please check the username and password.");
    }
});
