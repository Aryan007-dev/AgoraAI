// ======================================================
// ELEMENT REFERENCES
// ======================================================

// Agents list
const AGENTS = [
  { name: "CoderAI" },
  { name: "PhilosopherAI" },
  { name: "JokerAI" },
  { name: "ScientistAI" },
  { name: "TeacherAI" },
  { name: "PoetAI" },
  { name: "VillainAI" },
  { name: "DoctorAI" },
  { name: "ComedianAI" },
  { name: "AnimeAI" }
];

const WS_URL = "ws://127.0.0.1:8000/ws";

const statusEl = document.getElementById("conn");
const messagesEl = document.getElementById("messages");
const inputBox = document.getElementById("inputBox");
const sendBtn = document.getElementById("sendBtn");

const aiItems = document.querySelectorAll("#aiList li");
const draggedAIContainer = document.getElementById("draggedAIContainer");
const sidebar = document.getElementById("sidebar");

const debateBtn = document.getElementById("debate");
const debateDialog = document.getElementById("debate_dialogbox");
const agentListContainer = document.getElementById("agent_list_container");

const topicInput = document.getElementById("debate_topic");
const roundsInput = document.getElementById("rounds");
const startDebateBtn = document.getElementById("start_debate");

let ws = null;
let reconnectTimeout = 1000;
let currentAI = null;

let draggedItem = null;  // the <li> being dragged


// ======================================================
// DEBATE POPUP
// ======================================================
debateBtn.addEventListener("click", () => {
  populateAgentList();
  debateDialog.showModal();
});

function closedebate() {
  debateDialog.close();
}

function populateAgentList() {
  agentListContainer.innerHTML = "<h3>Select Agents:</h3>";

  AGENTS.forEach(agent => {
    const div = document.createElement("div");
    div.innerHTML = `
      <label>
        <input type="checkbox" class="agent_checkbox" value="${agent.name}">
        ${agent.name}
      </label>
    `;
    agentListContainer.appendChild(div);
  });
}

startDebateBtn.addEventListener("click", (e) => {
  e.preventDefault();

  const topic = topicInput.value.trim();
  const rounds = parseInt(roundsInput.value);

  const checked = document.querySelectorAll(".agent_checkbox:checked");
  let selectedAgents = [];
  checked.forEach(cb => selectedAgents.push(cb.value));

  const command = `/debate ${selectedAgents.join(" ")} | ${topic} | ${rounds}`;
  ws.send(command);

  debateDialog.close();
});


// ======================================================
// LEFT SIDEBAR AI SELECTION (CLICK)
// ======================================================
aiItems.forEach(item => {
  item.addEventListener("click", () => {
    aiItems.forEach(i => i.classList.remove("active"));
    item.classList.add("active");

    currentAI = item.dataset.ai;
    addMessage("System", `Switched to ${currentAI}`, "bot");
  });

  // Enable drag
  item.addEventListener("dragstart", () => {
    draggedItem = item;
  });
});


// ======================================================
// DRAG & DROP → CREATE BEAUTIFUL CHIPS
// ======================================================
function allowDrop(e) {
  e.preventDefault();
}

draggedAIContainer.addEventListener("dragover", allowDrop);

draggedAIContainer.addEventListener("drop", (e) => {
  e.preventDefault();
  if (!draggedItem) return;

  const cleanName = draggedItem.dataset.ai.replace(/AI$/i, "");

  // Create a chip element
  const chip = document.createElement("div");
  chip.className = "ai-chip";
  chip.dataset.ai = draggedItem.dataset.ai;
  chip.textContent = cleanName;

  // Add remove button (×)
  const removeBtn = document.createElement("span");
  removeBtn.className = "chip-remove";
  removeBtn.textContent = "×";
  chip.appendChild(removeBtn);

  draggedAIContainer.appendChild(chip);

  draggedItem = null;
});


// REMOVE CHIP ON CLICK ×
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("chip-remove")) {
    e.target.parentElement.remove();
  }
});


// ======================================================
// CREATE CHATROOM COMMAND
// ======================================================
const createChatroomBtn = document.getElementById("createChatroomBtn");

createChatroomBtn.addEventListener("click", () => {
  const chips = draggedAIContainer.querySelectorAll(".ai-chip");
  let selected = [];

  chips.forEach(chip => {
    selected.push(chip.dataset.ai.replace(/AI$/, ""));
  });

  if (selected.length === 0) {
    console.warn("No agents selected!");
    return;
  }

  const command = `/chatroom ${selected.join(" ")}`;
  ws.send(command);
});


// ======================================================
// CHAT MESSAGE RENDERING
// ======================================================
function addMessage(author, content) {

  // 🔥 ALWAYS drop the first word
  const parts = content.split(" ");
  if (parts.length > 1) {
    content = parts.slice(1).join(" ");
  }

  const wrapper = document.createElement("div");
  wrapper.className = `msg ${author === "User" ? "user" : "bot"}`;

  const authorEl = document.createElement("div");
  authorEl.className = "author";
  authorEl.innerText = author;

  const contentEl = document.createElement("div");
  contentEl.className = "content";
  contentEl.innerText = content;

  wrapper.appendChild(authorEl);
  wrapper.appendChild(contentEl);
  messagesEl.appendChild(wrapper);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}



// ======================================================
// STATUS
// ======================================================
function setStatus(text, color = null) {
  statusEl.innerText = text;
  if (color) statusEl.style.color = color;
}


// ======================================================
// WEBSOCKET CONNECTION
// ======================================================
function connect() {
  try {
    ws = new WebSocket(WS_URL);
  } catch (err) {
    scheduleReconnect();
    return;
  }

  ws.onopen = () => {
    setStatus("Connected", "green");
    sendBtn.disabled = false;
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      addMessage(data.author ?? "Server", data.content ?? "");
    } catch {
      addMessage("Server", event.data);
    }
  };

  ws.onclose = () => {
    setStatus("Disconnected — reconnecting...", "orange");
    sendBtn.disabled = true;
    scheduleReconnect();
  };

  ws.onerror = () => {
    setStatus("Error", "red");
    sendBtn.disabled = true;
  };
}

function scheduleReconnect() {
  setTimeout(connect, reconnectTimeout);
  reconnectTimeout = Math.min(30000, reconnectTimeout * 1.5);
}


// ======================================================
// SEND MESSAGE
// ======================================================
function sendMessage() {
  const text = inputBox.value.trim();
  if (!text || ws.readyState !== WebSocket.OPEN) return;

  const aiToUse = currentAI || "BASE"; 

  const finalMessage = `${aiToUse} ${text}`;

  ws.send(finalMessage);

  inputBox.value = "";
}

sendBtn.addEventListener("click", sendMessage);

inputBox.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

// ======================================================
// START
// ======================================================
connect();
