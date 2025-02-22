/*---------- Function for close icon to go to the home page ----------*/

    function redirectToPage() {
        const closeIcon = document.querySelector('.close-icon');
        const redirectUrl = closeIcon.getAttribute('data-url');  // Get URL from data attribute
    
        window.location.href = redirectUrl;  // Redirect to the specified URL
    }

/*---------- Function for close icon to go to the home page ----------*/

/*---------- To disable the Resend OTP button for 30 seconds ----------*/

    document.addEventListener("DOMContentLoaded", function () {
        let resendButton = document.getElementById("resendBtn");
        let resendTime = parseInt("{{ request.session.resend_disabled_until|default:0 }}") * 1000;
        let currentTime = new Date().getTime();
        
        if (resendTime > currentTime) {
            let remainingTime = Math.ceil((resendTime - currentTime) / 1000);
            resendButton.disabled = true;
            let countdown = setInterval(function () {
                remainingTime -= 1;
                resendButton.innerText = "Resend OTP (" + remainingTime + "s)";
                if (remainingTime <= 0) {
                    clearInterval(countdown);
                    resendButton.disabled = false;
                    resendButton.innerText = "Resend OTP";
                }
            }, 1000);
        }
    });

/*---------- To disable the Resend OTP button for 30 seconds ----------*/

/*---------- Log In page (Username and Password Validation) ----------*/

    // Client-side form validation
    /*document.getElementById('loginForm').addEventListener('submit', function (event) {
        let isValid = true;
    
        // Clear previous errors
        document.getElementById('usernameError').textContent = '';
        document.getElementById('passwordError').textContent = '';
    
        // Username validation
        const username = document.getElementById('username').value.trim();
        if (username === '') {
            document.getElementById('usernameError').textContent = 'Username is required.';
            isValid = false;
        }
    
        // Password validation
        const password = document.getElementById('password').value.trim();
        if (password === '') {
            document.getElementById('passwordError').textContent = 'Password is required.';
            isValid = false;
        } else if (password.length < 6) {
            document.getElementById('passwordError').textContent = 'Password must be at least 6 characters.';
            isValid = false;
        }
    
        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });*/

/*---------- Log In page (Username and Password Validation) ----------*/

/*function validatePassword() {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm_password").value;
    let errorSpan = document.getElementById("password_error");
    let submitButton = document.getElementById("submit_button");

    if (confirmPassword === "") {
        errorSpan.innerText = "";
        submitButton.disabled = true;
        return;
    }

    if (password !== confirmPassword) {
        errorSpan.innerText = "Passwords do not match!";
        submitButton.disabled = true;
    } else {
        errorSpan.innerText = "";
        submitButton.disabled = false;
    }
}*/