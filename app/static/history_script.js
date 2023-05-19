const newConversationButton = document.querySelector(".new-conversation-button");
const renameButton = document.querySelector(".history-rename-button");
const table = document.querySelector(".chatbox-container");

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

function renameConversation() {
}

function deleteConversation(conversationId) {
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
  location.reload();
}

newConversationButton.addEventListener("click", newConversation);
renameButton.addEventListener("click", renameConversation);

function displayConversation(conversationName, conversationId) {
  const tr = table.insertRow(-1);

  const td = document.createElement("tr");
  td.innerHTML = conversationName;

  const rename = document.createElement("button");
  rename.innerHTML = "Rename";

  const a = document.createElement("a");
  a.href = `/index/${conversationId}`;
  a.innerHTML = "Continue";

  const delet = document.createElement("button");
  delet.innerHTML = "Delete";

  tr.insertCell(td);
  tr.insertCell(button);
  tr.insertCell(a);
  tr.insertCell(delet);
}
