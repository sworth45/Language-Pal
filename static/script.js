document.addEventListener("DOMContentLoaded", function() {
    fetch('/languages')
        .then(response => response.json())
        .then(data => {
            const favoritesDiv = document.getElementById("favorites");
            const languageListDiv = document.getElementById("language-list");

            data.favorites.forEach(language => {
                let btn = document.createElement("button");
                btn.textContent = language;
                btn.onclick = () => openChat(language);
                favoritesDiv.appendChild(btn);
            });

            data.languages.forEach(language => {
                let btn = document.createElement("button");
                btn.textContent = language;
                btn.onclick = () => openChat(language);
                languageListDiv.appendChild(btn);
            });
        });
});

function openChat(language) {
    // This function will eventually load the chat window for the selected language
    alert(`Open chat for ${language}`);
}
