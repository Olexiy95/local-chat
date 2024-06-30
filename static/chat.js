const socket = new WebSocket("ws://" + window.location.host + "/ws");

socket.onmessage = function (event) {
  console.log("Message received: " + event.data);
  var messageData = JSON.parse(event.data);
  console.log("Message data: " + messageData);

  var messagesContainer = document.getElementById("messages");
  var messageElement = document.createElement("div");
  messageElement.innerHTML = `
  <div>
    [${convertToLocaleString(messageData.timestamp)}]
    <span><strong> <a href="/user/${messageData["id"]}"> ${
    messageData.username
  } </a></strong>: </span>
    <span>${messageData.content}</span>
  </div>
`;
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

function convertToLocaleString(utcString) {
  const date = new Date(utcString + "Z");
  return date.toLocaleString();
}

document.addEventListener("DOMContentLoaded", function () {
  const timestamps = document.querySelectorAll(".timestamp");
  timestamps.forEach((element) => {
    const utcTime = element.getAttribute("data-utc");
    const localTime = new Date(utcTime + "Z").toLocaleString();
    element.textContent = `[${localTime}]`;
  });
});

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
