const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadStatus = document.getElementById('uploadStatus');
const documentInfo = document.getElementById('documentInfo');
const chatContainer = document.getElementById('chatContainer');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');

let documentUploaded = false;

// File upload handlers
fileInput.addEventListener('change', handleFileUpload);

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = '#f8f9ff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'transparent';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'transparent';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileUpload();
    }
});

async function handleFileUpload() {
    const file = fileInput.files[0];
    if (!file) return;

    // Show loading
    uploadStatus.className = 'status-message loading';
    uploadStatus.textContent = '⏳ Uploading and processing document...';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/upload-document/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            uploadStatus.className = 'status-message success';
            uploadStatus.textContent = `✅ ${data.message}`;
            
            documentInfo.className = 'document-info show';
            documentInfo.innerHTML = `
                <strong>📄 ${file.name}</strong><br>
                <small>Processed into ${data.chunks} chunks</small>
            `;

            documentUploaded = true;
            questionInput.disabled = false;
            sendBtn.disabled = false;

            // Clear welcome message
            chatContainer.innerHTML = '';
        } else {
            throw new Error(data.detail || 'Upload failed');
        }
    } catch (error) {
        uploadStatus.className = 'status-message error';
        uploadStatus.textContent = `❌ Error: ${error.message}`;
    }
}

// Question handling
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !sendBtn.disabled) {
        askQuestion();
    }
});

sendBtn.addEventListener('click', askQuestion);

async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question || !documentUploaded) return;

    // Add user message
    addMessage(question, 'user');
    questionInput.value = '';

    // Add loading message
    const loadingId = addMessage('Thinking...', 'loading');

    try {
        const response = await fetch('http://localhost:8000/ask/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Remove loading message
        document.getElementById(loadingId).remove();

        if (response.ok) {
            addMessage(data.answer, 'assistant');
        } else {
            throw new Error(data.detail || 'Failed to get answer');
        }
    } catch (error) {
        document.getElementById(loadingId).remove();
        addMessage(`❌ Error: ${error.message}`, 'assistant');
    }
}

function addMessage(text, type) {
    const messageId = 'msg-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageId;
}
