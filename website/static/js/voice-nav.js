// static/js/voice-nav.js

// Ensure the Web Speech API is available
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = true; // Keep listening
    recognition.interimResults = false; // Final results only

    let isCurrentlyListening = false; // Tracks the actual state of the recognition engine
    const SESSION_STORAGE_KEY = 'voiceNavActive'; // Key for session storage

    // --- Helper Functions ---
    function speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            speechSynthesis.speak(utterance);
        } else {
            console.log("Browser doesn't support speech synthesis.");
        }
    }

    function updateButtonState(button, isActive) {
        if (button) {
            if (isActive) {
                button.textContent = "Stop Voice Navigation";
                button.style.backgroundColor = "#d9534f"; 
            } else {
                button.textContent = "Voice Navigation";
                button.style.backgroundColor = "blue"; 
            }
        }
    }

    function startRecognition(button) {
        if (!isCurrentlyListening) {
            try {
                recognition.start();
                sessionStorage.setItem(SESSION_STORAGE_KEY, 'true'); // Mark as intentionally active
                // isCurrentlyListening will be set true in onstart
                console.log('Attempting to start voice recognition...');
                // Initial button update (will be confirmed in onstart)
                 if (button) {
                     button.textContent = "Listening...";
                     button.style.backgroundColor = "#d9534f"; 
                 }
            } catch (error) {
                console.error("Recognition start failed:", error);
                sessionStorage.setItem(SESSION_STORAGE_KEY, 'false'); // Failed to start, disable auto-restart
                updateButtonState(button, false);
                isCurrentlyListening = false;
                 // Handle specific errors like "invalid state" if already started
                 if (error.name === 'InvalidStateError') {
                    console.warn("Recognition was already started.");
                    // We might already be listening, ensure state is correct
                     isCurrentlyListening = true; // Assume it's running if this error occurs
                     sessionStorage.setItem(SESSION_STORAGE_KEY, 'true');
                     updateButtonState(button, true);
                 }
            }
        } else {
            console.log("Recognition is already listening.");
            // Ensure session state and button are consistent
            sessionStorage.setItem(SESSION_STORAGE_KEY, 'true');
            updateButtonState(button, true);
        }
    }

    function stopRecognition(button) {
        let stoppedIntentionally = false; // Flag to check if stop was user-triggered
        if (isCurrentlyListening) {
            recognition.stop(); // This will trigger 'onend' eventually
            console.log('Attempting to stop voice recognition...');
            stoppedIntentionally = true; // Mark that we initiated the stop
        }
        // Always mark as inactive immediately when stop is requested
        sessionStorage.setItem(SESSION_STORAGE_KEY, 'false');
        isCurrentlyListening = false; // Assume stopped, onend will confirm
        updateButtonState(button, false);

        // Provide feedback to the user for stopping
        if (stoppedIntentionally) {
            speak("Exiting voice navigation");
       }
   
    }

    


    // --- DOM Ready ---
    document.addEventListener('DOMContentLoaded', () => {
        const startButton = document.getElementById('start-recording');
        const shapesLabel = document.querySelector('label[for="shapesFile"]');
        const graphsLabel = document.querySelector('label[for="graphsFile"]');
        const equationsLabel = document.querySelector('label[for="equationsFile"]');

        // --- Button Setup (Toggle) ---
        if (startButton) {
            // Initialize button based on session state
            const shouldBeActive = sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true';
            updateButtonState(startButton, shouldBeActive && isCurrentlyListening); // Reflect actual listening state if known

            startButton.addEventListener('click', () => {
                const isActive = sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true';
                if (!isActive) {
                    startRecognition(startButton); // User wants to start
                } else {
                    stopRecognition(startButton); // User wants to stop
                }
            });
        } else {
            console.warn('Voice navigation toggle button (id="start-recording") not found on this page.');
        }

        // --- Attempt Auto-Start based on Session ---
        if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true') {
            console.log("Session state active, attempting auto-start...");
            // Use a small timeout to let the page settle and potentially avoid race conditions
            setTimeout(() => startRecognition(startButton), 100);
        } else {
            console.log("Session state inactive, voice navigation will not auto-start.");
            // Ensure button state is correct if recognition somehow started
            if (isCurrentlyListening) stopRecognition(startButton);
            else updateButtonState(startButton, false);
        }


        // --- Recognition Event Handlers ---
        recognition.onresult = (event) => {
            const lastResultIndex = event.results.length - 1;
            const command = event.results[lastResultIndex][0].transcript.toLowerCase().trim();
            console.log('Heard:', command);

            // --- Stop Command ---
            if (command.includes('stop voice') || command.includes('quit voice')) {
                console.log('Stop/Quit command heard.');
                stopRecognition(startButton); // Use the function to handle state
                return;
            }

            // --- Navigation Commands ---
            else if (command.includes('log in') || command.includes('login')) {
                speak("Navigating to login page."); // Feedback for navigation
                window.location.href = '/login';
            } else if (command.includes('sign up')) {
                 speak("Navigating to sign up page."); // Feedback for navigation
                window.location.href = '/signup';
            } else if (command.includes('home') || command.includes('return') || command.includes('main page')) {
                 speak("Navigating to home page."); // Feedback for navigation
                window.location.href = '/';
            } else if (command.includes('submission history') || command.includes('history')) {
                 speak("Navigating to submission history."); // Feedback for navigation
                window.location.href = '/history';
            } else if (command.includes('generate quiz') || command.includes('quiz')) {
                 speak("Navigating to quiz generator."); // Feedback for navigation
                window.location.href = '/quiz';
            }


            // --- File Upload Commands ---
            else if (command.includes('analyze shapes') || command.includes('analyse shapes')) {
                if (shapesLabel) shapesLabel.click();
                else speak('Analyze shapes button not found on this page.');
            } else if (command.includes('analyze graphs') || command.includes('analyse graphs')) {
                if (graphsLabel) graphsLabel.click();
                else speak('Analyze graphs button not found on this page.');
            } else if (command.includes('analyze equations') || command.includes('analyse equations')) {
                if (equationsLabel) equationsLabel.click();
                else speak('Analyze equations button not found on this page.');
            }

            // --- Command Not Recognized ---
            else {
                // Optional: Provide feedback only if desired, might be annoying
                speak("Command not found");
                // speak('Command not recognized');
                console.log('Command not recognized.');

            }
        };

        recognition.onstart = () => {
            console.log('Speech recognition service has started.');
            isCurrentlyListening = true;
             // Update button only if it exists and session expects it to be active
             if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true') {
                 updateButtonState(startButton, true);
             } else {
                 // If it started unexpectedly, stop it.
                 console.warn("Recognition started but session state is inactive. Stopping.");
                 stopRecognition(startButton);
             }
        };

        recognition.onend = () => {
            console.log('Speech recognition service disconnected.');
            const wasListening = isCurrentlyListening; // Capture state before resetting
            isCurrentlyListening = false;
            updateButtonState(startButton, false); // Always update button to off state first

            // Check if we should try to restart
            if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true' && wasListening) {
                console.log('Session state is active, attempting to restart recognition after a short delay...');
                // Use a delay to prevent hammering the API if it fails immediately
                setTimeout(() => {
                    // Double check the session state again before restarting
                    if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true') {
                        startRecognition(startButton);
                    } else {
                         console.log('Session state changed to inactive during delay, not restarting.');
                    }
                }, 1000); // 1 second delay
            } else {
                 console.log('Recognition ended and session state is inactive, not restarting.');
            }
        };

        recognition.onerror = (event) => {
            console.error('Error occurred in recognition:', event.error);
            isCurrentlyListening = false; // Ensure listening flag is off

            // Handle specific critical errors by disabling auto-restart
            if (event.error === 'not-allowed' || event.error === 'audio-capture' || event.error === 'network') {
                 sessionStorage.setItem(SESSION_STORAGE_KEY, 'false');
                 console.warn(`Critical error (${event.error}), disabling automatic voice navigation for this session.`);
                 if (event.error === 'not-allowed') {
                    alert('Permission to use microphone was denied or is required. Please allow microphone access and manually click "Start Voice Navigation" again.');
                 } else if (event.error === 'audio-capture') {
                     alert('Audio capture error: No microphone found or there was an issue accessing it.');
                 } else {
                      alert(`Speech recognition network or system error: ${event.error}`);
                 }
            } else if (event.error === 'no-speech') {
                console.log('No speech detected for a while.');
                // 'onend' will likely fire after this, restart logic is handled there if session is active.
            } else {
                 // Other errors might be less critical, log them.
                 console.warn(`Speech recognition error: ${event.error}`);
            }

            // Always update button to reflect inactive state on error
            updateButtonState(startButton, false);
        };

    }); // End DOMContentLoaded

} else {
    console.error("Sorry, your browser doesn't support the Web Speech API.");
    // Alert the user and hide the button if it exists
    document.addEventListener('DOMContentLoaded', () => {
        alert("Sorry, your browser doesn't support the Web Speech API needed for voice navigation.");
        const startButton = document.getElementById('start-recording');
        if (startButton) {
            startButton.style.display = 'none';
            startButton.disabled = true;
        }
    });
}