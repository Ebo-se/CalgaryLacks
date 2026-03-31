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
  background: yellow; /* Yellow background */
  color: blue;         /* Blue text */
  font-family: Arial;
  text-align: center;
  overflow: hidden;
  transform-origin: center center;
}

#app {
  margin-top: 60px;
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
}

#bar {
  height: 100%;
  width: 10%;
  background: lime;
}

/* GLITCH */
.glitch {
  animation: glitch 0.15s infinite;
}
@keyframes glitch {
  0% { transform: translate(2px, -2px); }
  50% { transform: translate(-3px, 3px); }
  100% { transform: translate(0,0); }
}

/* POPUPS */
.popup {
  position: absolute;
  width: 200px;
  height: 100px;
  background: #222;
  border: 2px solid red;
  color: white;
  padding: 5px;
}

/*FAKE CRASH */
#crash {
  display: none;
  position: fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background:black;
  color:#00ffcc;
  font-family: monospace;
  padding:40px;
  z-index:9999;
}
</style>
</head>

<body>

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

// AI VOICE
function speak(text) {
  let msg = new SpeechSynthesisUtterance(text);
  msg.rate = 0.9;
  msg.pitch = 0.8;
  speechSynthesis.speak(msg);
}

// SOUND
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let intensity = 200;
function beep() {
  let osc = audioCtx.createOscillator();
  osc.type = "sawtooth";
  osc.frequency.setValueAtTime(intensity, audioCtx.currentTime);
  osc.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.1);
  intensity += 30;
}

// CURSOR CHAOS
setInterval(() => {
  if (Math.random() < 0.3) {
    document.body.style.cursor =
      ["pointer","wait","crosshair","not-allowed"][Math.floor(Math.random()*4)];
  }
}, 400);

// GLITCH
function glitch() {
  document.body.classList.add("glitch");
  setTimeout(()=>document.body.classList.remove("glitch"), 200);
}

// SCREEN WOBBLE
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
  }, 16); // ~60fps
}

// BUTTON MOVEMENT
let btn = document.getElementById("btn");
btn.onmousemove = () => {
  btn.style.left = Math.random()*window.innerWidth + "px";
  btn.style.top = Math.random()*window.innerHeight + "px";
};

// CHAOTIC CONFIRM FUNCTION
async function chaoticConfirm() {
  const phrases = [
    "Are you sure?"
  ];

  let toSpeak = [];
  let count = 2 + Math.floor(Math.random() * 2); // 2 or 3 phrases
  for (let i = 0; i < count; i++) {
    toSpeak.push(phrases[Math.floor(Math.random() * phrases.length)]);
  }

  toSpeak.forEach((p, i) => {
    setTimeout(() => speak(p), i * 300);
  });

  await new Promise(r => setTimeout(r, 500));
  return confirm("Are you sure?");
}

// INPUT HANDLER
document.getElementById("input").oninput = async (e) => {
  if (!(await chaoticConfirm())) {
    e.target.value = "";
    return;
  }

  if (Math.random() < 0.3) {
    beep();
    speak("Input rejected.");
    e.target.value = e.target.value.split("").sort(()=>Math.random()-0.5).join("");
    screenWobble(15, 400); // wobble on rejected input
  }
};

// CHECKBOX HANDLER
document.getElementById("check").onchange = async (e) => {
  if (!(await chaoticConfirm())) {
    e.target.checked = false;
    return;
  }

  if (Math.random() < 0.8) {
    e.target.checked = false;
    speak("That was incorrect.");
    screenWobble(20, 500); // wobble on failed checkbox
  }
};

// BUTTON CLICK HANDLER
btn.onclick = async () => {
  if (!(await chaoticConfirm())) return;

  stage++;
  beep();
  glitch();
  screenWobble(25, 600); // wobble on button press

  let label = document.getElementById("label");

  if (stage === 1) {
    label.innerText = "Type 'human' backwards.";
    speak("Suspicious human detected.");
  }
  else if (stage === 2) {
    label.innerText = "Select all images containing regret.";
    spawnPopup("Images failed.");
    speak("Regret is not measurable.");
  }
  else if (stage === 3) {
    label.innerText = "Do NOT click anything.";
    speak("Do not proceed.");
    setTimeout(()=>label.innerText="Why did you click?",2000);
  }
  else if (stage === 4) {
    label.innerText = "Set progress to exactly 73%.";
    speak("Precision required.");
  }
  else if (stage === 5) {
    label.innerText = "Final verification...";
    speak("Final judgment initiated.");
    for (let i=0;i<10;i++){
      setTimeout(()=>spawnPopup("Verifying..."), i*200);
    }
  }
  else if (stage === 6) {
    triggerCrash();
  }
  else {
    label.innerText = "You are not human.";
    speak("Conclusion. You have failed.");
  }
};

// POPUPS
function spawnPopup(text) {
  let d = document.createElement("div");
  d.className = "popup";
  d.style.left = Math.random()*window.innerWidth + "px";
  d.style.top = Math.random()*window.innerHeight + "px";
  d.innerHTML = "<p>"+text+"</p><button>OK</button>";

  d.querySelector("button").onclick = () => d.remove();

  d.onmouseover = () => {
    d.style.left = Math.random()*window.innerWidth + "px";
    d.style.top = Math.random()*window.innerHeight + "px";
  };

  document.body.appendChild(d);
}

// FAKE CRASH
function triggerCrash() {
  document.getElementById("crash").style.display = "block";
  speak("System failure detected.");
  screenWobble(50, 1000); // massive wobble on crash
  setTimeout(() => {
    location.reload();
  }, 4000);
}

// PROGRESS BAR RANDOMIZATION
setInterval(() => {
  progress += Math.random()*20 - 10;
  progress = Math.max(0, Math.min(100, progress));
  document.getElementById("bar").style.width = progress + "%";

  if (Math.random() < 0.3) {
    spawnPopup("Processing...");
    screenWobble(10, 300); // small random wobble
  }
}, 1000);

</script>

</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    threading.Timer(1.0, open_browser).start()
    httpd.serve_forever()