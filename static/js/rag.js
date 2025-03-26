document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chatBox");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const toggleSwitch = document.getElementById("darkModeToggle");

    // Dark Mode Functionality
    function switchTheme() {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
    }

    if (toggleSwitch) {
        toggleSwitch.addEventListener("click", switchTheme);
    }

    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }

    // Append message to chat box
    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender.toLowerCase());
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Send message
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("User", message);
        userInput.value = "";

        fetch("/ragLearning/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                appendMessage("Bot", data.messages[0].content);
            } else {
                appendMessage("Bot", "Sorry, I couldn't process that.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("Bot", "An error occurred.");
        });
    }

    // Event Listeners
    sendButton.addEventListener("click", sendMessage);
    
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});
