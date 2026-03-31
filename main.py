import http.server
import socketserver
import webbrowser
import threading

PORT = 8000

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Human Verification</title>
<style>
body {
  margin: 0;
  background: yellow;
  color: blue;
  font-family: Arial;
  text-align: center;
  overflow: hidden;
}

button {
  position: absolute;
  padding: 10px 20px;
}

#progress {
  width: 300px;
  height: 20px;
  background: #333;
  margin: 20px auto;
  position: relative;
}

#bar {
  height: 100%;
  width: 10%;
  background: lime;
}

#wobbleVideo {
  display: block;
  margin: 10px auto;
  width: 200px;
  transform-origin: 50% 50%;
  animation: spin 5s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
</head>

<body>

<img id="omniImage" src="thicc_omni_man_pic.png"
style="display:none; position:fixed; top:10px; right:10px; width:300px;">

<audio id="bgAudio" src="Voicy_thicc_omni_man.mp3" loop></audio>

<h1 id="label">Guess Who's Finally Getting His powers?</h1>
<input id="input"><br>
<input type="checkbox" id="check"> I am not a robot

<div id="progress">
  <div id="bar"></div>
  <video id="wobbleVideo" src="wobble.mp4" autoplay loop muted></video>
</div>

<button id="btn">Next</button>

<script>
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();

// Enable audio on first click
document.body.addEventListener("click", () => {
  if (audioCtx.state === "suspended") audioCtx.resume();
  let bg = document.getElementById("bgAudio");
  if (bg.paused) bg.play();
}, {once:true});

// CHAOS AUDIO
function playChaosAudio() {
  const files = [
    "are-you-sure-omni-man.mp3",
    "Voicy_thicc_omni_man.mp3",
    "Voicy_Think, Mark!.mp3"
  ];

  let layers = 4 + Math.floor(Math.random() * 4);

  for (let i = 0; i < layers; i++) {
    let file = files[Math.floor(Math.random() * files.length)];
    let audio = new Audio(file);
    audio.load();

    // Cranked-up audios
    if (file === "are-you-sure-omni-man.mp3" || file === "Voicy_Think, Mark!.mp3") {
      audio.volume = 1.0;                 // max volume
      audio.playbackRate = 0.95 + Math.random() * 0.15; // slightly slower, clear
    } else {
      audio.volume = 0.5 + Math.random() * 0.5;          // normal chaos
      audio.playbackRate = 0.8 + Math.random() * 1.5;    // normal chaos speed
    }

    audio.currentTime = Math.random() * 1.5;

    try {
      let source = audioCtx.createMediaElementSource(audio);
      let panner = audioCtx.createStereoPanner();
      source.connect(panner);
      panner.connect(audioCtx.destination);
      panner.pan.value = Math.random() * 2 - 1;
    } catch(e) {}

    audio.play().catch(()=>{});
  }
}

// SAFE MOUSE AUDIO (softer now)
let lastMousePlay = 0;
document.addEventListener("mousemove", (e) => {
  let now = Date.now();
  if (now - lastMousePlay > 120) {
    lastMousePlay = now;
    let audio = new Audio("invincible-not-nice.mp3");
    audio.volume = 0.15 + Math.random() * 0.1;  // reduced volume
    audio.playbackRate = 0.9;  // slower, clearer
    audio.play().catch(()=>{});
  }
});

// CONFIRM
async function chaoticConfirm() {
  document.getElementById("omniImage").style.display = "block";
  playChaosAudio();
  await new Promise(r => setTimeout(r, 300));
  let result = confirm("Are you sure?");
  document.getElementById("omniImage").style.display = "none";
  return result;
}

// EVENTS
document.getElementById("input").oninput = async (e) => {
  if (!(await chaoticConfirm())) e.target.value = "";
};
document.getElementById("check").onchange = async (e) => {
  if (!(await chaoticConfirm())) e.target.checked = false;
};
document.getElementById("btn").onclick = async () => {
  if (!(await chaoticConfirm())) return;
  document.getElementById("label").innerText = "You are not human.";
};

// PROGRESS CHAOS
let progress = 10;
setInterval(() => {
  progress += Math.random()*10 - 5;
  progress = Math.max(0, Math.min(100, progress));
  document.getElementById("bar").style.width = progress + "%";
}, 1000);
</script>

</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            return super().do_GET()

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    threading.Timer(1.0, open_browser).start()
    httpd.serve_forever()