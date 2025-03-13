const loginForm = document.querySelector(".form-group");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(loginForm);
    const data = new URLSearchParams(formData);

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: data
        });

        if (response.ok) {
            window.location.href = "/";
        } else {
            const errorText = await response.text();
            alert(`Login failed: ${errorText}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});


const applyDarkMode = () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        toggleButton.textContent = 'Light Mode';
    } else {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        toggleButton.textContent = 'Dark Mode';
    }
};

applyDarkMode();

toggleButton.addEventListener('click', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        localStorage.setItem('darkMode', 'disabled');
    } else {
        localStorage.setItem('darkMode', 'enabled');
    }
    applyDarkMode();
});

applyDarkMode();
