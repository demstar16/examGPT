const sendButton = document.querySelector(".chatbox-send-button");
const messageInput = document.querySelector(".chatbox-input");
const chatContainer = document.querySelector(".chatbox-container");

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

    // Get the conversation id from the url
    let url = window.location.href.split("/");
    let cid = url[url.length-1];

    // Send the message to the chatbot
    // a function inside "__init__.py"
    fetch(`/chatbot/${cid}`, {
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

  if (isUser) { // Add user message to page
    messageDiv.classList.add("chatbox-message-user");
    messageDiv.innerHTML = `<p class="chatbox-message-user-internal">${sender}: ${formattedMessage}</p>`;
  } else { // Add bot message to page
    messageDiv.classList.add("chatbox-message-chatbot");
    messageDiv.innerHTML = `<p class="chatbox-message-chatbot-internal">${sender}: ${formattedMessage}</p>`;
  }

  chatContainer.appendChild(messageDiv);
}

// Function to automatically scroll to the bottom of the chatbox when a new message arrives
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to display the loading message for ExamGPT
function displayLoadingMessage(sender, message) {
  const formattedMessage = message.replace(/\n/g, "<br>");
  const initialSpaces = "&nbsp;".repeat(3);
  const messageDiv = document.createElement("div");

  messageDiv.classList.add("chatbox-message", "chatbox-message-chatbot");
  messageDiv.innerHTML = `<p class="chatbox-message-chatbot-internal">${sender}: ${formattedMessage}${initialSpaces}</p>`;

  chatContainer.appendChild(messageDiv);

  // Dot animation
  let dots = 0;
  const loadingInterval = setInterval(() => {
    dots = (dots + 1) % 4;
    const dotString = ".".repeat(dots);
    const spaceString = "&nbsp;".repeat(3 - dots);
    messageDiv.innerHTML = `<p class="chatbox-message-chatbot-internal">${sender}: ${message}${dotString}${spaceString}</p>`;
  }, 500);

  return { loadingMessage: messageDiv, loadingInterval: loadingInterval };
}

// function to confirm logout
function confirmLogout() {
  if (confirm("Are you sure you want to log out?")) {
      window.location.href = "/logout";
  } else {
    return false; // Cancels the click event
  }
}