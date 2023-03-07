const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

function checkACookieExists() {
  if (
    document.cookie.split(";").some((item) => item.trim().startsWith("loginCookie="))
  ) {
    window.location = "http://www.google.com/"
  }
}

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "user" && password === "web_dev") {
        alert("You have successfully logged in.");
        document.cookie = loginCookie;max-age=86400
        location.reload();
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})