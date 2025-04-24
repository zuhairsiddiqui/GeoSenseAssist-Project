// static/js/voice-nav.js
// Voice Navigation Script for GeoSenseAssist
/* TODO : fix the issue with the file upload buttons not being recognized by the speech recognition engine
after user commands to education level or signup/login
*/
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
            // Cancel any ongoing speech before starting new speech
            // This prevents overlaps if commands come quickly
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            window.speechSynthesis.speak(utterance);
        } else {
            console.log("Browser doesn't support speech synthesis.");
        }
    }

    function updateButtonState(button, isActive) {
        // ... (function unchanged) ...
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
        // ... (function mostly unchanged, added speech cancel) ...
        if (!isCurrentlyListening) {
            try {
                // Ensure speech synthesis queue is clear
                if ('speechSynthesis' in window) window.speechSynthesis.cancel();

                recognition.start();
                sessionStorage.setItem(SESSION_STORAGE_KEY, 'true');
                console.log('Attempting to start voice recognition...');
                 if (button) {
                     button.textContent = "Listening...";
                     button.style.backgroundColor = "#d9534f";
                 }
            } catch (error) {
                console.error("Recognition start failed:", error);
                sessionStorage.setItem(SESSION_STORAGE_KEY, 'false');
                updateButtonState(button, false);
                isCurrentlyListening = false;
                 if (error.name === 'InvalidStateError') {
                    console.warn("Recognition was already started.");
                     isCurrentlyListening = true;
                     sessionStorage.setItem(SESSION_STORAGE_KEY, 'true');
                     updateButtonState(button, true);
                 } else {
                     speak(`Error starting voice recognition: ${error.message || error.name}`);
                 }
            }
        } else {
            console.log("Recognition is already listening.");
            sessionStorage.setItem(SESSION_STORAGE_KEY, 'true');
            updateButtonState(button, true);
        }
    }

    function stopRecognition(button) {
        // ... (function mostly unchanged, added speech cancel) ...
        let stoppedIntentionally = false;
        if (isCurrentlyListening) {
            recognition.stop();
            console.log('Attempting to stop voice recognition...');
            stoppedIntentionally = true;
        }
        sessionStorage.setItem(SESSION_STORAGE_KEY, 'false');
        isCurrentlyListening = false;
        updateButtonState(button, false);

        if (stoppedIntentionally) {
            // Cancel any speech *before* saying "Exiting"
             if ('speechSynthesis' in window) window.speechSynthesis.cancel();
             // Use a slight delay for the exit message if needed
             setTimeout(() => speak("Exiting voice navigation"), 50);
       } else {
            // Still cancel any pending speech if stopped unexpectedly
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
       }
    }

    // --- DOM Ready ---
    document.addEventListener('DOMContentLoaded', () => {
        // --- Get Element References ---
        const startButton = document.getElementById('start-recording');
        const shapesLabel = document.querySelector('label[for="shapesFile"]');
        const graphsLabel = document.querySelector('label[for="graphsFile"]');
        const equationsLabel = document.querySelector('label[for="equationsFile"]');
        const btnElementary = document.getElementById('edu-btn-elementary');
        const btnMiddle = document.getElementById('edu-btn-middle');
        const btnCollege = document.getElementById('edu-btn-college');

        // --- Button Setup (Toggle) ---
        // ... (code unchanged) ...
        if (startButton) {
            const shouldBeActive = sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true';
            updateButtonState(startButton, shouldBeActive && isCurrentlyListening);

            startButton.addEventListener('click', () => {
                const isActive = sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true';
                if (!isActive) {
                    startRecognition(startButton);
                } else {
                    stopRecognition(startButton);
                }
            });
        } else {
            console.warn('Voice navigation toggle button (id="start-recording") not found on this page.');
        }

        // --- Attempt Auto-Start based on Session ---
        // ... (code unchanged) ...
         if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true') {
            console.log("Session state active, attempting auto-start...");
            setTimeout(() => startRecognition(startButton), 100);
        } else {
            console.log("Session state inactive, voice navigation will not auto-start.");
            if (isCurrentlyListening) stopRecognition(startButton);
            else updateButtonState(startButton, false);
        }


        // --- Recognition Event Handlers ---
        recognition.onresult = (event) => {
            const lastResultIndex = event.results.length - 1;
            const command = event.results[lastResultIndex][0].transcript.toLowerCase().trim();
            console.log('Heard:', command);

            const educationFunctionExists = typeof setEducationLevel === 'function';
            // Check if TTS function exists (needed for audio commands)
            const ttsFunctionExists = typeof playTTS === 'function';
            // Get a reference to the speech synthesis object if available
            const synth = ('speechSynthesis' in window) ? window.speechSynthesis : null;


            // --- Stop Command ---
            if (command.includes('stop voice') || command.includes('quit voice')) {
                console.log('Stop/Quit command heard.');
                stopRecognition(startButton);
                return; // Exit early
            }

            // --- Navigation Commands ---
            else if (command.includes('log in') || command.includes('login')) {
                speak("Navigating to login page.");
                window.location.href = '/login';
            } else if (command.includes('sign up')) {
                 speak("Navigating to sign up page.");
                window.location.href = '/signup';
            } else if (command.includes('home') || command.includes('return') || command.includes('main page')) {
                 speak("Navigating to home page.");
                window.location.href = '/';
            } else if (command.includes('submission history') || command.includes('history')) {
                 speak("Navigating to submission history.");
                window.location.href = '/history';
            } else if (command.includes('generate quiz') || command.includes('quiz')) {
                 speak("Navigating to quiz generator.");
                window.location.href = '/quiz';
            }

            // --- File Upload Commands ---
            // NOTE: These still have the potential browser security issue
            // where the .click() might be blocked.
            else if (command.includes('analyze shapes') || command.includes('analyse shapes')) {
                if (shapesLabel) {
                    // Using speakAndThen (if defined) or simple speak + delay
                    speak("Opening shapes file selection.");
                     setTimeout(() => { // Using simple delay as speakAndThen wasn't in this version
                        if(shapesLabel) shapesLabel.click();
                     }, 150);
                } else {
                    speak('Analyze shapes button not found on this page.');
                }
            } else if (command.includes('analyze graphs') || command.includes('analyse graphs')) {
                if (graphsLabel) {
                     speak("Opening graphs file selection.");
                      setTimeout(() => {
                        if(graphsLabel) graphsLabel.click();
                     }, 150);
                } else {
                    speak('Analyze graphs button not found on this page.');
                }
            } else if (command.includes('analyze equations') || command.includes('analyse equations')) {
                if (equationsLabel) {
                    speak("Opening equations file selection.");
                     setTimeout(() => {
                        if(equationsLabel) equationsLabel.click();
                     }, 150);
                } else {
                    speak('Analyze equations button not found on this page.');
                }
            }

            // --- Education Level Commands ---
            // ... (code unchanged) ...
            else if (command.includes('k 5') || command.includes('elementary')) {
                if (btnElementary && educationFunctionExists) {
                    speak("Setting level to K through 5.");
                    setEducationLevel('elementarylevel', btnElementary); // Call the function directly
                } else {
                    speak('Elementary level button or function not available on this page.');
                    console.warn('Could not find #edu-btn-elementary or setEducationLevel function.');
                }
            } else if (command.includes('6 12') || command.includes('middle') || command.includes('six twelve')) { // Added "six twelve"
                if (btnMiddle && educationFunctionExists) {
                    speak("Setting level to 6 through 12.");
                    setEducationLevel('middlelevel', btnMiddle); // Call the function directly
                } else {
                    speak('Middle level button or function not available on this page.');
                    console.warn('Could not find #edu-btn-middle or setEducationLevel function.');
                }
            } else if (command.includes('12 plus') || command.includes('college') || command.includes('twelve plus')) { // Added "twelve plus"
                 if (btnCollege && educationFunctionExists) {
                    speak("Setting level to 12 plus.");
                    setEducationLevel('collegelevel', btnCollege); // Call the function directly
                } else {
                    speak('College level button or function not available on this page.');
                     console.warn('Could not find #edu-btn-college or setEducationLevel function.');
                }
            }

            // --- Audio Playback Commands (NEW SECTION) ---
            else if (command.includes('play audio')) {
                if (ttsFunctionExists) {
                    speak("Playing audio analysis.");
                    // Call playTTS - it should handle starting/restarting
                    playTTS();
                } else {
                    speak("Play audio command is not available on this page.");
                    console.warn("playTTS function not found.");
                }
            }
            else if (command.includes('pause audio')) {
                if (synth && synth.speaking && !synth.paused) {
                    // Only pause if it's actually speaking and not already paused
                    speak("Pausing audio.");
                    synth.pause();
                } else if (synth && synth.paused) {
                     speak("Audio is already paused.");
                } else {
                    speak("Pause audio command is not available or no audio is playing.");
                    console.warn("Cannot pause: Synth not available, not speaking, or already paused.");
                }
            }
            // Added resume for completeness, mirroring 'P' key toggle logic
            else if (command.includes('resume audio') || command.includes('continue audio')) {
                 if (synth && synth.paused) {
                    // Only resume if it's actually paused
                    speak("Resuming audio.");
                    synth.resume();
                 } else if (synth && synth.speaking){
                     speak("Audio is already playing.");
                 } else {
                     speak("Resume audio command is not available or audio was not paused.");
                     console.warn("Cannot resume: Synth not available or not paused.");
                 }
            }
             else if (command.includes('restart audio')) {
                if (ttsFunctionExists && synth) {
                    speak("Restarting audio analysis.");
                    // Cancel current speech first
                    synth.cancel();
                    // Call playTTS after a short delay to ensure cancel finishes
                    setTimeout(() => {
                        playTTS();
                    }, 100);
                } else {
                    speak("Restart audio command is not available on this page.");
                    console.warn("Cannot restart: playTTS function or synth not found.");
                }
            }

            // --- Command Not Recognized ---
            else {
                console.log('Command not recognized:', command);
                 // speak("Command not recognized."); // Optional feedback
            }
        }; // End of recognition.onresult

        recognition.onstart = () => {
            // ... (code unchanged) ...
             console.log('Speech recognition service has started.');
            isCurrentlyListening = true;
             if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true') {
                 updateButtonState(startButton, true);
             } else {
                 console.warn("Recognition started but session state is inactive. Stopping.");
                 stopRecognition(startButton);
             }
        };

        recognition.onend = () => {
            // ... (code unchanged, added speech cancel) ...
            console.log('Speech recognition service disconnected.');
            const wasListening = isCurrentlyListening; // Capture state before resetting
            isCurrentlyListening = false;
            updateButtonState(startButton, false); // Always update button to off state first

            // Also cancel any potentially pending speech on disconnect
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();


            // Check if we should try to restart
            if (sessionStorage.getItem(SESSION_STORAGE_KEY) === 'true' && wasListening) {
                console.log('Session state is active, attempting to restart recognition after a short delay...');
                setTimeout(() => {
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
            // ... (code mostly unchanged, added speech cancel) ...
             console.error('Error occurred in recognition:', event.error);
             isCurrentlyListening = false; // Ensure listening flag is off
             // Also cancel any potentially pending speech on error
             if ('speechSynthesis' in window) window.speechSynthesis.cancel();


            // Handle specific critical errors by disabling auto-restart
            if (event.error === 'not-allowed' || event.error === 'audio-capture' || event.error === 'network' || event.error === 'service-not-allowed') {
                 sessionStorage.setItem(SESSION_STORAGE_KEY, 'false');
                 console.warn(`Critical error (${event.error}), disabling automatic voice navigation for this session.`);
                 let userMessage = '';
                 if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                     userMessage = 'Microphone permission denied. Please allow access and restart voice navigation manually.';
                 } else if (event.error === 'audio-capture') {
                      userMessage = 'Microphone not found or access issue.';
                 } else { // network error
                       userMessage = 'Speech recognition network or system error.';
                 }
                 speak(userMessage); // Give audio feedback
                 alert(userMessage + ` (Error: ${event.error})`); // Also alert

            } else if (event.error === 'no-speech') {
                console.log('No speech detected for a while.');
            } else {
                 console.warn(`Speech recognition error: ${event.error}`);
            }

            updateButtonState(startButton, false);
        };

    }); // End DOMContentLoaded

} else {
    // ... (Fallback unchanged) ...
    console.error("Sorry, your browser doesn't support the Web Speech API.");
    document.addEventListener('DOMContentLoaded', () => {
        alert("Sorry, your browser doesn't support the Web Speech API needed for voice navigation.");
        const startButton = document.getElementById('start-recording');
        if (startButton) {
            startButton.style.display = 'none';
            startButton.disabled = true;
        }
    });
}