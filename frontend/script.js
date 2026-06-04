console.log("SCRIPT VERSION 2");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    // Display user message
    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    userInput.value = "";

    try {

        const response = await fetch("https://ai-powered-placement-cell-faq-chatbot.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        console.log("Status:", response.status);

        const data = await response.json();
        
        console.log("Received:", data);
        console.log("Response Data:", data);

        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.answer}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        console.error("Error:", error);

        chatBox.innerHTML += `
            <div class="bot-message">
                Error connecting to server.
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

async function loadChatHistory() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat-history"
        );

        const chats = await response.json();

        chatBox.innerHTML = "";

        chats.forEach(chat => {

            chatBox.innerHTML += `
                <div class="user-message">
                    ${chat.user_message}
                </div>
            `;

            chatBox.innerHTML += `
                <div class="bot-message">
                    ${chat.bot_response}
                </div>
            `;
        });

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        console.error(
            "Error loading chat history:",
            error
        );
    }
}

userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }
});

window.onload = loadChatHistory;