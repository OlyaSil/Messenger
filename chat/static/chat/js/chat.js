function initializeWebSocket(groupName) {
    const chatSocket = new WebSocket(
        `ws://${window.location.host}/ws/chat/${encodeURIComponent(groupName)}/`
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLog = document.getElementById('chat-log');
        const messageElement = document.createElement('div');
        const timestamp = new Date(data.timestamp);
        messageElement.innerHTML = `<strong>${data.email}</strong>: ${data.message} <small>${timestamp.toLocaleString()}</small>`;
        chatLog.appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly:', e);
    };

    chatSocket.onerror = function(e) {
        console.error('WebSocket encountered an error:', e);
    };

    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) { // Enter key
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({'message': message}));
        messageInputDom.value = ''; // Clear input after sending
    };

    return chatSocket;
}

const everyoneButOneSocket = initializeWebSocket("EveryoneButOne");
const checkingTheVibesSocket = initializeWebSocket("CheckingTheVibes");
