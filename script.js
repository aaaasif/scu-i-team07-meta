async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatBox = document.getElementById("chat-box");

    if (!userInput) return;

    // this is to isplay User Message
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "chat-message user-message";
    userMessageDiv.innerHTML = `<strong>You:</strong> ${userInput}`;
    chatBox.appendChild(userMessageDiv);

    document.getElementById("user-input").value = ""; // Clear input

    // for Auto-scrolling
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userInput })
        });

        const data = await response.json();
        const botResponse = data.answer || "Sorry, I couldn't find an answer.";

        // this is to display Bot Response
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "chat-message bot-message";
        botMessageDiv.innerHTML = `
            <div class="bot-response">
                <img src="deepseek-icon.png" alt="DeepSeek AI" class="bot-icon">
                <div class="bot-text">${botResponse}</div>
            </div>
        `;
        chatBox.appendChild(botMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("Chatbot error:", error);
    }
}

// questions  Flashcard Click
function setQuestion(question) {
    document.getElementById("user-input").value = question;
    sendMessage();
}

// this is to handle Enter Key
function handleKeyPress(event) {
    if (event.key === "Enter") sendMessage();
}
