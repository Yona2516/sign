// tts.js (Node side)
const fs = require("fs");
const util = require("util");
const path = require("path");
const player = require("play-sound")(); // to play audio
const textToSpeech = require("@google-cloud/text-to-speech");

// Set credentials
const client = new textToSpeech.TextToSpeechClient({
  keyFilename: path.join(__dirname, "credentials/service-account.json"),
});

async function speakSwahili(text) {
  const request = {
    input: { text: text },
    voice: {
      languageCode: "sw-KE",
      name: "sw-KE-Standard-A", // 👈 THIS IS REQUIRED
    },
    audioConfig: {
      audioEncoding: "MP3",
    },
  };

  const [response] = await client.synthesizeSpeech(request);
  const outputPath = path.join(__dirname, "output.mp3");

  await util.promisify(fs.writeFile)(
    outputPath,
    response.audioContent,
    "binary"
  );
  console.log(`Audio content written to ${outputPath}`);

  // Play the file
  player.play(outputPath, (err) => {
    if (err) console.error("Audio playback error:", err);
  });
}

module.exports = speakSwahili;
