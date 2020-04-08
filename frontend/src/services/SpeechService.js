import store from "../store";

/*******************************/
/*       Text-to-speech        */
/*******************************/

let textToSpeech = text => {
    let speech = new SpeechSynthesisUtterance();
    speech.voice = speechSynthesis.getVoices()[33];
    speech.text = text;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    // console.log(speech);
    speechSynthesis.speak(speech);
};

/*******************************/
/*       Speech-to-text        */
/*******************************/
const SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
let recognition = new SpeechRecognition();

let initSpeechToText = () => {
    recognition.lang = "en-EN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = e => {
        let result = "";
        const last = e.results.length - 1;
        result = e.results[last][0].transcript;
        console.log(e.results[0][0].confidence);
        console.log(result);
        store.state.conversation.sttResponse = result;
        store.state.conversation.sttInProgress = false;

        setTimeout(() => {
            store.dispatch("conversation/speak", result);
            store.state.conversation.sttResponse = "";
        }, 1000);
    };

    recognition.onspeechend = () => {
        recognition.stop();
        console.log("Recognition Done");
        store.state.conversation.sttResponse = "";
        store.state.conversation.sttInProgress = false;
    };

    recognition.onnomatch = () => {
        console.log("No match/recongition.");
        store.state.conversation.sttInProgress = false;
    };

    recognition.onerror = e => {
        console.log(e.error);
        store.state.conversation.sttResponse = "";
        store.state.conversation.sttInProgress = false;
    };
};

function startSpeaking() {
    console.log("Recongition started");
    recognition.start();
    console.log(store);
    store.state.conversation.sttInProgress = true;
}

export default {
    textToSpeech,
    startSpeaking,
    initSpeechToText
};
