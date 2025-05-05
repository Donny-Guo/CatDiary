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
<div class='diary-interface' style="font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; background-color: #fefefe; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
  <h2 style="color: #333;">📸 Upload Cat Image</h2>
  <input type="file" id="imageUpload" accept="image/*" style="margin-bottom: 10px;"><br>
  <div style="margin-bottom: 20px; align-items: center;">
    <img id="previewImg" style="border: 1px solid #ccc; border-radius: 8px; margin-top: 10px; width: 600px;">
  </div>

  <button id="generateBtn" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer;">🔮 Generate Diary</button><br><br>

  <h2 style="color: #333;">📝 Generated Diary</h2>
  <textarea id="text" placeholder="Diary will appear here..." rows="15" cols="100" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; resize: vertical; background-color: rgba(0,0,0,0.05); color: black;"></textarea><br>

  <p style='color: black;'><strong>Mood:</strong> <span id="tone"></span></p>

  <audio id="audioPlayer" controls style="margin-top: 15px; width: 100%;"></audio><br><br>

  <button id="saveBtn" style="padding: 10px 20px; background-color: #2196F3; color: white; border: none; border-radius: 6px; cursor: pointer;">💾 Save Diary</button>
</div>

`;
// const diaryForm = `
//   <div class='diary-interface'>
//     <h2>📸 Upload Cat Image</h2>
//     <input type="file" id="imageUpload" accept="image/*"><br>
//     <div><img id="previewImg" width="200"></div>
    

//     <button id="generateBtn">🔮 Generate Diary</button><br><br>

//     <h2>📝 Generated Diary</h2>
//     <textarea id="text" placeholder="Diary will appear here..." rows="15" cols="100"></textarea><br>
//     <p><strong>Tone:</strong> <span id="tone"></span></p>
//     <p><strong>Persona:</strong> <span id="persona"></span></p>
//     <p><strong>Voice:</strong> <span id="voice"></span></p>

//     <audio id="audioPlayer" controls></audio><br><br>

//     <button id="saveBtn">💾 Save Diary</button>
//   </div>
// `;

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
