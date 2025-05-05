// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
import './index.css'
// import App from './App.jsx'

// createRoot(document.getElementById('root')).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )

const app = document.getElementById('app');
const diaryForm = `
  <div>
    <h2>📸 Upload Cat Image</h2>
    <input type="file" id="imageUpload" accept="image/*"><br>
    <img id="previewImg" width="200"/><br><br>

    <button id="generateBtn">🔮 Generate Diary</button><br><br>

    <h2>📝 Generated Diary</h2>
    <textarea id="text" placeholder="Diary will appear here..." rows="6" cols="40"></textarea><br>
    <p><strong>Tone:</strong> <span id="tone"></span></p>
    <p><strong>Persona:</strong> <span id="persona"></span></p>
    <p><strong>Voice:</strong> <span id="voice"></span></p>

    <audio id="audioPlayer" controls></audio><br><br>

    <button id="saveBtn">💾 Save Diary</button>
  </div>
`;

app.innerHTML = diaryForm;

// Preview image
document.getElementById('imageUpload').addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) {
    document.getElementById('previewImg').src = URL.createObjectURL(file);
  }
});

// 🔮 Generate button logic
document.getElementById('generateBtn').addEventListener('click', async () => {
  const imageFile = document.getElementById('imageUpload').files[0];
  if (!imageFile) {
    alert("Please upload an image first.");
    return;
  }

  const formData = new FormData();
  formData.append('image', imageFile);

  const res = await fetch('/api/generate', {
    method: 'POST',
    body: formData
  });

  const result = await res.json();
  console.log(result);
  document.getElementById('text').value = result.text || '';
  document.getElementById('audioPlayer').src = `/audio/${result.audio_path}`;
  document.getElementById('tone').textContent = result.tone || '';
  document.getElementById('persona').textContent = result.persona || '';
  document.getElementById('voice').textContent = result.voice || '';
});

// 💾 Save button logic
document.getElementById('saveBtn').addEventListener('click', async () => {
  const text = document.getElementById('text').value;
  const tone = document.getElementById('tone').textContent;
  const persona = document.getElementById('persona').textContent;
  const voice = document.getElementById('voice').textContent;
  const audio = document.getElementById('audioPlayer').src;

  const entry = {
    text,
    tone,
    persona,
    voice,
    audio_path: audio.replace('/static/', '')  // backend expects relative path
  };

  const res = await fetch('/api/diary', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry)
  });

  const result = await res.json();
  alert(result.message || "Diary saved.");
});
