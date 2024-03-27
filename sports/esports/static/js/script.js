document.addEventListener("DOMContentLoaded", function() {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    // Event listener for sign-up button
    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
        document.getElementById("signupFormContainer").classList.remove("hidden");
        document.getElementById("signinFormContainer").classList.add("hidden");
    });

    // Event listener for sign-in button
    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
        document.getElementById("signinFormContainer").classList.remove("hidden");
        document.getElementById("signupFormContainer").classList.add("hidden");
    });

    // Initially removing the 'hidden' class from sign-in form container
    document.getElementById("signinFormContainer").classList.remove("hidden");
});
