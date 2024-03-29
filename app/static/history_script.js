const newConversationButton = document.querySelector(".new-conversation-button");
const historyContainer = document.querySelector(".history-container");

function newConversation() {
  // Create new conversation in the database
  fetch("/newConversation", {
    method: "POST"
  })
  .then((response) => response.json())
  .then((data) => {
    // Display new conversation on the page
    displayConversation("New Conversation", data["id"]);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
}

function renameConversation(conversationId, button) {
  // rename a conversation in the database
  var newName = window.prompt("Enter the new conversation name:");
  fetch("/renameConversation", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ conversationId, newName }),
  })
  .catch((error) => {
    console.error("Error:", error);
  });

  // Rename conversation in the page
  div = button.parentNode;
  p = div.firstElementChild ;
  p.innerHTML = newName;
}

function deleteConversation(conversationId, button) {
  if (!confirm("Are you sure you want to delete this conversation?")) {
    return;
  }

  // Delete a conversation in the database
  fetch("/deleteConversation", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ conversationId }),
  })
  .catch((error) => {
    console.error("Error:", error);
  });

  // Delete conversation from page
  div = button.parentNode;
  div.remove();
}

newConversationButton.addEventListener("click", newConversation);

function displayConversation(conversationName, conversationId) {
  // Div to contain the conversation
  const div = document.createElement("div");
  div.classList.add("history-conversation");

  // P that contains the conversation name
  const p = document.createElement("p");
  p.innerHTML = conversationName;

  // Rename button
  const rename = document.createElement("button");
  rename.classList.add("history-rename-button");
  rename.onclick = function () {renameConversation(conversationId, rename)};
  rename.innerHTML = "Rename";

  // Continue button
  const a = document.createElement("a");
  a.style.textAlign = "center";
  a.href = `/index/${conversationId}`;
  a.innerHTML = "Continue";

  // Delete button
  const delet = document.createElement("button");
  delet.classList.add("history-delete-button");
  delet.onclick = function () {deleteConversation(conversationId, delet)};
  delet.innerHTML = "Delete";

  // Add all elements to the div
  div.appendChild(p)
  div.appendChild(rename)
  div.appendChild(a)
  div.appendChild(delet)

  historyContainer.appendChild(div);
}


// function to confirm logout
function confirmLogout() {
  if (confirm("Are you sure you want to log out?")) {
      window.location.href = "/logout";
  } else {
    return false; // Cancels the click event
  }
}

