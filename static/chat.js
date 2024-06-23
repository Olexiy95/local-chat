const socket = new WebSocket("ws://" + window.location.host + "/ws");

socket.onmessage = function (event) {
  console.log("Message received: " + event.data);
  var messageData = JSON.parse(event.data);
  var messagesContainer = document.getElementById("messages");
  var messageElement = document.createElement("div");
  messageElement.innerHTML = `
    <div>
      <span><strong>${messageData.username}</strong> [${messageData.timestamp}]:</span>
      <span>${messageData.content}</span>
    </div>
  `;
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

function sendMessage() {
  let input = document.getElementById("messageInput");
  let message = input.value;
  socket.send(message);
  console.log("Message SENT: " + message);
  input.value = "";
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
