document
  .getElementById("requestBtn")
  .addEventListener("click", function (event) {
    event.preventDefault();

    var responseElement = document.getElementById("response");
    var requestBtn = document.getElementById("requestBtn");

    responseElement.classList.add("hidden");
    requestBtn.disabled = true;
    requestBtn.innerHTML = "Loading...";

    sendRequest();
  });

document
  .getElementById("messagePassing")
  .addEventListener("click", async function (event) {
    event.preventDefault();

    var message = document.getElementById("inputMessage").value;

    sendMessage(message);
    setTimeout(() => {
      receiveMessages();
    }, 500);
  });

document
  .getElementById("endedMessage")
  .addEventListener("click", function (event) {
    event.preventDefault();

    endedMessages();
  });

function sendRequest() {
  fetch("http://127.0.0.1:8000/model/Request-Response/", {})
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("responseText").classList.remove("hidden");
      document.getElementById("responseText").innerHTML = `
          <code>
${JSON.stringify(data, null, 2)}
          </code>
      `;
      document.getElementById("requestBtn").disabled = false;
      document.getElementById("requestBtn").innerHTML = "Send Request";
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("response").innerText =
        "Error occurred while fetching response.";
    });
}

function sendMessage(message) {
  fetch("http://127.0.0.1:8000/model/message-passing/send_messages/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ message }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data.message);
      document.getElementById("resMessage").innerHTML = ` 
      <div class="text-white mt-5 font-medium bg-green-400 p-4 px-2 rounded-lg   inline-block">
          ${data.message}
      </div>`;
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("response").innerText =
        "Error occurred while fetching response.";
    });
}

function receiveMessages() {
  fetch("http://127.0.0.1:8000/model/message-passing/receive_messages/", {})
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const messagesDiv = document.getElementById("message");
      messagesDiv.innerHTML = data.messages
        .map(
          (data) =>
            `<div class="text-white mt-5 font-medium bg-blue-400 p-3 rounded-lg ">
          <div>
            "Pesan : ${data.message}"
          </div>
          <div class="text-lg">
            Sent time : ${data.sent_time}, Recived time : ${data.received_time}
          </div>
          </div>`
        )
        .join("");
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("response").innerText =
        "Error occurred while fetching response.";
    });
}

function endedMessages() {
  fetch("http://127.0.0.1:8000/model/message-passing/shutdown/", {})
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      document.getElementById("resMessage").innerHTML = ` 
    <div class="text-white mt-5 font-medium bg-green-400 p-4 rounded-lg   inline-block">
        ${data.status}
    </div>`;
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("response").innerText =
        "Error occurred while fetching response.";
    });
}
