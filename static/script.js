const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

const sessionId = "session-" + Math.random().toString(36).substring(2);

function appendMessage(text, sender) {


    const chatBox = document.getElementById("chat-box")

    const message = document.createElement("div")
    message.classList.add("message")

    if (sender === "bot") {

        message.classList.add("bot-message")

        message.innerHTML =
            `<img class="avatar" src="/static/bot.png">
                <div class="bubble bot">${text}</div>`


    } else {

        message.classList.add("user-message")

        message.innerHTML =
            `<div class="bubble user">${text}</div>`

    }

    chatBox.appendChild(message)

    chatBox.scrollTop = chatBox.scrollHeight

}


async function sendMessage() {


    const message = input.value.trim();

    if (message === "") return;

    appendMessage(message, "user");

    input.value = "";

    try {

        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sessionId: sessionId,
                message: message
            })
        });

        const data = await response.json();

        const loadingMsg = document.getElementById("loading-message");
        if (loadingMsg) loadingMsg.remove();

        appendMessage(data.reply, "bot");

    } catch (error) {

        const loadingMsg = document.getElementById("loading-message");
        if (loadingMsg) loadingMsg.remove();

        appendMessage("Error contacting server.", "bot");

        console.error(error);
    }


}

input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
