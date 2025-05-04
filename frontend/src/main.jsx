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
    <h2>📝 Today’s Diary</h2>
    <input type="file" id="imageUpload" accept="image/*"><br>
    <img id="previewImg" width="200"/><br>

    <label for="mood">Mood:</label>
    <select id="mood">
      <option>😊</option><option>😢</option><option>😠</option><option>😴</option>
    </select><br>

    <textarea id="text" placeholder="Write your diary..."></textarea><br>

    <audio id="audioPlayer" controls></audio><br>

    <button id="saveBtn">Save</button>
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

// Preview audio
document.getElementById('audioUpload').addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) {
    document.getElementById('audioPlayer').src = URL.createObjectURL(file);
  }
});

// Save data to backend
document.getElementById('saveBtn').addEventListener('click', async () => {
  const mood = document.getElementById('mood').value;
  const text = document.getElementById('text').value;
  const imageFile = document.getElementById('imageUpload').files[0];
  const audioFile = document.getElementById('audioUpload').files[0];

  const formData = new FormData();
  formData.append('mood', mood);
  formData.append('text', text);
  if (imageFile) formData.append('image', imageFile);
  if (audioFile) formData.append('audio', audioFile);

  const res = await fetch('/api/diary', {
    method: 'POST',
    body: formData
  });

  const result = await res.json();
  alert(result.message || 'Saved!');
});
