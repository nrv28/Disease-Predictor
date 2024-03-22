
// Function to append a message to the conversation
function appendMessage(type, message) {
    var conversation = document.getElementById('conversation');
    var messageDiv = document.createElement('div');
    messageDiv.className = (type === 'user') ? 'user-message' : 'gemini-message';
    messageDiv.innerHTML = '<strong>' + ((type === 'user') ? 'You:' : 'Copilot:') + '</strong> ' + message + '<br>';
    conversation.appendChild(messageDiv);
    conversation.scrollTop = conversation.scrollHeight;
}

// Function to start the chat process
function startChat() {
    // Enable send and stop buttons, disable start button
    document.getElementById('send-button').disabled = false;
    document.getElementById('stop-button').disabled = false;

    // Append a message indicating the chat has started
    appendMessage('gemini', 'Chat started. Ask me anything!');
}

// Function to stop the chat process
function stopChat() {
    // Disable send and stop buttons, enable start button
    document.getElementById('send-button').disabled = true;
    document.getElementById('stop-button').disabled = true;

    // Append a message indicating the chat has stopped
    appendMessage('gemini', 'Chat stopped.');
}

// Start the chat automatically when the page loads
startChat();

// Event listener for the send button
document.getElementById('send-button').addEventListener('click', function () {
    var userQuery = document.getElementById('user-query').value;
    appendMessage('user', userQuery);
    document.getElementById('user-query').value = ''; // Clear input field

    document.querySelector('.loader').style.display = 'inline-block';

    // Send user query to server using fetch API
    fetch('/chat', {
        method: 'POST',
        body: 'user_query=' + encodeURIComponent(userQuery),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
        .then(response => response.text())
        .then(data => {
            appendMessage('gemini', data);
            document.querySelector('.loader').style.display = 'none';
          }
        );
});

// Event listener for the stop button
document.getElementById('stop-button').addEventListener('click', stopChat);
