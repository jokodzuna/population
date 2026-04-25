let populationData = [];

const gameState = {
  numPlayers: 2,
  targetScore: 5,
  players: [],
  usedCountryIndices: [],
  currentRound: 1,
  currentCountry: null,
  currentPlayerTurn: 0
};

function $(id) { return document.getElementById(id); }

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  $(id).classList.add('active');
}

function formatNumber(n) {
  if (n === '' || n === null || n === undefined) return '';
  const num = parseInt(String(n).replace(/,/g, '').replace(/\D/g, ''), 10);
  if (isNaN(num)) return '';
  return num.toLocaleString('en-US');
}

function parseNumber(str) {
  return parseInt(String(str).replace(/,/g, '').replace(/\D/g, ''), 10) || 0;
}

function getInitials(name) {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

function renderLeaderboard(containerId) {
  const container = $(containerId);
  const sorted = [...gameState.players].sort((a, b) => b.score - a.score);
  container.innerHTML = sorted.map((p, i) => {
    const rankClass = i === 0 ? 'first' : i === 1 ? 'second' : i === 2 ? 'third' : '';
    return `
      <div class="lb-row">
        <div class="lb-rank ${rankClass}">${i + 1}</div>
        <div class="lb-name">${p.name}</div>
        <div class="lb-score">${p.score}</div>
      </div>
    `;
  }).join('');
}

function setupSegmented(selectorId, stateKey, onChange) {
  const container = $(selectorId);
  container.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      gameState[stateKey] = parseInt(btn.dataset.value, 10);
      if (onChange) onChange();
    });
  });
}

function buildNameInputs() {
  const container = $('names-container');
  container.innerHTML = '';
  for (let i = 0; i < gameState.numPlayers; i++) {
    const div = document.createElement('div');
    div.className = 'name-input-group';
    div.innerHTML = `
      <label>Player ${i + 1} Name</label>
      <input type="text" id="name-${i}" placeholder="Player ${i + 1}" value="Player ${i + 1}">
    `;
    container.appendChild(div);
  }
}

function pickRandomCountry() {
  if (gameState.usedCountryIndices.length >= populationData.length) {
    gameState.usedCountryIndices = [];
  }
  let idx;
  do {
    idx = Math.floor(Math.random() * populationData.length);
  } while (gameState.usedCountryIndices.includes(idx));
  gameState.usedCountryIndices.push(idx);
  gameState.currentCountry = populationData[idx];
}

function showPassScreen() {
  const p = gameState.players[gameState.currentPlayerTurn];
  $('pass-player-name').textContent = `Ready ${p.name}?`;
  showScreen('screen-pass');
}

function showGuessScreen() {
  const p = gameState.players[gameState.currentPlayerTurn];
  $('guess-round').textContent = gameState.currentRound;
  $('guess-player-badge').textContent = p.name;
  $('guess-country').textContent = gameState.currentCountry.country;
  $('guess-input').value = '';
  showScreen('screen-guess');
  $('guess-input').focus();
}

function finishRound() {
  const actual = gameState.currentCountry.population;
  let bestDiff = Infinity;
  let winnerIdx = -1;

  gameState.players.forEach((p, i) => {
    const diff = Math.abs(p.currentGuess - actual);
    p.lastDiff = diff;
    p.lastGuess = p.currentGuess;
    if (diff < bestDiff) {
      bestDiff = diff;
      winnerIdx = i;
    }
  });

  if (winnerIdx >= 0) {
    gameState.players[winnerIdx].score += 1;
  }

  // Results
  $('results-country').textContent = gameState.currentCountry.country;
  $('results-actual').textContent = formatNumber(actual);

  const sortedByDiff = [...gameState.players].map((p, i) => ({ p, i })).sort((a, b) => a.p.lastDiff - b.p.lastDiff);
  const list = $('results-list');
  list.innerHTML = sortedByDiff.map(({ p, i }) => {
    const isWinner = i === winnerIdx;
    const pct = actual > 0 ? (p.lastDiff / actual * 100).toFixed(1) : '0';
    const diffClass = pct < 10 ? 'very-close' : pct < 50 ? 'close' : '';
    return `
      <div class="result-row ${isWinner ? 'winner' : ''}">
        <div class="result-avatar" style="background:${getAvatarColor(i)}22;color:${getAvatarColor(i)}">${getInitials(p.name)}</div>
        <div class="result-info">
          <div class="result-name">${p.name} ${isWinner ? '⭐' : ''}</div>
          <div class="result-guess">Guessed ${formatNumber(p.lastGuess)}</div>
        </div>
        <div class="result-diff ${diffClass}">
          ${formatNumber(p.lastDiff)} off<br><small>${pct}%</small>
        </div>
      </div>
    `;
  }).join('');

  const winner = winnerIdx >= 0 ? gameState.players[winnerIdx] : null;
  $('point-award').textContent = winner
    ? `${winner.name} gets the point! Closest guess wins.`
    : 'No winner this round.';

  renderLeaderboard('leaderboard-results');
  showScreen('screen-results');
}

function checkWinner() {
  const winner = gameState.players.find(p => p.score >= gameState.targetScore);
  if (!winner) return false;

  $('winner-name').textContent = `${winner.name} Wins!`;
  $('winner-score').textContent = `Final Score: ${winner.score}`;
  renderLeaderboard('final-leaderboard');
  showScreen('screen-winner');
  return true;
}

function nextRound() {
  gameState.currentRound += 1;
  gameState.currentPlayerTurn = 0;
  gameState.players.forEach(p => { p.currentGuess = 0; p.lastDiff = 0; p.lastGuess = 0; });
  pickRandomCountry();
  showPassScreen();
}

function initGame() {
  gameState.players = [];
  for (let i = 0; i < gameState.numPlayers; i++) {
    const nameInput = $(`name-${i}`);
    const name = nameInput ? nameInput.value.trim() || `Player ${i + 1}` : `Player ${i + 1}`;
    gameState.players.push({
      name,
      score: 0,
      currentGuess: 0,
      lastGuess: 0,
      lastDiff: 0
    });
  }
  gameState.currentRound = 1;
  gameState.currentPlayerTurn = 0;
  gameState.usedCountryIndices = [];
  renderLeaderboard('leaderboard-ready');
  showScreen('screen-ready');
}

async function loadData() {
  try {
    const res = await fetch('population-data.json');
    populationData = await res.json();
  } catch (e) {
    populationData = [];
    alert('Failed to load population data. Please ensure population-data.json exists.');
  }
}

function init() {
  loadData();

  setupSegmented('num-players-selector', 'numPlayers', buildNameInputs);
  setupSegmented('target-score-selector', 'targetScore');

  $('btn-setup-next').addEventListener('click', () => {
    buildNameInputs();
    showScreen('screen-names');
  });

  $('btn-names-next').addEventListener('click', () => {
    initGame();
  });

  $('btn-start-game').addEventListener('click', () => {
    pickRandomCountry();
    showPassScreen();
  });

  $('btn-pass-ready').addEventListener('click', () => {
    showGuessScreen();
  });

  $('btn-submit-guess').addEventListener('click', () => {
    const val = parseNumber($('guess-input').value);
    if (val <= 0) {
      alert('Please enter a valid population guess.');
      return;
    }
    gameState.players[gameState.currentPlayerTurn].currentGuess = val;
    gameState.currentPlayerTurn++;

    if (gameState.currentPlayerTurn < gameState.numPlayers) {
      showPassScreen();
    } else {
      finishRound();
    }
  });

  $('guess-input').addEventListener('input', (e) => {
    const raw = e.target.value;
    const digits = raw.replace(/\D/g, '');
    const formatted = formatNumber(digits);
    if (formatted !== raw) {
      e.target.value = formatted;
    }
  });

  $('guess-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      $('btn-submit-guess').click();
    }
  });

  $('btn-next-round').addEventListener('click', () => {
    if (!checkWinner()) {
      nextRound();
    }
  });

  $('btn-play-again').addEventListener('click', () => {
    showScreen('screen-setup');
  });
}

init();
