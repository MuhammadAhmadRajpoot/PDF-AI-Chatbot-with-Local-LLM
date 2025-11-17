// static/js/script.js

// === Confirmation Message ===
console.log("Chatbot JavaScript loaded successfully!");

document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const imageUpload = document.getElementById("image-upload");
    const previewContainer = document.getElementById("image-preview-container");
    const urlInput = document.getElementById("url-input");
    const submitUrlBtn = document.getElementById("submit-url-btn");

    let selectedImageData = null; // Store image data here temporarily

    function appendMessage(sender, text, imageSrc = null) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", `${sender}-message`);
        
        if (imageSrc) {
            const img = document.createElement('img');
            img.src = imageSrc;
            img.classList.add('image-preview');
            messageDiv.appendChild(img);
        }
        
        if (text) {
            const textElement = document.createElement("p");
            textElement.textContent = text;
            messageDiv.appendChild(textElement);
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to create and show the image preview
    function showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            selectedImageData = e.target.result; // Store the data
            
            previewContainer.innerHTML = ''; // Clear old preview
            const img = document.createElement('img');
            img.src = selectedImageData;
            img.classList.add('image-preview-thumbnail');
            
            const cancelButton = document.createElement('button');
            cancelButton.textContent = '×';
            cancelButton.classList.add('cancel-preview-btn');
            
            cancelButton.onclick = function() {
                selectedImageData = null;
                imageUpload.value = ''; // Clear file input
                previewContainer.classList.remove('active');
                previewContainer.innerHTML = '';
            };

            previewContainer.appendChild(img);
            previewContainer.appendChild(cancelButton);
            previewContainer.classList.add('active');
        };
        reader.readAsDataURL(file);
    }
    
    // Initial welcome message
    appendMessage("bot", "Assalam-o-Alaikum! Main aapka Gemini AI chatbot hun. Main aapki har tarah se madad kar sakta hun. Koi bhi sawal poochen ya tasveer upload karen.");

    // Event listener for when a file is selected
    imageUpload.addEventListener("change", function(e) {
        if (e.target.files && e.target.files[0]) {
            showImagePreview(e.target.files[0]);
        }
    });

    // New event listener for processing URL
    submitUrlBtn.addEventListener("click", function() {
        const url = urlInput.value.trim();
        if (url) {
            appendMessage("user", `Processing URL: ${url}`);
            
            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage("bot", data.response);
            })
            .catch(error => {
                console.error("Error:", error);
                appendMessage("bot", "Ma'azrat, URL process karne mein koi masla paish aaya.");
            });
            urlInput.value = "";
        }
    });

    // Event listener for the form submission
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (!message && !selectedImageData) {
            return;
        }

        const formData = {
            message: message,
            image: selectedImageData
        };

        appendMessage("user", message, selectedImageData); 
        sendRequestToServer(formData);
        
        userInput.value = "";
        imageUpload.value = ""; 
        selectedImageData = null;
        previewContainer.classList.remove('active');
        previewContainer.innerHTML = '';
    });

    function sendRequestToServer(formData) {
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            appendMessage("bot", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("bot", "Ma'azrat, jawab dainay mein koi masla paish aaya.");
        });
    }
});