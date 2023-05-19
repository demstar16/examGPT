const renameButton = document.querySelector(".history-rename-button");
const continueButton = document.querySelector(".history-continue-button");

function sendMessage() {
  const message = messageInput.value.trim();

  if (message !== "") {
    displayMessage("You", message, true); // Display user's message
    scrollToBottom();

    // Disable input and button while ExamGPT is thinking.
    messageInput.disabled = true;
    sendButton.disabled = true;

    // Display loading message
    const { loadingMessage, loadingInterval } = displayLoadingMessage("ExamGPT", "Thinking");
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
        // Remove loading message
        chatContainer.removeChild(loadingMessage);

        displayMessage("ExamGPT", data.message, false); // Display chatbot's response
        scrollToBottom();

        // Re-enable input and button
        messageInput.disabled = false;
        sendButton.disabled = false;
      })
      .catch((error) => {
        console.error("Error:", error);

        // Re-enable input and button
        messageInput.disabled = false;
        sendButton.disabled = false;
      });

    messageInput.value = "";
  }
}

renameButton.addEventListener("click", sendMessage);
continueButton.addEventListener("click", sendMessage);

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
