const WebSocket = require("ws");

const ws = new WebSocket("ws://localhost:8765");
let label1 = "ina subiria";

let istexttosign = false;

const signs = [
  "kuhara",
  "uzito kupungua",
  "moyo zaifu",
  "kuungua",
  "maumivu",
  "hospitali",
  "dactari",
  "jifunze",
  "salama",
  "kifo",
  "dawa",
];
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const label = data.label;
  const base64Image = data.image;

  function speakSwahili(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "sw-KE"; // Swahili (Kenya), adjust if needed

    // Try to use Swahili voice if available
    const voices = window.speechSynthesis.getVoices();
    const swahiliVoice = voices.find((v) => v.lang.startsWith("sw"));
    const swahiliVoice1 = voices.filter((v) => v.lang.startsWith("sw"));
    console.log(voices);

    if (swahiliVoice) {
      utterance.voice = swahiliVoice;
    }

    window.speechSynthesis.speak(utterance);
  }

  document.getElementById("label").innerText = `Prediction: ${label}`;

  const imgElement = document.getElementById("video");
  //  imgElement.src = 'data:image/jpeg;base64,' + event.data.image;
  imgElement.src = `data:image/jpeg;base64,${base64Image}`;

  const checked = document.getElementById("switch-component");
  const video1 = document.getElementById("video1");

  const texttosign = document.getElementById("texttosign");
  const texttosignbtn = document.getElementById("texttosignbtn");

  texttosignbtn.addEventListener("click", () => {
    istexttosign = true;
    const s = signs.find((data) => data == texttosign.value);
    if (s) {
      video1.src = s + ".gif";
    } else {
      video1.src = "nosign.png";
    }
    // setTimeout(() => {
    //   istexttosign = false;
    //   const s = signs.find((data) => data == "dactari");
    //   if (s) {
    //   } else {
    //     video1.src = "nosign.png";
    //   }
    // }, 5000);
  });

  if (label == "ina subiria") {
    // video1.src = "nosign.png";
  } else {
    if (label !== label1) {
      if (checked.checked) {
        speakSwahili(label);
      }
      //video1.src = "habari.png";
    }
  }
  label1 = label;
};

ws.onopen = () => {
  console.log("Connected to Python WebSocket Server");
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};
