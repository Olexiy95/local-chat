const input = document.getElementById("messageInput");

input.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("sendMessageBtn").click();
  }
});
