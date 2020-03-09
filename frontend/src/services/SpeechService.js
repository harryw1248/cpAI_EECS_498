import Vue from "vue";

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
    console.log(speech);
    speechSynthesis.speak(speech);
};

/*******************************/
/*       Speech-to-text        */
/*******************************/
//import MicrophoneStream from "microphone-stream";
//const { MediaPresenter } = require("sfmediastream");
const navigator = Vue.prototype.winNavigator;
//let micStream = null;
/*
let presenterMedia = new MediaPresenter(
    {
        audio: {
            channelCount: 1,
            echoCancellation: false
        }
    },
    1000
); // 1sec

presenterMedia.onRecordingReady = function(packet) {
    console.log("Recording started!");
    console.log("Header size: " + packet.data.size + "bytes");

    // Every new streamer must receive this header packet
    //mySocket.emit("bufferHeader", packet);
};

presenterMedia.onBufferProcess = function(packet) {
    console.log("Buffer sent: " + packet[0].size + "bytes");
    //mySocket.emit("stream", packet);
};
*/
function stopStream() {
    /*console.log("micStream.stop()");
    micStream.stop();*/
    //console.log("stopStream()");
    //presenterMedia.stopRecording();
    //presenter.stopRecording();
}

function startStream() {
    //presenterMedia.startRecording();
    /*
    const handleSuccess = stream => {
        micStream = new MicrophoneStream();
        micStream.setStream(stream);
        console.log("micStream set.");

        presenter = new MediaPresenter();
        console.log("getUserMedia succesful, created MediaPresenter");
    };

    const handleError = err => {
        console.log("getUserMedia failed.");
    };

    navigator.getUserMedia(
        // constraints
        {
            video: false,
            audio: true
        },
        handleSuccess,
        handleError
    );*/
}

export default {
    textToSpeech
    /*, startStream, stopStream */
};
