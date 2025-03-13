const signupForm = document.querySelector("form");

signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(signupForm);
    const data = new URLSearchParams(formData);

    try {
        const response = await fetch("/signup", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: data
        });

        if (response.ok) {
            alert("Signup successful! Redirecting to login...");
            window.location.href = "/login";
        } else {
            const errorText = await response.text();
            alert(`Signup failed: ${errorText}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});
