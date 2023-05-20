const newConversationButton = document.querySelector(".new-conversation-button");
const renameButton = document.querySelector(".history-rename-button");
const historyContainer = document.querySelector(".history-container");

function newConversation() {
  // Create new conversation in the database
  fetch("/newConversation", {
    method: "POST"
  })
  .then((response) => response.json())
  .then((data) => {
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

  // Rename conversation from page
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
renameButton.addEventListener("click", renameConversation);

function displayConversation(conversationName, conversationId) {
  const div = document.createElement("div");
  div.classList.add("history-conversation");

  const p = document.createElement("p");
  p.innerHTML = conversationName;

  const rename = document.createElement("button");
  div.classList.add("history-rename-button");
  rename.innerHTML = "Rename";

  const a = document.createElement("a");
  a.style.textAlign = "center";
  a.href = `/index/${conversationId}`;
  a.innerHTML = "Continue";

  const delet = document.createElement("button");
  div.classList.add("history-delete-button");
  delet.innerHTML = "Delete";

  div.appendChild(p)
  div.appendChild(rename)
  div.appendChild(a)
  div.appendChild(delet)

  historyContainer.appendChild(div);
}

