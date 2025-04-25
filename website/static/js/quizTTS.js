document.addEventListener('DOMContentLoaded', () => {
    const readButton = document.getElementById('read-aloud-btn');
    if (!readButton) return;

    const questions = document.querySelectorAll('.question-text');
    let current = 0;
    let paused = false;

    function speakAnswerChoices(options, onComplete = () => {}) {
        let i = 0;
        function speakNext() {
            if (i >= 4 || i >= options.length) {
                onComplete();
                return;
            }
            const label = options[i].parentElement;
            const text = label.textContent.trim();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1;
            utterance.onend = () => {
                i++;
                speakNext();
            };
            speechSynthesis.speak(utterance);
        }
        speakNext();
    }

    function speakQuestionWithAnswers(index) {
        if (index < 0 || index >= questions.length) return;
        const questionEl = questions[index];
        const options = questionEl.parentElement.querySelectorAll('input[type="radio"]');
        const questionText = questionEl.textContent;

        const utterance = new SpeechSynthesisUtterance(questionText);
        utterance.rate = 1;
        utterance.onend = () => {
            speakAnswerChoices(options);
        };
        speechSynthesis.speak(utterance);
    }

    function handleKey(e) {
        switch (e.key) {
            case 'n':
                if (current < questions.length) {
                    speechSynthesis.cancel(); // stop any ongoing speech
                    current++;
                    speakQuestionWithAnswers(current);
                    
                }
                break;
            case 'r':
                if (current >= 0) {
                    speechSynthesis.cancel(); // stop any ongoing speech
                    // restart from the current question
                    // on question 1, logical error causing it to not read the question again
                    speakQuestionWithAnswers(current);
                }
                break;
            case 'p':
                if (speechSynthesis.speaking && !paused) {
                    speechSynthesis.pause();
                    paused = true;
                } else if (paused) {
                    speechSynthesis.resume();
                    paused = false;
                }
                break;
        }
    }

    document.addEventListener('keydown', handleKey);

    readButton.addEventListener('click', () => {
        speechSynthesis.cancel(); // Stop previous speech if any
        speakQuestionWithAnswers(current);
    });
});
