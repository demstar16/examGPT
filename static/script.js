const sendButton = document.querySelector(".chatbox-send-button");
const messageInput = document.querySelector(".chatbox-input");
const chatContainer = document.querySelector(".chatbox-container");

function sendMessage() {
  const message = messageInput.value.trim();

  if (message !== "") {
    displayMessage("You", message, true); // Display user's message
    scrollToBottom();

    // Send the message to the chatbot
    // a function inside "app.py"
    fetch("/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => {
        displayMessage("ExamGPT", data.message, false); // Display chatbot's response
        scrollToBottom();
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    messageInput.value = "";
  }
}

sendButton.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// function determine which side of the chatbox container to display the message
// left for bot & right or user
function displayMessage(sender, message, isUser) {
  const formattedMessage = message.replace(/\n/g, "<br>");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chatbox-message");

  if (isUser) {
    messageDiv.classList.add("chatbox-message-user");
    messageDiv.innerHTML = `<p class="chatbox-message-user-internal">${sender}: ${formattedMessage}</p>`;
  } else {
    messageDiv.classList.add("chatbox-message-chatbot");
    messageDiv.innerHTML = `<p class="chatbox-message-chatbot-internal">${sender}: ${formattedMessage}</p>`;
  }

  chatContainer.appendChild(messageDiv);
}

// Function to automatically scroll to the bottom of the chatbox when a new message arrives
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
