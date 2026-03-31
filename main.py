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
  transform-origin: center center;
}

#app { margin-top: 60px; }

button {
  position: absolute;
  padding: 10px 20px;
}

#progress {
  width: 300px;
  height: 20px;
  background: #333;
  margin: 20px auto;
}

#bar {
  height: 100%;
  width: 10%;
  background: lime;
}

.glitch { animation: glitch 0.15s infinite; }
@keyframes glitch {
  0% { transform: translate(2px, -2px); }
  50% { transform: translate(-3px, 3px); }
  100% { transform: translate(0,0); }
}

.popup {
  position: absolute;
  width: 200px;
  height: 100px;
  background: #222;
  border: 2px solid red;
  color: white;
  padding: 5px;
}

#crash {
  display: none;
  position: fixed;
  top:0; left:0;
  width:100%; height:100%;
  background:black;
  color:#00ffcc;
  font-family: monospace;
  padding:40px;
  z-index:9999;
}
</style>
</head>

<body>

<img id="omniImage" src="thicc_omni_man_pic.png"
style="display:none; position:fixed; top:10px; right:10px; width:400px; z-index:9999;">

<audio id="bgAudio" src="Voicy_thicc_omni_man.mp3" loop></audio>

<div id="app">
  <h1 id="label">Guess Who's Finally Getting His powers?</h1>
  <input id="input" placeholder="Type here"><br>
  <input type="checkbox" id="check"> I am not a robot
  <div id="progress"><div id="bar"></div></div>
  <button id="btn">Next</button>
</div>

<div id="crash">
  <h1>SYSTEM ERROR</h1>
  <p>Human verification process has failed.</p>
  <p>Initiating shutdown...</p>
</div>

<script>
let stage = 0;
let progress = 10;

// AUDIO CONTEXT
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();

// ✅ Resume AudioContext on first click (REQUIRED)
document.body.addEventListener("click", () => {
    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }

    const bg = document.getElementById("bgAudio");
    if (bg.paused) bg.play();
}, {once: true});

// 🔥 CHAOS AUDIO
function playChaosAudio() {
  let layers = 6 + Math.floor(Math.random() * 6);

  for (let i = 0; i < layers; i++) {

    let audio = new Audio("are-you-sure-omni-man.mp3");
    audio.load();

    audio.volume = Math.min(1, Math.random() * 1.5);
    audio.playbackRate = 0.5 + Math.random() * 2.5;

    if (Math.random() < 0.3) {
      audio.playbackRate *= 3;
    }

    audio.currentTime = Math.random() * 1.5;

    try {
      let source = audioCtx.createMediaElementSource(audio);
      let panner = audioCtx.createStereoPanner();

      source.connect(panner);
      panner.connect(audioCtx.destination);

      let interval = setInterval(() => {
        panner.pan.value = (Math.random() * 2 - 1);
      }, 30);

      audio.onended = () => clearInterval(interval);
    } catch (e) {
      console.log("Audio node error:", e);
    }

    audio.play().catch(err => {
      console.log("Playback failed:", err);
    });
  }
}

// CHAOTIC CONFIRM
async function chaoticConfirm() {
  const img = document.getElementById("omniImage");
  img.style.display = "block";

  playChaosAudio();

  await new Promise(r => setTimeout(r, 300));

  let result = confirm("Are you sure?");
  img.style.display = "none";
  return result;
}

// EFFECTS
function beep() {
  let osc = audioCtx.createOscillator();
  osc.type = "sawtooth";
  osc.frequency.setValueAtTime(200, audioCtx.currentTime);
  osc.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.1);
}

function glitch() {
  document.body.classList.add("glitch");
  setTimeout(()=>document.body.classList.remove("glitch"), 200);
}

function screenWobble(intensity = 20, duration = 500) {
  let start = Date.now();
  let body = document.body;
  let interval = setInterval(() => {
    let time = Date.now() - start;
    if (time > duration) {
      body.style.transform = "";
      clearInterval(interval);
      return;
    }
    let x = (Math.random() - 0.5) * intensity;
    let y = (Math.random() - 0.5) * intensity;
    let rotate = (Math.random() - 0.5) * intensity/2;
    body.style.transform = `translate(${x}px, ${y}px) rotate(${rotate}deg)`;
  }, 16);
}

// BUTTON CHAOS
let btn = document.getElementById("btn");
btn.onmousemove = () => {
  btn.style.left = Math.random()*window.innerWidth + "px";
  btn.style.top = Math.random()*window.innerHeight + "px";
};

// INPUT
document.getElementById("input").oninput = async (e) => {
  if (!(await chaoticConfirm())) {
    e.target.value = "";
  }
};

// CHECKBOX
document.getElementById("check").onchange = async (e) => {
  if (!(await chaoticConfirm())) {
    e.target.checked = false;
  }
};

// BUTTON CLICK
btn.onclick = async () => {
  if (!(await chaoticConfirm())) return;

  stage++;
  beep();
  glitch();
  screenWobble(25, 600);

  let label = document.getElementById("label");

  if (stage === 1) label.innerText = "Type 'human' backwards.";
  else if (stage === 2) label.innerText = "Select all images containing regret.";
  else if (stage === 3) label.innerText = "Do NOT click anything.";
  else if (stage === 4) label.innerText = "Set progress to exactly 73%.";
  else if (stage === 5) label.innerText = "Final verification...";
  else if (stage === 6) triggerCrash();
  else label.innerText = "You are not human.";
};

// CRASH
function triggerCrash() {
  document.getElementById("crash").style.display = "block";
  screenWobble(50, 1000);
  setTimeout(() => location.reload(), 4000);
}

// PROGRESS CHAOS
setInterval(() => {
  progress += Math.random()*20 - 10;
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