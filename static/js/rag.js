// document.getElementById('sendButton').addEventListener('click', function() {
//     const userInput = document.getElementById('userInput').value;
    
//     // Clear the input field
//     document.getElementById('userInput').value = '';

//     // Display the user's message
//     const responseDiv = document.getElementById('response');
//     responseDiv.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

//     fetch('/ragLearning/ask', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ message: userInput })
//     })
//     .then(response => response.json())
//     .then(data => {
//         const modelResponse = data.choices[0].message.content;
//         responseDiv.innerHTML += `<p><strong>Model:</strong> ${modelResponse}</p>`;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         responseDiv.innerHTML += `<p><strong>Error:</strong> Something went wrong!</p>`;
//     });
// });

import marked from 'marked';

document.getElementById('sendButton').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value;
    const chatBox = document.getElementById('chatBox');
    
    // Clear the input field
    document.getElementById('userInput').value = '';

    // Display the user's message in chat box
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Display thinking message
    const thinkingMessage = document.createElement('div');
    thinkingMessage.classList.add('message', 'bot-message');
    thinkingMessage.textContent = 'Thinking...';
    chatBox.appendChild(thinkingMessage);

    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send user input to the server
    fetch('/ragLearning/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Remove thinking message and display model response
        chatBox.removeChild(thinkingMessage);
        
        const modelResponse = data.choices[0].message.content;

        // Convert Markdown response to HTML
        const formattedResponse = marked(modelResponse);

        // Create a new message element with the formatted response
        const modelMessage = document.createElement('div');
        modelMessage.classList.add('message', 'bot-message');
        modelMessage.innerHTML = `<strong>Model:</strong> ${formattedResponse}`;  // Use innerHTML to display HTML content

        chatBox.appendChild(modelMessage);

        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        // Remove thinking message and display error
        chatBox.removeChild(thinkingMessage);
        
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('message', 'bot-message');
        errorMessage.textContent = 'Error: Something went wrong!';
        chatBox.appendChild(errorMessage);

        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});

// Optionally, allow sending the message with the Enter key
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();  // Prevent line break
        document.getElementById('sendButton').click();
    }
});


const toggleButton = document.querySelector('.dark-mode-toggle');

const applyDarkMode = () => {
    const toggleButton = document.querySelector('.dark-mode-toggle');
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

document.querySelector('.dark-mode-toggle').addEventListener('click', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        localStorage.setItem('darkMode', 'disabled');
    } else {
        localStorage.setItem('darkMode', 'enabled');
    }
    applyDarkMode();
});
