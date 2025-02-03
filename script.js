function sendPrompt() {
    const input = document.getElementById("userInput").value;
    const responseBox = document.getElementById("response");

    if (!input.trim()) {
        alert("Please enter a prompt!");
        return;
    }

    // Add shimmer effect
    responseBox.innerHTML = `<span class="shimmer">DuckBot is thinking...</span>`;

    fetch("server.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "input=" + encodeURIComponent(input)
    })
    .then(response => response.text())
    .then(data => {
        responseBox.innerHTML = ""; // Clear shimmer
        typeText(responseBox, data); // Start typing effect
    })
    .catch(error => {
        responseBox.innerHTML = "Error: " + error;
    });
}

// Typing effect function
function typeText(element, text, index = 0) {
    if (index < text.length) {
        element.innerHTML += text.charAt(index);
        setTimeout(() => typeText(element, text, index + 1), 50); // Adjust speed here
    }
}

// Function to check if Enter key is pressed
function checkEnter(event) {
    if (event.key === "Enter") {
        sendPrompt(); // Call sendPrompt() when Enter is pressed
    }
}