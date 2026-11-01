const grid = document.querySelector('#sudoku');
const original = JSON.parse(grid.dataset.original);
const id = grid.dataset.puzzleId;
const fields = [...grid.querySelectorAll('input')];
const feedback = document.querySelector('#feedback');
let mistakes = 0;
let submitted = false;
const start = Date.now();

function boardData() {
  return Array.from({length: 9}, (_, row) =>
    Array.from({length: 9}, (_, col) => {
      const value = fields[row * 9 + col].value;
      return value ? Number(value) : 0;
    }));
}

async function postJson(url, payload) {
  const response = await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
  const data = await response.json();
  return {ok: response.ok, data};
}

fields.forEach(field => field.addEventListener('input', () => {
  field.value = /^[1-9]$/.test(field.value) ? field.value : '';
  feedback.textContent = '';
}));

document.querySelector('#check').addEventListener('click', async () => {
  try {
    const response = await postJson(`/api/check/${encodeURIComponent(id)}`, {board: boardData()});
    feedback.textContent = response.data.message || 'Fehler bei der Prüfung.';
    if (response.ok && !response.data.valid) mistakes++;
  } catch { feedback.textContent = 'Verbindung fehlgeschlagen.'; }
});

document.querySelector('#reset').addEventListener('click', () => {
  fields.forEach((field, i) => field.value = original[Math.floor(i / 9)][i % 9] || '');
  feedback.textContent = 'Sudoku zurückgesetzt.';
});

document.querySelector('#submit').addEventListener('click', async () => {
  if (submitted) {feedback.textContent = 'Das Ergebnis wurde bereits gespeichert.'; return;}
  const player = prompt('Dein Spielername (max. 30 Zeichen):', 'Gast');
  if (player === null) return;
  const seconds = Math.floor((Date.now() - start) / 1000);
  try {
    const response = await postJson(`/api/submit/${encodeURIComponent(id)}`, {board: boardData(), player, seconds, mistakes});
    feedback.textContent = response.data.message || response.data.error;
    if (response.ok) submitted = true;
  } catch {feedback.textContent = 'Verbindung fehlgeschlagen.';}
});

setInterval(() => {document.querySelector('#timer').textContent = `Zeit: ${Math.floor((Date.now() - start) / 1000)} Sekunden`;}, 1000);
