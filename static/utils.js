const input = document.getElementById("messageInput");

input
  ? input.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("sendMessageBtn").click();
      }
    })
  : null;

const icon = document.getElementById("togglePassword");
let password = document.getElementById("password");

icon.addEventListener("click", function () {
  if (password.type === "password") {
    password.type = "text";
    icon.classList.add("fa-eye-slash");
    icon.classList.remove("fa-eye");
  } else {
    password.type = "password";
    icon.classList.add("fa-eye");
    icon.classList.remove("fa-eye-slash");
  }
});

function logout() {
  fetch("/auth/logout", { method: "GET" })
    .then((response) => {
      // Check if the response is okay
      if (response.ok) {
        window.location.href = "/";
      }
    })
    .catch((error) => console.error("Error:", error));
}
