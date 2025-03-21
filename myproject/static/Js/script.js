/*---------- Function for close icon to go to the home page ----------*/

    function redirectToPage() {
        const closeIcon = document.querySelector('.close-icon');
        const redirectUrl = closeIcon.getAttribute('data-url');  // Get URL from data attribute
    
        window.location.href = redirectUrl;  // Redirect to the specified URL
    }

/*---------- Function for close icon to go to the home page ----------*/

/*---------- To disable the Resend OTP button for 30 seconds ----------*/

document.addEventListener("DOMContentLoaded", function () { 
    let resendButton = document.getElementById("resendOtpButton");
    let countdownElement = document.getElementById("countdown");
    let timerText = document.getElementById("timer");
    let countdown = 30;
    let form = resendButton.closest("form"); // Get the form containing the button

    function updateTimer() {
        if (countdown > 0) {
            countdownElement.textContent = countdown;
            countdown--;
            setTimeout(updateTimer, 1000);
        } else {
            resendButton.disabled = false; // Enable button after countdown
            timerText.style.display = "none";
        }
    }

    // Disable button initially when page loads
    resendButton.disabled = true;
    updateTimer();

    resendButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default only to handle timer
        resendButton.disabled = true; // Disable button immediately after click
        countdown = 30;
        timerText.style.display = "block";
        updateTimer();

        // Submit the form manually after disabling button
        setTimeout(() => {
            form.submit();
        }, 100); // Small delay to ensure button is disabled before form submission
    });
});

/*---------- To disable the Resend OTP button for 30 seconds ----------*/

/*---------- Script for the live filter from the search bar ----------*/



/*---------- Script for the live filter from the search bar ----------*/
