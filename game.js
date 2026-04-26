let populationData = [];
let factsData = [];

const gameState = {
  numPlayers: 2,
  targetScore: 5,
  players: [],
  usedCountryIndices: [],
  currentRound: 1,
  currentCountry: null,
  currentPlayerTurn: 0
};

const STORAGE_KEY = 'gameState';

function $(id) { return document.getElementById(id); }

let exitReturnScreen = null;

const cheatState = {
  flagged: false
};

const CHEAT_STORAGE_KEY = 'cheatLastActiveTime';
const CHEAT_ACTIVE_KEY = 'cheatIsTurnActive';
const CHEAT_DEPARTURE_KEY = 'cheatDepartureTime';
const CHEAT_THRESHOLD = 5000;
let heartbeatInterval = null;

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  $(id).classList.add('active');
}

function showExitModal(returnScreen) {
  exitReturnScreen = returnScreen;
  $('exit-modal').classList.add('active');
}

function hideExitModal() {
  $('exit-modal').classList.remove('active');
  exitReturnScreen = null;
}

function showCheatOverlay() {
  $('cheat-modal').classList.add('active');
}

function hideCheatOverlay() {
  $('cheat-modal').classList.remove('active');
}

function startHeartbeat() {
  if (heartbeatInterval) clearInterval(heartbeatInterval);
  localStorage.setItem(CHEAT_ACTIVE_KEY, 'true');
  localStorage.setItem(CHEAT_STORAGE_KEY, String(Date.now()));
  heartbeatInterval = setInterval(() => {
    localStorage.setItem(CHEAT_STORAGE_KEY, String(Date.now()));
  }, 500);
}

function stopHeartbeat() {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
  localStorage.removeItem(CHEAT_ACTIVE_KEY);
  localStorage.removeItem(CHEAT_STORAGE_KEY);
  localStorage.removeItem(CHEAT_DEPARTURE_KEY);
}

function saveCheatTimestamp() {
  if (localStorage.getItem(CHEAT_ACTIVE_KEY) === 'true') {
    // Write to departure key (never overwritten by heartbeat)
    localStorage.setItem(CHEAT_DEPARTURE_KEY, String(Date.now()));
  }
}

function checkCheatGap() {
  const isActive = localStorage.getItem(CHEAT_ACTIVE_KEY);
  const departureTime = parseInt(localStorage.getItem(CHEAT_DEPARTURE_KEY), 10);
  const heartbeatTime = parseInt(localStorage.getItem(CHEAT_STORAGE_KEY), 10);
  // Consume departure key so it doesn't re-trigger
  localStorage.removeItem(CHEAT_DEPARTURE_KEY);
  const referenceTime = departureTime || heartbeatTime;
  if (isActive === 'true' && referenceTime) {
    const gap = Date.now() - referenceTime;
    console.log(`[CheatDetection] Gap: ${(gap / 1000).toFixed(2)}s (via ${departureTime ? 'departure' : 'heartbeat'})`);
    if (gap > CHEAT_THRESHOLD) {
      cheatState.flagged = true;
      const activeScreen = document.querySelector('.screen.active');
      if (activeScreen && activeScreen.id === 'screen-guess') {
        showCheatOverlay();
      }
    }
  }
}

function skipTurn() {
  stopHeartbeat();
  const p = gameState.players[gameState.currentPlayerTurn];
  p.currentGuess = -1;
  p.lastDiff = Infinity;
  p.lastGuess = 0;
  cheatState.flagged = false;
  hideCheatOverlay();
  gameState.currentPlayerTurn++;
  if (gameState.currentPlayerTurn < gameState.numPlayers) {
    showPassScreen();
  } else {
    finishRound();
  }
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

function getAvatarColor(index) {
  const colors = ['#38bdf8', '#4ade80', '#f87171', '#fbbf24'];
  return colors[index % colors.length];
}

function getInitials(name) {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

function saveState(screenId) {
  const save = {
    numPlayers: gameState.numPlayers,
    targetScore: gameState.targetScore,
    players: gameState.players,
    usedCountryIndices: gameState.usedCountryIndices,
    currentRound: gameState.currentRound,
    currentPlayerTurn: gameState.currentPlayerTurn,
    currentCountryName: gameState.currentCountry ? gameState.currentCountry.country : null,
    screen: screenId
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(save));
}

function clearState() {
  localStorage.removeItem(STORAGE_KEY);
}

function restoreState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return false;
  try {
    const saved = JSON.parse(raw);
    gameState.numPlayers = saved.numPlayers;
    gameState.targetScore = saved.targetScore;
    gameState.players = saved.players;
    gameState.usedCountryIndices = saved.usedCountryIndices;
    gameState.currentRound = saved.currentRound;
    gameState.currentPlayerTurn = saved.currentPlayerTurn;
    if (saved.currentCountryName && populationData.length > 0) {
      gameState.currentCountry = populationData.find(c => c.country === saved.currentCountryName) || null;
    }
    return saved.screen || false;
  } catch (e) {
    clearState();
    return false;
  }
}

function syncSegmented(selectorId, value) {
  const container = $(selectorId);
  container.querySelectorAll('button').forEach(b => {
    b.classList.toggle('active', parseInt(b.dataset.value, 10) === value);
  });
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
      <label class="toggle-label">
        <input type="checkbox" id="hint-${i}" class="toggle-input">
        <span class="toggle-slider"></span>
        <span class="toggle-text">Hints</span>
      </label>
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
  saveState('screen-pass');
}

function getRoundPoints() {
  const numPlayers = gameState.numPlayers;
  const pointTable = {
    2: [1, 0],
    3: [3, 1, 0],
    4: [5, 3, 1, 0]
  };
  const points = pointTable[numPlayers] || [1, 0];

  const sorted = [...gameState.players].map((p, i) => ({ idx: i, diff: p.lastDiff }))
    .sort((a, b) => a.diff - b.diff);

  const result = new Array(numPlayers).fill(0);
  let i = 0;
  while (i < numPlayers) {
    let j = i + 1;
    while (j < numPlayers && sorted[j].diff === sorted[i].diff) j++;
    const groupSize = j - i;
    let sumPoints = 0;
    for (let k = i; k < j && k < points.length; k++) {
      sumPoints += points[k];
    }
    const ptsPerPlayer = Math.floor(sumPoints / groupSize);
    for (let k = i; k < j; k++) {
      result[sorted[k].idx] = ptsPerPlayer;
    }
    i = j;
  }
  return result;
}

function getHintInterval(pop) {
  if (pop < 200000) return { min: 0, max: 200000, label: '0 – 200,000' };
  if (pop < 1000000) return { min: 200000, max: 1000000, label: '200,000 – 1,000,000' };
  if (pop < 10000000) return { min: 1000000, max: 10000000, label: '1,000,000 – 10,000,000' };
  if (pop < 50000000) return { min: 10000000, max: 50000000, label: '10,000,000 – 50,000,000' };
  if (pop < 100000000) return { min: 50000000, max: 100000000, label: '50,000,000 – 100,000,000' };
  if (pop < 200000000) return { min: 100000000, max: 200000000, label: '100,000,000 – 200,000,000' };
  if (pop < 500000000) return { min: 200000000, max: 500000000, label: '200,000,000 – 500,000,000' };
  return { min: 500000000, max: Infinity, label: '500,000,000+' };
}

function showGuessScreen() {
  const p = gameState.players[gameState.currentPlayerTurn];
  $('guess-round').textContent = gameState.currentRound;
  $('guess-player-badge').textContent = p.name;
  $('guess-country').textContent = gameState.currentCountry.country;
  const hintEl = $('guess-hint');
  if (p.hints && gameState.currentCountry) {
    const interval = getHintInterval(gameState.currentCountry.population);
    hintEl.textContent = `Hint: between ${interval.label}`;
    hintEl.style.display = 'block';
  } else {
    hintEl.style.display = 'none';
  }
  $('guess-input').value = '';
  showScreen('screen-guess');
  $('guess-input').focus();
  checkCheatGap();
  startHeartbeat();
  saveState('screen-guess');
}

function renderResultsScreen() {
  const actual = gameState.currentCountry.population;
  const roundPoints = getRoundPoints();

  let winnerIdx = -1;
  let bestDiff = Infinity;
  gameState.players.forEach((p, i) => {
    if (p.lastDiff < bestDiff) {
      bestDiff = p.lastDiff;
      winnerIdx = i;
    }
  });

  $('results-country').textContent = gameState.currentCountry.country;
  $('results-actual').textContent = formatNumber(actual);

  const fact = getRandomFact(gameState.currentCountry.country);
  $('results-fact').textContent = fact ? `Fun Fact: ${fact}` : '';
  $('results-fact').style.display = fact ? 'block' : 'none';

  const sortedByDiff = [...gameState.players].map((p, i) => ({ p, i, pts: roundPoints[i] }))
    .sort((a, b) => a.p.lastDiff - b.p.lastDiff);
  const list = $('results-list');
  list.innerHTML = sortedByDiff.map(({ p, i, pts }) => {
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
        <div class="result-points">+${pts}</div>
      </div>
    `;
  }).join('');

  const pointMessages = sortedByDiff.filter(({ pts }) => pts > 0)
    .map(({ p, pts }) => `${p.name} +${pts}`).join(', ');
  $('point-award').textContent = pointMessages
    ? `Points awarded: ${pointMessages}`
    : 'No points this round.';

  renderLeaderboard('leaderboard-results');
  showScreen('screen-results');
}

function finishRound() {
  stopHeartbeat();
  const actual = gameState.currentCountry.population;

  gameState.players.forEach((p, i) => {
    if (p.currentGuess < 0) {
      p.lastDiff = Infinity;
      p.lastGuess = 0;
    } else {
      const diff = Math.abs(p.currentGuess - actual);
      p.lastDiff = diff;
      p.lastGuess = p.currentGuess;
    }
  });

  const roundPoints = getRoundPoints();
  gameState.players.forEach((p, i) => {
    p.score += roundPoints[i];
  });

  renderResultsScreen();
  saveState('screen-results');
}

function checkWinner() {
  const winner = gameState.players.find(p => p.score >= gameState.targetScore);
  if (!winner) return false;
  stopHeartbeat();

  $('winner-name').textContent = `${winner.name} Wins!`;
  $('winner-score').textContent = `Final Score: ${winner.score}`;
  renderLeaderboard('final-leaderboard');
  showScreen('screen-winner');
  clearState();
  return true;
}

function nextRound() {
  stopHeartbeat();
  gameState.currentRound += 1;
  gameState.currentPlayerTurn = 0;
  gameState.players.forEach(p => { p.currentGuess = 0; p.lastDiff = 0; p.lastGuess = 0; });
  cheatState.flagged = false;
  pickRandomCountry();
  showPassScreen();
}

function initGame() {
  stopHeartbeat();
  cheatState.flagged = false;
  gameState.players = [];
  for (let i = 0; i < gameState.numPlayers; i++) {
    const nameInput = $(`name-${i}`);
    const hintInput = $(`hint-${i}`);
    const name = nameInput ? nameInput.value.trim() || `Player ${i + 1}` : `Player ${i + 1}`;
    const hintEnabled = hintInput ? hintInput.checked : false;
    gameState.players.push({
      name,
      score: 0,
      currentGuess: 0,
      lastGuess: 0,
      lastDiff: 0,
      hints: hintEnabled
    });
  }
  gameState.currentRound = 1;
  gameState.currentPlayerTurn = 0;
  gameState.usedCountryIndices = [];
  renderLeaderboard('leaderboard-ready');
  showScreen('screen-ready');
  saveState('screen-ready');
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

async function loadFacts() {
  try {
    const res = await fetch('facts.json');
    factsData = await res.json();
  } catch (e) {
    factsData = [];
  }
}

function getRandomFact(countryName) {
  const entry = factsData.find(f => f.country === countryName);
  if (!entry || !entry.facts || entry.facts.length === 0) return null;
  const idx = Math.floor(Math.random() * entry.facts.length);
  return entry.facts[idx];
}

async function init() {
  await Promise.all([loadData(), loadFacts()]);

  setupSegmented('num-players-selector', 'numPlayers', buildNameInputs);
  setupSegmented('target-score-selector', 'targetScore');
  buildNameInputs();

  const savedScreen = restoreState();
  if (savedScreen) {
    syncSegmented('num-players-selector', gameState.numPlayers);
    syncSegmented('target-score-selector', gameState.targetScore);
    if (savedScreen === 'screen-ready') {
      renderLeaderboard('leaderboard-ready');
      showScreen('screen-ready');
    } else if (savedScreen === 'screen-pass') {
      showPassScreen();
    } else if (savedScreen === 'screen-guess') {
      showGuessScreen();
    } else if (savedScreen === 'screen-results') {
      renderResultsScreen();
    }
  }

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
    stopHeartbeat();
    clearState();
    showScreen('screen-setup');
  });

  // Exit game handlers
  const exitButtons = [
    { id: 'btn-exit-ready', screen: 'screen-ready' },
    { id: 'btn-exit-pass', screen: 'screen-pass' },
    { id: 'btn-exit-guess', screen: 'screen-guess' },
    { id: 'btn-exit-results', screen: 'screen-results' }
  ];

  exitButtons.forEach(({ id, screen }) => {
    $(id).addEventListener('click', () => {
      showExitModal(screen);
    });
  });

  $('btn-exit-cancel').addEventListener('click', () => {
    hideExitModal();
    if (exitReturnScreen) {
      showScreen(exitReturnScreen);
    }
  });

  $('btn-exit-confirm').addEventListener('click', () => {
    hideExitModal();
    stopHeartbeat();
    clearState();
    showScreen('screen-setup');
  });

  // Cheat Detection: unified heartbeat + localStorage
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      saveCheatTimestamp();
    } else {
      checkCheatGap();
    }
  });

  window.addEventListener('pagehide', () => {
    saveCheatTimestamp();
  });

  window.addEventListener('pageshow', (e) => {
    checkCheatGap();
    const activeScreen = document.querySelector('.screen.active');
    if (activeScreen && activeScreen.id === 'screen-guess') {
      startHeartbeat();
    }
  });

  $('btn-cheat-skip').addEventListener('click', () => {
    skipTurn();
  });
}

init();
