// static/js/voice-nav.js

// Ensure the Web Speech API is available
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = true; // Try to keep listening
    recognition.interimResults = false; // We only want final results

    let isListening = false; // Flag to track if we are intentionally listening

    // --- DOM Elements ---
    // We need to wait for the DOM to be ready to find elements
    document.addEventListener('DOMContentLoaded', () => {
        const startButton = document.getElementById('start-recording');
        const shapesLabel = document.querySelector('label[for="shapesFile"]');
        const graphsLabel = document.querySelector('label[for="graphsFile"]');
        const equationsLabel = document.querySelector('label[for="equationsFile"]');

        if (startButton) {
            startButton.textContent = "Start Voice Navigation"; // Initial text
            startButton.addEventListener('click', () => {
                if (!isListening) {
                    try {
                        recognition.start();
                        isListening = true;
                        startButton.textContent = "Stop Voice Navigation";
                        startButton.style.backgroundColor = "#d9534f"; // Red when listening
                        console.log('Voice recognition started by button.');
                    } catch (error) {
                        console.error("Recognition start failed:", error);
                        isListening = false; // Reset flag if start fails
                        startButton.textContent = "Start Voice Navigation";
                        startButton.style.backgroundColor = "blue";
                    }
                } else {
                    recognition.stop(); // User clicked stop
                    isListening = false;
                    startButton.textContent = "Start Voice Navigation";
                    startButton.style.backgroundColor = "blue";
                    console.log('Voice recognition stopped by button.');
                }
            });
        } else {
            console.warn('Voice navigation start button (id="start-recording") not found on this page.');
        }

        // --- Recognition Event Handlers ---
        recognition.onresult = (event) => {
            // Get the last result
            const lastResultIndex = event.results.length - 1;
            const command = event.results[lastResultIndex][0].transcript.toLowerCase().trim();
            console.log('Heard:', command);

            // Stop Command
            if (command.includes('stop') || command.includes('quit')) {
                console.log('Stop/Quit command heard.');
                recognition.stop(); // Will trigger onend
                return; // Don't process other commands if stopping
            }

            // Navigation Commands (work on any page)
            else if (command.includes('log in') || command.includes('login')) {
                window.location.href = '/login';
            } else if (command.includes('sign up')) {
                window.location.href = '/signup';
            } else if (command.includes('home') || command.includes('return') || command.includes('main page')) {
                window.location.href = '/';
            } else if (command.includes('submission history') || command.includes('history')) {
                window.location.href = '/history'; // Make sure this route exists in Flask
            } else if (command.includes('generate quiz') || command.includes('quiz')) {
                window.location.href = '/quiz'; // Make sure this route exists in Flask
            }

            // File Upload Commands (only work if labels exist on the current page)
            else if (command.includes('analyze shapes') || command.includes('analyse shapes')) {
                if (shapesLabel) {
                    console.log('Triggering shapes file input.');
                    shapesLabel.click();
                } else {
                    console.log('Shapes label not found on this page.');
                    speak('Analyze shapes button not found on this page.');
                }
            } else if (command.includes('analyze graphs') || command.includes('analyse graphs')) {
                if (graphsLabel) {
                    console.log('Triggering graphs file input.');
                    graphsLabel.click();
                } else {
                    console.log('Graphs label not found on this page.');
                    speak('Analyze graphs button not found on this page.');
                }
            } else if (command.includes('analyze equations') || command.includes('analyse equations')) {
                if (equationsLabel) {
                    console.log('Triggering equations file input.');
                    equationsLabel.click();
                } else {
                    console.log('Equations label not found on this page.');
                    speak('Analyze equations button not found on this page.');
                }
            }

            // Command Not Recognized
            else {
                speak('Command not recognized');
                console.log('Command not recognized.');
            }
        };

        recognition.onstart = () => {
            // Don't log here if using the button, button handles feedback
            if (startButton) {
                 startButton.textContent = "Listening...";
                 startButton.style.backgroundColor = "#d9534f"; // Red
            }
            console.log('Speech recognition service has started.');
        };

        recognition.onend = () => {
            console.log('Speech recognition service disconnected.');
             if (startButton) {
                 startButton.textContent = "Start Voice Navigation";
                 startButton.style.backgroundColor = "blue"; // Reset button
            }
            // Reset listening flag ONLY if recognition stops unexpectedly
            // If stopped by button click or "stop" command, isListening is already false.
            // We don't automatically restart here anymore, user must click Start again.
             isListening = false;
        };

        recognition.onerror = (event) => {
            console.error('Error occurred in recognition:', event.error);
            isListening = false; // Reset flag on error
             if (startButton) {
                 startButton.textContent = "Start Voice Navigation";
                 startButton.style.backgroundColor = "blue";
            }
            if (event.error === 'no-speech') {
                console.log('No speech detected.');
                // Maybe provide feedback? Don't restart automatically
            } else if (event.error === 'audio-capture') {
                alert('Audio capture error: No microphone found or permission denied.');
            } else if (event.error === 'not-allowed') {
                alert('Permission to use microphone was denied. Please allow microphone access in browser settings.');
            } else {
                 alert(`Speech recognition error: ${event.error}`);
            }
        };

        // --- Helper Functions ---
        function speak(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                speechSynthesis.speak(utterance);
            } else {
                console.log("Browser doesn't support speech synthesis.");
            }
        }

    }); // End DOMContentLoaded

} else {
    console.error("Sorry, your browser doesn't support the Web Speech API.");
    alert("Sorry, your browser doesn't support the Web Speech API needed for voice navigation.");
    // Optionally hide the start button if the API isn't supported
    document.addEventListener('DOMContentLoaded', () => {
        const startButton = document.getElementById('start-recording');
        if (startButton) {
            startButton.style.display = 'none';
        }
    });
}