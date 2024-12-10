document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-text');
    const recordButton = document.getElementById('start-recording');
    const feedbackContent = document.getElementById('feedback-content');
    let isRecording = false;
    
    // Send text message
    async function sendMessage(message, type = 'text') {
        // Add user message to chat
        appendMessage('user', message);
        
        // Clear input
        userInput.value = '';
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    type: type
                })
            });
            
            const data = await response.json();
            
            // Add assistant's response to chat
            appendMessage('assistant', data.response);
            
            // Update feedback panel
            updateFeedback(data.analysis, data.suggestions);
            
            // Convert response to speech
            speakResponse(data.response);
            
        } catch (error) {
            console.error('Error:', error);
            appendMessage('assistant', 'Sorry, there was an error processing your message.');
        }
    }
    
    // Append message to chat
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Update feedback panel
    function updateFeedback(analysis, suggestions) {
        feedbackContent.innerHTML = '';
        
        if (analysis.length === 0) {
            feedbackContent.innerHTML = '<div class="alert alert-success">Great job! No errors found.</div>';
            return;
        }
        
        analysis.forEach(error => {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'feedback-item';
            errorDiv.innerHTML = `
                <strong>${error.category}:</strong> ${error.message}<br>
                ${error.suggestions.length > 0 ? 
                    `<small>Suggestion: <span class="suggestion">${error.suggestions[0]}</span></small>` : 
                    ''}
            `;
            feedbackContent.appendChild(errorDiv);
        });
    }
    
    // Text-to-speech
    async function speakResponse(text) {
        try {
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            const audio = new Audio(data.audio_path);
            audio.play();
        } catch (error) {
            console.error('Error playing audio:', error);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    });
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = userInput.value.trim();
            if (message) {
                sendMessage(message);
            }
        }
    });
    
    recordButton.addEventListener('click', () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });
    
    // Initialize progress chart
    initProgressChart();
});

// Initialize progress chart
async function initProgressChart() {
    try {
        const response = await fetch('/progress');
        const data = await response.json();
        
        const ctx = document.getElementById('progress-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(entry => entry.date),
                datasets: [{
                    label: 'Average Score',
                    data: data.map(entry => entry.average_score),
                    borderColor: '#007bff',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading progress data:', error);
    }
}
