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
   // Convert the language to lowercase and replace spaces with dashes if needed
   let urlLanguage = language.toLowerCase().replace(/\s+/g, '-');
    
   // Redirect to the new URL for the language chat page
   window.location.href = `http://127.0.0.1:5000/${urlLanguage}/`;
}
