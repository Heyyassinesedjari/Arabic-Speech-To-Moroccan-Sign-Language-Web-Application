const chatForm = document.querySelector('.chat-form');
const chatBox = document.querySelector('.chat');
let url = '/process_data';
let url1 = '/process_audio';

const typingIndicator = document.querySelector('.typing-indicator');
const langSwitch = document.getElementById('lang-switch');

chatForm.addEventListener('submit', (event) => {
  let answer;
  event.preventDefault();
  const message = event.target.querySelector('input').value;
  appendChatBox('user', message);
  appendTyping();
  const data = {
    question: message,
    language: 'english'
  };
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'asr_to_sign/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      stopTyping();
      if (result["message"] == 200) {
        const videoUrl = result["filepath"]
        console.log("videoUrl :" + videoUrl)
        sendVideo(videoUrl);
      }
      else {
        console.log(11111111111111111111111111)
        const videoUrl = result["filepath"]
        console.log("videoUrl :" + videoUrl)
        sendVideo(videoUrl);
      }
    })
    .catch(error => {
      stopTyping();
      const videoUrl = result["filepath"]
      console.log("videoUrl :" + videoUrl)
      sendVideo(videoUrl);
    });
  event.target.reset();
});

function appendChatBox(userType, message) {
  const chatBubble = document.createElement('div');
  const chatBoxDiv = document.createElement('div');
  chatBubble.classList.add('chat-bubble');
  chatBubble.classList.add(userType);
  chatBubble.textContent = message;
  chatBoxDiv.classList.add('chat-box-' + userType);
  chatBoxDiv.appendChild(chatBubble);
  chatBox.appendChild(chatBoxDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendTyping() {
  const divTyping = document.createElement('div');
  divTyping.classList.add("typing-indicator");
  const span1 = document.createElement('span');
  const span2 = document.createElement('span');
  const span3 = document.createElement('span');
  divTyping.appendChild(span1);
  divTyping.appendChild(span2);
  divTyping.appendChild(span3);
  chatBox.appendChild(divTyping);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function startTyping() {
  showTypingIndicator();
  setTimeout(() => {
    console.log('Bot is typing...');
  }, 1000);
}

function stopTyping() {
  const typingIndicator = document.querySelector('.typing-indicator');
  typingIndicator.remove();
}

const recordButton = document.getElementById('record-button');
let audioRecording = null;


function sendAudio(audio) {
  const audioUrl = URL.createObjectURL(audio);

  const messageItem = document.createElement("div");
  messageItem.classList.add("chat-message");
  messageItem.classList.add("outgoing-message"); // Ajouter la classe pour aligner le message à droite
  messageItem.innerHTML = `
    <div class="audio-message">
      <audio controls>
        <source src="${audioUrl}" type="audio/webm">
        Your browser does not support the audio element.
      </audio>
    </div>
  `;

  chatBox.appendChild(messageItem);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function deleteFile(filePath) {
  if (window.File && window.FileSystem) {
    window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
    window.requestFileSystem(window.TEMPORARY, 5 * 1024 * 1024, function (fs) {
      fs.root.getFile(filePath, { create: false }, function (fileEntry) {
        fileEntry.remove(function () {
          console.log('File deleted successfully');
        }, function (error) {
          console.log('Error deleting file:', error);
        });
      }, function (error) {
        console.log('Error retrieving file:', error);
      });
    }, function (error) {
      console.log('Error requesting file system:', error);
    });
  } else {
    console.log('File and FileSystem APIs are not supported');
  }
}




function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      console.log(audioChunks);

      mediaRecorder.addEventListener('dataavailable', (event) => {
        audioChunks.push(event.data);
        console.log(audioChunks);
      });

      mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        sendAudio(audioBlob);
        appendTyping();
        var formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');
        fetch('/process_audio', {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(result => {
            stopTyping();
            if (result["message"] == 200) {
              const videoUrl = result["filepath"]
              console.log("videoUrl :" + videoUrl)
              sendVideo(videoUrl);
            } else {
              const videoUrl = result["filepath"]
              console.log("videoUrl :" + videoUrl)
              sendVideo(videoUrl);
            }
            // deleteFile(result["filepath"])
            //console.log("The answer is retrieved successfully!");
          })
          .catch(error => {
            // Handle any errors that occur during the request
          });
      });

      mediaRecorder.start();

      recordButton.textContent = 'Stop Recording';
      recordButton.removeEventListener('click', startRecording);
      recordButton.addEventListener('click', stopRecording);

      audioRecording = mediaRecorder;
    })
    .catch((error) => {
      console.error('Error accessing microphone:', error);
    });
}

function stopRecording() {
  if (audioRecording) {
    audioRecording.stop();
    audioRecording = null;

    recordButton.textContent = 'Record';
    recordButton.removeEventListener('click', stopRecording);
    recordButton.addEventListener('click', startRecording);
  }
}

recordButton.addEventListener('click', startRecording);



// ...existing code...

// Helper function to send messages
function sendMessage(message) {
  // Send the text message
  console.log("Text message:", message);
}

// function sendVideo(videoUrl) {
//   const messageItem = document.createElement("div");
//   messageItem.classList.add("chat-message");
//   messageItem.classList.add("incoming-message");
//   messageItem.innerHTML = `
//     <div class="video-message">
//       <video controls style="width: 400px; height: 300px;">
//         <source src="${videoUrl}" type="video/mp4">
//         Your browser does not support the video element.
//       </video>
//     </div>
//   `;

//   chatBox.appendChild(messageItem);
//   chatBox.scrollTop = chatBox.scrollHeight;

//   // Attacher un gestionnaire d'événement pour le chargement de la vidéo
//   const videoElement = messageItem.querySelector("video");
//   videoElement.addEventListener("canplaythrough", function() {
//     videoElement.play();
//   });
// }



function sendVideo(videoUrl) {
  const cacheBuster = Math.random(); // Generate a random number as a cache-busting query parameter
  const updatedUrl = `${videoUrl}?cb=${cacheBuster}`; // Add cache-buster as a query parameter

  const messageItem = document.createElement("div");
  messageItem.classList.add("chat-message");
  messageItem.classList.add("incoming-message");
  messageItem.innerHTML = `
    <div class="video-message">
      <video controls style="width: 400px; height: 300px;">
        <source src="${updatedUrl}" type="video/mp4">
        Your browser does not support the video element.
      </video>
    </div>
  `;

  chatBox.appendChild(messageItem);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Attach an event handler for video loading
  const videoElement = messageItem.querySelector("video");
  videoElement.addEventListener("canplaythrough", function () {
    videoElement.play();
  });
}
