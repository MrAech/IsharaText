document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const clearSearchButton = document.getElementById('clearSearchButton');
    const wordList = document.getElementById('wordList');
    const toggleButton = document.querySelector('.dark-mode-toggle');
    let player; 
    let currentVideoId = '';
    let currentPage = 1;
    const itemsPerPage = 100;

    const tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    window.onYouTubeIframeAPIReady = function () {
        player = new YT.Player('player', {
            height: '640',
            width: '390',
            videoId: '', 
            playerVars: { 
                playsinline: 1,
                rel: 0, 
                autoplay: 1,
                controls: 0 
            },
            events: {
                'onStateChange': onPlayerStateChange
            }
        });
    };

    function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.ENDED) {
            player.loadVideoById(currentVideoId);
        }
    }

    const leftPanel = document.getElementById('leftPanel');
    const rightPanel = document.getElementById('rightPanel');
    const playerElement = document.getElementById('player');

    // Function to set the initial sizes
    // const setInitialSizes = () => {
    //     const container = document.getElementById('container');
    //     const leftPanelWidth = leftPanel.offsetWidth;

    //     // Set the right panel width based on the left panel width
    //     rightPanel.style.width = `calc(100% - ${leftPanelWidth}px)`;
    //     playerElement.style.width = '100%';
    //     playerElement.style.height = `${(rightPanel.offsetWidth * 9) / 16}px`; // Maintain 16:9 aspect ratio
    // };

    const setInitialSizes = () => {
        const leftPanelWidth = leftPanel.offsetWidth;
        rightPanel.style.width = `calc(100% - ${leftPanelWidth}px)`;
        playerElement.style.width = '100%';
        playerElement.style.height = `${Math.max(400, rightPanel.offsetHeight - 50)}px`; // Ensures a good height
    };
    

    // Call the function to set initial sizes
    setInitialSizes();

    // Resize event listener
    window.addEventListener('resize', setInitialSizes);

    function loadPage(page) {
        fetch(`/dictionary/api/paginate?page=${page}&items_per_page=${itemsPerPage}`)
            .then(response => response.json())
            .then(data => {
                wordList.innerHTML = '';
                for (const [key, value] of Object.entries(data.items)) {
                    const gridItem = document.createElement('div');
                    gridItem.className = 'grid-item';
                    gridItem.innerHTML = `<a href="#" class="video-link" data-video-id="${value}">${key}</a>`;
                    wordList.appendChild(gridItem);
                }
                document.getElementById('pageInfo').textContent = `Page ${data.page}`;
                document.getElementById('prevPage').disabled = data.page === 1;
                document.getElementById('nextPage').disabled = data.page * itemsPerPage >= data.total;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

    loadPage(currentPage);

    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadPage(currentPage);
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        currentPage++;
        loadPage(currentPage);
    });

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        fetch(`/dictionary/api/search?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(results => {
                wordList.innerHTML = '';
                for (const [key, value] of Object.entries(results)) {
                    const gridItem = document.createElement('div');
                    gridItem.className = 'grid-item';
                    gridItem.innerHTML = `<a href="#" class="video-link" data-video-id="${value}">${key}</a>`;
                    wordList.appendChild(gridItem);
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    });

    clearSearchButton.addEventListener('click', () => {
        searchInput.value = ''; 
        loadPage(1);
        currentPage = 1;
    });

    wordList.addEventListener('click', function (event) {
        if (event.target.classList.contains('video-link')) {
            event.preventDefault();
            const videoId = event.target.getAttribute('data-video-id');
            if (player) {
                currentVideoId = videoId; 
                player.loadVideoById(videoId);
            }
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

    const resizer = document.getElementById('resizer');
    let isResizing = false;

    resizer.addEventListener('mousedown', (event) => {
        isResizing = true;
    });

    document.addEventListener('mousemove', (event) => {
        if (isResizing) {
            const container = document.getElementById('container');
            const newWidth = event.clientX - container.getBoundingClientRect().left;

            if (newWidth > 200 && newWidth < container.offsetWidth * 0.7) {
                leftPanel.style.width = `${newWidth}px`;
                rightPanel.style.width = `calc(100% - ${newWidth}px)`;
                playerElement.style.width = '100%';
                playerElement.style.height = `${(rightPanel.offsetWidth * 9) / 16}px`;
            }
        }
    });

    document.addEventListener('mouseup', () => {
        isResizing = false;
    });
});