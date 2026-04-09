// frontend.js

// ハンバーガーメニュー制御
const hamburger = document.getElementById("hamburger");
const navPanel = document.getElementById("navPanel");
const navClose = document.getElementById("navClose");

hamburger.addEventListener("click", () => navPanel.classList.add("open"));
navClose.addEventListener("click", () => navPanel.classList.remove("open"));

// APIの基本URL（バックエンドFastAPI）
const API_BASE = "http://localhost:8000";

// タスク一覧取得
async function fetchTasks() {
  try {
    const res = await fetch(`${API_BASE}/tasks`);
    const tasks = await res.json();
    console.log("Tasks:", tasks);
    // TODO: DOMにタスク表示
  } catch (err) {
    console.error("Error fetching tasks:", err);
  }
}

// 新しいタスク作成
async function createTask(type, content) {
  try {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type, content }),
    });
    const newTask = await res.json();
    console.log("Created Task:", newTask);
    fetchTasks(); // 再表示
  } catch (err) {
    console.error("Error creating task:", err);
  }
}

// 音声ファイル送信（仮）
async function sendSpeech(file) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await fetch(`${API_BASE}/speech-to-text`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    console.log("Speech Text:", data.text);
    return data.text;
  } catch (err) {
    console.error("Error sending speech:", err);
  }
}

// 初期ロードでタスク一覧取得
fetchTasks();
