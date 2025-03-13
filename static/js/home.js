document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.querySelector(".dark-mode-toggle");

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

    // Apply dark mode when page loads
    applyDarkMode();

    toggleButton.addEventListener('click', () => {
        // Toggle between dark and light mode
        if (localStorage.getItem('darkMode') === 'enabled') {
            localStorage.setItem('darkMode', 'disabled');
        } else {
            localStorage.setItem('darkMode', 'enabled');
        }
        applyDarkMode();
    });

    // Handle "Get Started" Button Click to scroll to "Our Features"
    const getStartedButton = document.querySelector(".btn");
    if (getStartedButton) {
        getStartedButton.addEventListener("click", () => {
            document.getElementById("ourFeatures").scrollIntoView({ behavior: 'smooth' });
        });
    }
});
