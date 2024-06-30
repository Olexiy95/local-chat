const socket = new WebSocket("ws://" + window.location.host + "/ws");

socket.onmessage = function (event) {
  console.log("Message received: " + event.data);
  var messageData = JSON.parse(event.data);
  console.log("Message data: " + messageData);
  const user_id = messageData.user_id;
  console.log("user_id: " + user_id);
  var messagesContainer = document.getElementById("messages");
  var messageElement = document.createElement("div");
  messageElement.innerHTML = `
  <div>
    <span><strong> <a href="/user/${messageData["user_id"]}"> ${messageData.username} </a></strong> [${messageData.timestamp}]:</span>
    <span>${messageData.content}</span>
  </div>
`;
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

window.addEventListener("load", function () {
  updateScroll();
});

function updateScroll() {
  var messages = document.getElementById("messages");
  messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
  let input = document.getElementById("messageInput");
  let message = input.value;
  socket.send(message);
  console.log("Message SENT: " + message);
  input.value = "";
  updateScroll();
}

function sendVoiceMessage(voiceBlob) {
  socket.send(voiceBlob);
}

function clearChat() {
  fetch("/clear_chat", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "Chat cleared") {
        let messages = document.getElementById("messages");
        messages.innerHTML = "";
      }
    });
}
