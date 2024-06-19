document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("#login-form");
    const signupForm = document.querySelector("#signup-form");
    const passwordInput = document.getElementById("password");
    const passToggleBtn = document.getElementById("pass-toggle-btn");

    // Function to display error messages
    const showError = (field, errorText) => {
        field.classList.add("error");
        const errorElement = document.createElement("small");
        errorElement.classList.add("error-text");
        errorElement.innerText = errorText;
        field.closest(".input-box").appendChild(errorElement);
    }

    // Function to handle login form submission
    const handleLoginForm = (e) => {
        e.preventDefault();
        const emailInput = document.getElementById("email");
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Regular expression pattern for email validation
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        // Clearing previous error messages
        document.querySelectorAll(".input-box .error").forEach(field => field.classList.remove("error"));
        document.querySelectorAll(".error-text").forEach(errorText => errorText.remove());

        // Performing validation checks
        if (!emailPattern.test(email)) {
            showError(emailInput, "Enter a valid email address");
        }
        if (password === "") {
            showError(passwordInput, "Enter your password");
        }
        // Checking for any remaining errors before form submission
        const errorInputs = document.querySelectorAll(".input-box .error");
        if (errorInputs.length > 0) return;

        // Login form validation logic here
        // Example: Validate email and password
        // If validation passes, submit the form
        loginForm.submit();
    }

    // Function to handle signup form submission
    const handleSignupForm = (e) => {
        e.preventDefault();

        // Signup form validation logic here
        // Example: Validate all fields and passwords match
        // If validation passes, submit the form
        const nameInput = document.getElementById("name");
        const emailInput = document.getElementById("email");
        const idInput = document.getElementById("id");
        const companyInput = document.getElementById("company");
        const confirmPasswordInput = document.getElementById('confirmPassword');

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const id = idInput.value.trim();
        const company = companyInput.value.trim();
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        

        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        document.querySelectorAll(".input-box .error").forEach(field => field.classList.remove("error"));
        document.querySelectorAll(".error-text").forEach(errorText => errorText.remove());

        if (name === "") {
            showError(nameInput, "Enter your name");
        }
        if (!emailPattern.test(email)) {
            showError(emailInput, "Enter a valid email address");
        }
        if (id === "") {
            showError(idInput, "Enter your ID");
        }
        if (company === "") {
            showError(companyInput, "Enter your company name");
        }
        if (password === "") {
            showError(passwordInput, "Enter your password");
        }
        
        if (confirmPassword === "") {
            showError(confirmPasswordInput, "Confirm your password");
        } else if (confirmPassword !== password) {
            showError(confirmPasswordInput, "Passwords do not match");
        }
       // Checking for any remaining errors before form submission
       const errorInputs = document.querySelectorAll(".input-box .error");
       if (errorInputs.length > 0) return;
        
        signupForm.submit();
    }

    // Password toggle functionality
    passToggleBtn.addEventListener('click', () => {
        passToggleBtn.classList.toggle("bx-show");
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    });

    // Add event listener for login form submission
    if (loginForm) {
        loginForm.addEventListener("submit", handleLoginForm);
    }

    // Add event listener for signup form submission
    if (signupForm) {
        signupForm.addEventListener("submit", handleSignupForm);
    }
});


    // Wrap your code in an immediately invoked function expression (IIFE)
    document.addEventListener("DOMContentLoaded", function() {
        const menuBtn = document.querySelector(".menu-btn");
        const sidebar = document.querySelector(".sidebar");
    
        if (menuBtn && sidebar ) {
            menuBtn.addEventListener("click", function() {
                
                sidebar.classList.toggle("active");
                
            });
        }



        const arrowIcon = document.querySelector(".arrow");
        const subMenu = document.querySelector(".sub-menu");
    
        if (arrowIcon && subMenu) {
            arrowIcon.addEventListener("click", function() {
                subMenu.classList.toggle("show");
                arrowIcon.classList.toggle("rotate");
            });
        }
    
        
    });
    