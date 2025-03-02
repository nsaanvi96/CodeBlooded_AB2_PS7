document.addEventListener("DOMContentLoaded", function() {
    // Login
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            alert("Login successful! Redirecting...");
            window.location.href = "dashboard.html";
        });
    }

    // Signup
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function(event) {
            event.preventDefault();
            alert("Signup successful! Redirecting...");
            window.location.href = "index.html";
        });
    }

    // Forgot Password
    const forgotForm = document.getElementById("forgotForm");
    if (forgotForm) {
        forgotForm.addEventListener("submit", function(event) {
            event.preventDefault();
            alert("Password reset link sent to your email!");
        });
    }
});
