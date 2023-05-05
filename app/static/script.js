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

const NUM_PARTICLES = 50;
const PARTICLE_SIZE = 10;

const particles = [];

document.addEventListener('mousedown', (event) => {
  for (let i = 0; i < particles.length; i++) {
    const particle = particles[i];
    const rect = particle.getBoundingClientRect();
    const centerX = rect.left + PARTICLE_SIZE / 2;
    const centerY = rect.top + PARTICLE_SIZE / 2;
    const dx = event.clientX - centerX;
    const dy = event.clientY - centerY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    particle.vx = (dx / distance) * 10;
    particle.vy = (dy / distance) * 10;
  }
});

document.addEventListener('mouseup', () => {
  for (let i = 0; i < particles.length; i++) {
    const particle = particles[i];
    particle.vx = (Math.random() - 0.5) * 5;
    particle.vy = (Math.random() - 0.5) * 5;
  }
});


function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.top = `${Math.random() * window.innerHeight}px`;
    particle.style.left = `${Math.random() * window.innerWidth}px`;

    // Generate a random pastel color for each particle
    const hue = Math.floor(Math.random() * 360);
    const pastel = `hsl(${hue}, 50%, 80%)`;
    particle.style.backgroundColor = pastel;

    document.body.appendChild(particle);
    particles.push(particle);
  }
  

  function updateParticles() {
    for (let i = 0; i < particles.length; i++) {
      const particle = particles[i];
      let x = parseInt(particle.style.left);
      let y = parseInt(particle.style.top);
      let vx = particle.vx || (Math.random() - 0.5) * 5;
      let vy = particle.vy || (Math.random() - 0.5) * 5;
      x += vx;
      y += vy;
      if (x < 0 || x > window.innerWidth - PARTICLE_SIZE) {
        vx *= -1;
      }
      if (y < 0 || y > window.innerHeight - PARTICLE_SIZE) {
        vy *= -1;
      }
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      particle.vx = vx;
      particle.vy = vy;
    }
  }
  

for (let i = 0; i < NUM_PARTICLES; i++) {
  createParticle();
}

setInterval(updateParticles, 20);
