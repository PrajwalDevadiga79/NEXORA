"""
NyayaSathi - Advanced Voice Input Module
Integrates a minimal, ChatGPT-styled microphone button and language selector
directly into the Streamlit chat input bar using the browser's Web Speech API.
Supports English (India), Hindi, and Kannada.
"""

import streamlit.components.v1 as components

VOICE_LANGUAGES = {
    "en-IN": "English (India)",
    "hi-IN": "हिन्दी (Hindi)",
    "kn-IN": "ಕನ್ನಡ (Kannada)",
}


def inject_chat_voice_input():
    """
    Renders an invisible client-side controller that mounts a ChatGPT-styled
    microphone button and language selector directly beside the chat input submit button.
    Transcribed speech is placed directly into the chat input textarea as editable text.
    """
    html_code = """
    <script>
    (function() {
        // Prevent duplicate initializations
        if (window.__nyayasathi_voice_init) return;
        window.__nyayasathi_voice_init = true;

        const parentDoc = window.parent.document;
        let recognition = null;
        let isRecording = false;
        let currentLang = localStorage.getItem("ns_voice_lang") || "en-IN";

        // Supported languages configuration
        const LANGS = {
            "en-IN": { label: "EN", full: "English" },
            "hi-IN": { label: "हिं", full: "हिन्दी" },
            "kn-IN": { label: "ಕನ್ನ", full: "ಕನ್ನಡ" }
        };

        // React-compatible value setter for textarea
        function setChatInputValue(textarea, value) {
            if (!textarea) return;
            textarea.focus();
            let prototype = Object.getPrototypeOf(textarea);
            let descriptor = null;
            while (prototype) {
                descriptor = Object.getOwnPropertyDescriptor(prototype, "value");
                if (descriptor && descriptor.set) break;
                prototype = Object.getPrototypeOf(prototype);
            }
            if (descriptor && descriptor.set) {
                descriptor.set.call(textarea, value);
            } else {
                textarea.value = value;
            }
            // Dispatch input & change events so React recognizes the text and enables Submit button
            textarea.dispatchEvent(new Event("input", { bubbles: true }));
            textarea.dispatchEvent(new Event("change", { bubbles: true }));
        }

        // Show floating status / error toast above the chat input
        function showVoiceToast(message, type = "info", autoHideMs = 3500) {
            let toast = parentDoc.getElementById("ns-voice-toast");
            if (!toast) {
                toast = parentDoc.createElement("div");
                toast.id = "ns-voice-toast";
                toast.style.cssText = `
                    position: fixed;
                    bottom: 84px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: #18181B;
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 9999px;
                    padding: 8px 18px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
                    z-index: 999999;
                    font-size: 13px;
                    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
                    color: #ECECEC;
                    transition: opacity 0.2s ease, transform 0.2s ease;
                    pointer-events: auto;
                `;
                parentDoc.body.appendChild(toast);
            }

            let indicator = "";
            if (type === "listening") {
                indicator = `<span style="width: 8px; height: 8px; border-radius: 50%; background: #EF4444; display: inline-block; animation: nsPulse 1s infinite;"></span>`;
            } else if (type === "error") {
                indicator = `<span style="color: #F87171;">⚠️</span>`;
            } else if (type === "success") {
                indicator = `<span style="color: #34D399;">✓</span>`;
            }

            let stopBtnHtml = type === "listening" ? `<button id="ns-toast-stop-btn" style="background:#27272A; border:1px solid #3F3F46; border-radius:12px; color:#E4E4E7; font-size:11px; padding:2px 8px; cursor:pointer; margin-left:8px;">Stop</button>` : "";

            toast.innerHTML = `${indicator} <span>${message}</span> ${stopBtnHtml}`;
            toast.style.display = "flex";
            toast.style.opacity = "1";

            if (type === "listening") {
                const stopBtn = parentDoc.getElementById("ns-toast-stop-btn");
                if (stopBtn) {
                    stopBtn.onclick = function(e) {
                        e.stopPropagation();
                        stopRecording();
                    };
                }
            }

            if (autoHideMs > 0) {
                clearTimeout(toast._hideTimer);
                toast._hideTimer = setTimeout(() => {
                    toast.style.opacity = "0";
                    setTimeout(() => { toast.style.display = "none"; }, 200);
                }, autoHideMs);
            }
        }

        function hideVoiceToast() {
            const toast = parentDoc.getElementById("ns-voice-toast");
            if (toast) {
                toast.style.opacity = "0";
                setTimeout(() => { toast.style.display = "none"; }, 200);
            }
        }

        // Initialize Web Speech Recognition
        function getSpeechRecognition() {
            const SpeechRec = window.parent.SpeechRecognition ||
                              window.parent.webkitSpeechRecognition ||
                              window.SpeechRecognition ||
                              window.webkitSpeechRecognition;
            if (!SpeechRec) return null;
            return new SpeechRec();
        }

        function startRecording(micBtn) {
            const SpeechRec = getSpeechRecognition();
            if (!SpeechRec) {
                showVoiceToast("Voice recognition is not supported in this browser. Please use Google Chrome, Edge, or Brave.", "error", 5000);
                return;
            }

            const chatInputArea = parentDoc.querySelector('textarea[data-testid="stChatInputTextArea"]');
            const initialText = chatInputArea ? chatInputArea.value.trim() : "";
            let interimTranscript = "";
            let finalTranscript = initialText ? initialText + " " : "";

            recognition = SpeechRec;
            recognition.lang = currentLang;
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;

            recognition.onstart = function() {
                isRecording = true;
                micBtn.classList.add("recording");
                const langName = (LANGS[currentLang] && LANGS[currentLang].full) || currentLang;
                showVoiceToast(`Listening... Speak in ${langName}`, "listening", 0);
            };

            recognition.onresult = function(event) {
                interimTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcriptPiece = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcriptPiece + " ";
                    } else {
                        interimTranscript += transcriptPiece;
                    }
                }
                const fullText = (finalTranscript + interimTranscript).replace(/\\s+/g, " ");
                setChatInputValue(chatInputArea, fullText);
            };

            recognition.onerror = function(event) {
                isRecording = false;
                micBtn.classList.remove("recording");
                if (event.error === "not-allowed") {
                    showVoiceToast("Microphone permission denied. Please allow microphone access in your browser settings.", "error", 5000);
                } else if (event.error === "no-speech") {
                    showVoiceToast("No speech detected. Click the mic to try again.", "error", 3500);
                } else if (event.error === "network") {
                    showVoiceToast("Network error occurred during speech recognition.", "error", 4000);
                } else {
                    showVoiceToast(`Voice input error: ${event.error}`, "error", 3500);
                }
            };

            recognition.onend = function() {
                isRecording = false;
                micBtn.classList.remove("recording");
                const currentText = chatInputArea ? chatInputArea.value.trim() : "";
                if (currentText && currentText !== initialText) {
                    showVoiceToast("Speech recognized! Review or edit before sending.", "success", 3000);
                } else {
                    hideVoiceToast();
                }
            };

            try {
                recognition.start();
            } catch (err) {
                showVoiceToast(`Could not start voice recognition: ${err.message}`, "error", 4000);
            }
        }

        function stopRecording() {
            if (recognition && isRecording) {
                try {
                    recognition.stop();
                } catch (e) {}
                isRecording = false;
            }
        }

        // Attach buttons to the chat input container
        function mountVoiceControls() {
            const chatInput = parentDoc.querySelector('div[data-testid="stChatInput"]');
            if (!chatInput) return;

            // Find the submit button
            const submitBtn = chatInput.querySelector('button[data-testid="stChatInputSubmitButton"]');
            if (!submitBtn) return;

            // Check if already mounted
            if (chatInput.querySelector('#ns-voice-controls-wrapper')) return;

            // Create wrapper
            const wrapper = parentDoc.createElement("div");
            wrapper.id = "ns-voice-controls-wrapper";
            wrapper.style.cssText = `
                display: flex;
                align-items: center;
                gap: 6px;
                margin-right: 6px;
                user-select: none;
            `;

            // Language Selector Button / Pill
            const langBtn = parentDoc.createElement("button");
            langBtn.id = "ns-voice-lang-btn";
            langBtn.title = "Switch Voice Language (English / हिन्दी / ಕನ್ನಡ)";
            langBtn.type = "button";
            langBtn.innerHTML = `
                <span id="ns-lang-flag" style="font-size: 11px; opacity: 0.85; margin-right: 3px;">🌐</span>
                <span id="ns-lang-code" style="font-size: 11px; font-weight: 600; color: #D4D4D8;">${(LANGS[currentLang] && LANGS[currentLang].label) || "EN"}</span>
            `;
            langBtn.style.cssText = `
                background: #18181B;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 4px 8px;
                color: #A1A1AA;
                cursor: pointer;
                display: flex;
                align-items: center;
                height: 28px;
                transition: all 0.15s ease;
                outline: none;
            `;

            langBtn.onmouseenter = () => {
                langBtn.style.background = "#27272A";
                langBtn.style.borderColor = "rgba(255, 255, 255, 0.2)";
            };
            langBtn.onmouseleave = () => {
                langBtn.style.background = "#18181B";
                langBtn.style.borderColor = "rgba(255, 255, 255, 0.1)";
            };

            // Language toggle click (cycles between en-IN, hi-IN, kn-IN)
            const langCycle = ["en-IN", "hi-IN", "kn-IN"];
            langBtn.onclick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (isRecording) stopRecording();
                const nextIdx = (langCycle.indexOf(currentLang) + 1) % langCycle.length;
                currentLang = langCycle[nextIdx];
                localStorage.setItem("ns_voice_lang", currentLang);
                parentDoc.getElementById("ns-lang-code").textContent = LANGS[currentLang].label;
                showVoiceToast(`Voice language set to: ${LANGS[currentLang].full}`, "info", 2000);
            };

            // Microphone Button (ChatGPT minimalist line style)
            const micBtn = parentDoc.createElement("button");
            micBtn.id = "ns-voice-mic-btn";
            micBtn.title = "Click to speak your legal inquiry";
            micBtn.type = "button";
            micBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:block;">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                    <line x1="12" x2="12" y1="19" y2="22"></line>
                </svg>
            `;
            micBtn.style.cssText = `
                background: transparent;
                border: none;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #D4D4D8;
                cursor: pointer;
                transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
                outline: none;
                padding: 0;
            `;

            micBtn.onmouseenter = () => {
                if (!isRecording) {
                    micBtn.style.background = "#27272A";
                    micBtn.style.color = "#FFFFFF";
                }
            };
            micBtn.onmouseleave = () => {
                if (!isRecording) {
                    micBtn.style.background = "transparent";
                    micBtn.style.color = "#D4D4D8";
                }
            };

            micBtn.onclick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (isRecording) {
                    stopRecording();
                } else {
                    startRecording(micBtn);
                }
            };

            wrapper.appendChild(langBtn);
            wrapper.appendChild(micBtn);

            // Insert directly before the submit button
            submitBtn.parentNode.insertBefore(wrapper, submitBtn);

            // Inject keyframes for recording pulse if not present
            if (!parentDoc.getElementById("ns-voice-styles")) {
                const styleEl = parentDoc.createElement("style");
                styleEl.id = "ns-voice-styles";
                styleEl.textContent = `
                    @keyframes nsPulse {
                        0%, 100% { opacity: 1; transform: scale(1); }
                        50% { opacity: 0.4; transform: scale(1.3); }
                    }
                    #ns-voice-mic-btn.recording {
                        background: rgba(239, 68, 68, 0.2) !important;
                        color: #EF4444 !important;
                        border: 1px solid rgba(239, 68, 68, 0.4) !important;
                        animation: nsPulse 1.2s infinite ease-in-out !important;
                    }
                `;
                parentDoc.head.appendChild(styleEl);
            }
        }

        // Run mounting logic repeatedly to survive React component updates
        setInterval(mountVoiceControls, 300);
        mountVoiceControls();
    })();
    </script>
    """
    components.html(html_code, height=0, width=0)
