async function translateText() {
    const inputText = document.getElementById('inputText').value.trim();
    const loadingBar = document.getElementById('loadingBar');
    const outputText = document.getElementById('outputText');

    if (!inputText) {
        outputText.innerText = "Please enter text.";
        return;
    }

    loadingBar.style.display = 'block';
    outputText.innerText = '';

    try {
        const response = await fetch('/textToSign/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText })
        });
        const data = await response.json();
        outputText.innerText = data.translation || "Translation not available.";
    } catch (error) {
        outputText.innerText = 'Error translating text. ' + error;
    } finally {
        loadingBar.style.display = 'none';
    }
}

function startRecognition(language) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = language === 'en' ? 'en-US' : 'hi-IN';

    recognition.onresult = function (event) {
        document.getElementById('inputText').value = event.results[0][0].transcript;
    };

    recognition.start();
}


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
