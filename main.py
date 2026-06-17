<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Хроники города – Расширенная версия</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Georgia', serif; background: #1a1a2e; color: #e0d6c2; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 4px; background-image: radial-gradient(ellipse at center, #16213e 0%, #0f0f1a 100%); }
        .game-container { width: 100%; max-width: 880px; background: rgba(22, 33, 62, 0.92); border: 2px solid #8b7355; border-radius: 12px; padding: 10px 8px; box-shadow: 0 0 40px rgba(0,0,0,0.7); max-height: 99vh; overflow-y: auto; display: flex; flex-direction: column; gap: 5px; }
        .game-header { text-align: center; border-bottom: 1px solid #8b7355; padding-bottom: 3px; }
        .game-header h1 { font-size: 1.1rem; color: #d4af37; letter-spacing: 2px; }
        .subtitle { font-style: italic; color: #a09080; font-size: 0.58rem; }
        .main-layout { display: flex; gap: 6px; flex-wrap: wrap; }
        .left-col { flex: 1.8; min-width: 260px; display: flex; flex-direction: column; gap: 4px; }
        .right-col { flex: 1.2; min-width: 220px; display: flex; flex-direction: column; gap: 4px; }
        .city-phase { text-align: center; font-size: 0.65rem; color: #c5a86b; }
        .context-hint { text-align: center; font-size: 0.55rem; font-style: italic; padding: 2px 5px; border-radius: 4px; }
        .hint-story { color: #d4af37; background: rgba(212,175,55,0.1); }
        .hint-critical { color: #e74c3c; background: rgba(231,76,60,0.15); }
        .hint-important { color: #e67e22; background: rgba(230,126,34,0.1); }
        .hint-normal { color: #7d9b7d; }
        .stats-panel { display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1px; background: rgba(0,0,0,0.3); border-radius: 5px; padding: 3px 2px; border: 1px solid #4a3f35; }
        .stat-item { text-align: center; flex: 1; min-width: 35px; }
        .stat-icon { font-size: 0.7rem; display: block; }
        .stat-value { font-size: 0.7rem; font-weight: bold; color: #f0c27b; }
        .stat-label { font-size: 0.4rem; color: #9a8b7a; text-transform: uppercase; }
        .stat-danger { color: #e74c3c !important; animation: pulse 1s infinite; }
        .stat-warning { color: #e67e22 !important; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
        .turn-counter { text-align: center; color: #a09080; font-size: 0.6rem; }
        .turn-counter span { color: #d4af37; font-weight: bold; }
        .progress-bar { width: 100%; height: 2px; background: #3a2f24; border-radius: 2px; overflow: hidden; }
        .progress-fill { height: 100%; background: #d4af37; transition: width 0.5s; border-radius: 2px; }

        /* Карта города */
        .city-map { background: #1a2a1a; border: 2px solid #4a6a3a; border-radius: 8px; padding: 8px; font-family: 'Courier New', monospace; font-size: 0.55rem; line-height: 1.1; color: #8ab88a; text-align: center; white-space: pre; min-height: 100px; }
        .city-map .river { color: #5a9aca; }
        .city-map .house { color: #c8a86b; }
        .city-map .market { color: #d4af37; }
        .city-map .temple { color: #c8c8ff; }
        .city-map .walls { color: #8a8a8a; }
        .city-map .tree { color: #5a8a3a; }
        .city-map .guild { color: #c8a8d8; }

        /* Панели */
        .panel { background: rgba(0,0,0,0.35); border: 1px solid #4a3f35; border-radius: 5px; padding: 5px 6px; }
        .panel h3 { font-size: 0.6rem; color: #d4af37; text-align: center; margin-bottom: 3px; }
        .panel-row { display: flex; justify-content: space-between; align-items: center; padding: 2px 0; border-bottom: 1px dotted #3a2f24; font-size: 0.55rem; }
        .panel-row:last-child { border-bottom: none; }
        .row-name { color: #c5a86b; }
        .row-detail { color: #7d9b7d; font-size: 0.48rem; }
        .row-value { color: #d4af37; font-weight: bold; }

        /* Событие */
        .event-card { background: #2a1f14; border: 2px solid #8b7355; border-radius: 8px; padding: 8px 7px; box-shadow: 0 3px 15px rgba(0,0,0,0.6); animation: fadeIn 0.3s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        .event-icon { font-size: 1.2rem; text-align: center; display: block; margin-bottom: 2px; }
        .event-title { font-size: 0.8rem; color: #d4af37; text-align: center; margin-bottom: 2px; border-bottom: 1px dashed #5a4a3a; padding-bottom: 2px; }
        .event-description { font-size: 0.62rem; line-height: 1.25; color: #c5b8a8; margin-bottom: 5px; white-space: pre-line; }
        .event-urgency { font-size: 0.45rem; text-align: center; margin-bottom: 2px; padding: 1px 3px; border-radius: 3px; display: inline-block; width: 100%; }
        .urgency-critical { background: rgba(231,76,60,0.3); color: #e74c3c; }
        .urgency-important { background: rgba(230,126,34,0.3); color: #e67e22; }
        .urgency-story { background: rgba(212,175,55,0.15); color: #d4af37; }
        .urgency-quest { background: rgba(155,89,182,0.3); color: #c39bdb; }
        .urgency-battle { background: rgba(231,76,60,0.35); color: #ff6b6b; }
        .choices-container { display: flex; flex-direction: column; gap: 2px; }
        .choice-btn { background: linear-gradient(180deg, #3e2e1f 0%, #2a1f14 100%); border: 1px solid #8b7355; color: #e0d6c2; padding: 4px 6px; border-radius: 4px; cursor: pointer; font-family: 'Georgia', serif; font-size: 0.6rem; text-align: left; transition: all 0.2s; line-height: 1.1; }
        .choice-btn:hover { background: linear-gradient(180deg, #5a3e28 0%, #3e2e1f 100%); border-color: #d4af37; }
        .choice-btn .hint { display: block; font-size: 0.45rem; color: #9a8b7a; margin-top: 1px; }
        .choice-btn.locked { opacity: 0.4; pointer-events: none; background: #1a1a1a; }
        .restart-btn { background: transparent; border: 1px solid #6a4f3a; color: #9a8b7a; padding: 2px 10px; border-radius: 12px; cursor: pointer; font-family: 'Georgia', serif; margin: 2px auto 0; display: block; font-size: 0.55rem; }
        .restart-btn:hover { border-color: #c0392b; color: #e74c3c; }
        .game-over-overlay { background: rgba(0,0,0,0.8); border-radius: 8px; padding: 10px; text-align: center; border: 1px solid #c0392b; }
        .game-over-overlay h2 { color: #c0392b; margin-bottom: 3px; font-size: 0.8rem; }
        .game-over-overlay p { font-size: 0.6rem; }
        .cooldown-indicator { font-size: 0.4rem; color: #6a5a4a; text-align: center; }
        .small-btn { background: rgba(139,115,85,0.3); border: 1px solid #5a4a3a; color: #c5b8a8; padding: 1px 6px; border-radius: 8px; cursor: pointer; font-size: 0.45rem; font-family: 'Georgia', serif; }
        .small-btn:hover { background: rgba(139,115,85,0.5); color: #d4af37; }
        .trade-active { color: #5a9aca; }
        .guild-level { color: #d4af37; font-size: 0.45rem; }
    </style>
</head>
<body>
<div class="game-container" id="gameContainer">
    <div class="game-header"><h1>🏘️ ХРОНИКИ ГОРОДА</h1><div class="subtitle">Карта · Гильдии · Торговля · Битвы · Артефакты</div></div>
    <div class="main-layout">
        <div class="left-col">
            <div class="city-phase" id="cityPhase">🌱 Поселение</div>
            <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:5%"></div></div>
            <div class="context-hint" id="contextHint"></div>
            <div class="stats-panel">
                <div class="stat-item"><span class="stat-icon">👥</span><span class="stat-value" id="population">12</span><span class="stat-label">Жители</span></div>
                <div class="stat-item"><span class="stat-icon">💰</span><span class="stat-value" id="gold">8</span><span class="stat-label">Золото</span></div>
                <div class="stat-item"><span class="stat-icon">😊</span><span class="stat-value" id="happiness">60</span><span class="stat-label">Дух</span></div>
                <div class="stat-item"><span class="stat-icon">🏠</span><span class="stat-value" id="houses">3</span><span class="stat-label">Дома</span></div>
                <div class="stat-item"><span class="stat-icon">🌾</span><span class="stat-value" id="food">25</span><span class="stat-label">Еда</span></div>
                <div class="stat-item"><span class="stat-icon">🔬</span><span class="stat-value" id="science">0</span><span class="stat-label">Наука</span></div>
            </div>
            <div class="turn-counter">📜 <span id="turnDisplay">Год 1, Весна</span></div>
            <div id="eventCardArea"></div>
            <div class="cooldown-indicator" id="cooldownInfo"></div>
            <button class="restart-btn" id="restartButton">🔄 Основать заново</button>
        </div>
        <div class="right-col">
            <!-- Карта города -->
            <div class="city-map" id="cityMap"></div>
            <!-- Легендарные предметы -->
            <div class="panel" id="artifactsPanel"><h3>💎 Артефакты</h3><div id="artifactsList"></div></div>
            <!-- Торговые маршруты -->
            <div class="panel" id="tradeRoutesPanel"><h3>🐪 Торговля</h3><div id="tradeRoutesList"></div></div>
            <!-- Гильдии -->
            <div class="panel" id="guildsPanel"><h3>🏛️ Гильдии</h3><div id="guildsList"></div></div>
            <!-- Советники -->
            <div class="panel" id="advisorsPanel"><h3>👥 Советники</h3><div id="advisorsList"></div></div>
            <!-- Технологии -->
            <div class="panel" id="techPanel"><h3>🔬 Технологии</h3><div id="techList"></div></div>
            <!-- Репутация -->
            <div class="panel" id="reputationPanel"><h3>🌍 Отношения</h3><div id="reputationList"></div></div>
            <!-- Журнал -->
            <div class="panel" id="journalPanel" style="max-height:100px;overflow-y:auto;"><h3>📜 Журнал</h3><div id="journalEntries"></div></div>
        </div>
    </div>
</div>

<script>
(function() {
    const state = {
        population: 12, gold: 8, happiness: 60, houses: 3, food: 25, science: 0,
        turn: 1, seasonIndex: 0, gameOver: false, gameOverMessage: '',
        flags: {}, chainContext: null, history: [], lastEventId: null,
        cooldowns: {}, globalStep: 0, storyPhase: 0,
        location: null,
        // Новые системы
        artifacts: [], // [{id, name, icon, bonus, desc}]
        tradeRoutes: [], // [{id, target, goods, profit, risk, turnsLeft}]
        guilds: {
            merchants: { name: 'Гильдия купцов', level: 0, bonus: '💰 Торговля +5', cost: 40 },
            warriors: { name: 'Гильдия воинов', level: 0, bonus: '⚔️ Защита +10%', cost: 50 },
            thieves: { name: 'Гильдия теней', level: 0, bonus: '🕵️ Информация', cost: 45 },
            mages: { name: 'Гильдия магов', level: 0, bonus: '🔮 Наука +3', cost: 60 },
            artisans: { name: 'Гильдия ремесленников', level: 0, bonus: '🏠 Стройка дешевле', cost: 35 }
        },
        battle: null, // {enemy, enemyStrength, playerStrength, phase}
        advisors: {
            general: { name: 'Воевода', loyalty: 70, bonus: '🛡️ Защита', hired: true },
            treasurer: { name: 'Казначей', loyalty: 75, bonus: '💰 Доход', hired: false },
            priest: { name: 'Жрец', loyalty: 80, bonus: '😊 Счастье', hired: false },
            scholar: { name: 'Учёный', loyalty: 65, bonus: '🔬 Наука', hired: false },
            spy: { name: 'Шпион', loyalty: 50, bonus: '🕵️ Инфо', hired: false }
        },
        technologies: {
            irrigation: { name: 'Орошение', cost: 30, researched: false },
            medicine: { name: 'Медицина', cost: 40, researched: false },
            masonry: { name: 'Каменная кладка', cost: 35, researched: false },
            engineering: { name: 'Инженерия', cost: 60, researched: false },
            cartography: { name: 'Картография', cost: 45, researched: false },
            guilds: { name: 'Гильдии', cost: 50, researched: false },
            navigation: { name: 'Навигация', cost: 70, researched: false },
            alchemy: { name: 'Алхимия', cost: 80, researched: false }
        },
        reputation: {
            northKingdom: { name: 'Север', value: 50 },
            southEmpire: { name: 'Юг', value: 40 },
            merchantGuild: { name: 'Купцы', value: 60 },
            hillTribes: { name: 'Горцы', value: 30 }
        },
        activeQuests: [], eventUsage: {}, lastCategory: ''
    };

    const allFlags = 'locationChosen,shelterBuilt,wellBuilt,marketBuilt,wallsBuilt,templeBuilt,barracksBuilt,libraryBuilt,portBuilt,aqueductBuilt,guildBuilt,banditsDealt,plagueDealt,dragonDealt,allianceFormed,goldMineOpened,universityBuilt,floodDealt,droughtDealt,relicFound,strangerDealt,firstHunt,firstTrade,firstFestival,thievesDealt,fireDealt,cultDealt,ambassadorDealt,arenaBuilt,explorerDealt,mirageDealt,princeDealt,waterSource,blacksmithDealt,tournamentDealt,refugeesDealt,spyDealt,monopolyDealt,inventorDealt,mineDealt,ghostDealt,prophetDealt,shipwreckDealt,pilgrimsDealt,oracleDealt,censusDealt,feastDealt,sabotageDealt,meteorDealt,hermitDealt,runawayDealt,counterfeitDealt,blightDealt,minstrelDealt,beastDealt,treasureDealt,iceDealt,prophecyDealt,ratsDealt,advisorEvent1,advisorEvent2,questAmulet,questDragonEgg,questTraitor,artifactSword,artifactCrown,artifactBook'.split(',');
    allFlags.forEach(f => state.flags[f] = false);

    const seasons = ['Весна','Лето','Осень','Зима'];
    const CD_BASE = 3, CD_VAR = 1;

    // ===== КАРТА ГОРОДА =====
    function renderCityMap() {
        const el = document.getElementById('cityMap');
        if (!el) return;
        const w = 20, h = 10;
        let map = Array(h).fill(null).map(() => Array(w).fill('·'));
        const loc = state.flags.location;

        // Река
        if (loc === 'river') { for (let y = 0; y < h; y++) map[y][16] = '║'; map[3][16] = '║'; map[7][16] = '║'; }

        // Дома (зависят от количества)
        const houseCount = Math.min(20, Math.floor(state.houses / 2));
        const housePositions = [[2,3],[3,3],[4,3],[5,4],[2,5],[3,5],[6,4],[4,6],[5,6],[7,5],[2,7],[3,7],[4,8],[5,8],[6,7],[7,7],[8,6],[8,8],[3,9],[5,9]];
        for (let i = 0; i < Math.min(houseCount, housePositions.length); i++) {
            const [y, x] = housePositions[i]; if (y < h && x < w) map[y][x] = '⌂';
        }

        // Рынок
        if (state.flags.marketBuilt) { map[5][9] = '🏪'; map[5][10] = '▣'; map[6][9] = '▣'; map[6][10] = '▣'; }

        // Храм
        if (state.flags.templeBuilt) { map[3][12] = '⛪'; map[4][12] = '┃'; }

        // Стены
        if (state.flags.wallsBuilt) {
            for (let x = 1; x < 15; x++) { if (map[1][x] === '·') map[1][x] = '━'; if (map[8][x] === '·') map[8][x] = '━'; }
            for (let y = 1; y < 8; y++) { if (map[y][1] === '·') map[y][1] = '┃';
                if (map[y][14] === '·') map[y][14] = '┃'; }
        }

        // Деревья (лес)
        if (loc === 'forest') { map[2][18] = '♣';
            map[4][18] = '♣';
            map[6][19] = '♣';
            map[3][17] = '♣'; }

        // Холмы
        if (loc === 'hills') { map[7][17] = '▲';
            map[7][18] = '▲';
            map[6][19] = '▲'; }

        // Казармы
        if (state.flags.barracksBuilt) { map[6][2] = '⚔';
            map[7][2] = '⚔'; }

        // Порт
        if (state.flags.portBuilt) { map[2][15] = '⚓'; }

        // Арена
        if (state.flags.arenaBuilt) { map[4][4] = '⊙'; }

        let html = '';
        for (let y = 0; y < h; y++) {
            let row = '';
            for (let x = 0; x < w; x++) {
                let ch = map[y][x];
                if (ch === '║' || ch === '━' || ch === '┃') row += `<span class="river">${ch}</span>`;
                else if (ch === '⌂') row += `<span class="house">${ch}</span>`;
                else if (ch === '🏪' || ch === '▣') row += `<span class="market">${ch}</span>`;
                else if (ch === '⛪') row += `<span class="temple">${ch}</span>`;
                else if (ch === '♣') row += `<span class="tree">${ch}</span>`;
                else if (ch === '⚔' || ch === '⊙') row += `<span class="walls">${ch}</span>`;
                else if (ch === '⚓') row += `<span class="guild">${ch}</span>`;
                else row += ch;
            }
            html += row + '\n';
        }
        el.innerHTML = html;
    }

    // ===== АРТЕФАКТЫ =====
    function addArtifact(artifact) {
        if (state.artifacts.find(a => a.id === artifact.id)) return;
        state.artifacts.push(artifact);
        applyArtifactBonus(artifact);
        addJournalEntry(`Найден артефакт: ${artifact.name}!`);
    }
    function applyArtifactBonus(a) {
        if (a.id === 'sword_of_valor') { state.happiness += 10; }
        if (a.id === 'crown_of_wisdom') { state.science += 20; }
        if (a.id === 'book_of_secrets') { state.science += 15;
            state.flags.plagueDealt = true; }
        if (a.id === 'merchant_ring') { state.gold += 30; }
        if (a.id === 'healing_amulet') { state.population += 5;
            state.happiness += 10; }
    }
    function updateArtifacts() {
        const el = document.getElementById('artifactsList');
        if (!el) return;
        if (state.artifacts.length === 0) { el.innerHTML = '<div class="panel-row"><span class="row-name">Нет артефактов</span></div>'; return; }
        el.innerHTML = state.artifacts.map(a => `<div class="panel-row"><span class="row-name">${a.icon} ${a.name}</span><span class="row-detail">${a.bonus}</span></div>`).join('');
    }

    // ===== ТОРГОВЫЕ МАРШРУТЫ =====
    function startTradeRoute(target, goods, cost, profit, risk, duration) {
        if (state.gold < cost) return false;
        state.gold -= cost;
        state.tradeRoutes.push({ id: Date.now(), target, goods, profit, risk, turnsLeft: duration });
        addJournalEntry(`Отправлен караван в ${target} с ${goods}.`);
        return true;
    }
    function updateTradeRoutes() {
        const el = document.getElementById('tradeRoutesList');
        if (!el) return;
        if (state.tradeRoutes.length === 0) { el.innerHTML = '<div class="panel-row"><span class="row-name">Нет маршрутов</span></div><button class="small-btn" onclick="openTradeMenu()">➕ Отправить</button>'; return; }
        el.innerHTML = state.tradeRoutes.map(tr => {
            const status = tr.turnsLeft > 0 ? `⏳ ${tr.turnsLeft} ход.` : '✅ Прибыл!';
            const cls = tr.turnsLeft > 0 ? 'trade-active' : '';
            return `<div class="panel-row ${cls}"><span class="row-name">🐪 ${tr.target}</span><span class="row-detail">${tr.goods} | ${status}</span></div>`;
        }).join('') + '<button class="small-btn" onclick="openTradeMenu()">➕ Новый</button>';
    }
    window.openTradeMenu = function() {
        const routes = [
            { target: 'Северное королевство', goods: 'Меха', cost: 20, profit: 40, risk: 0.2, duration: 3 },
            { target: 'Южная империя', goods: 'Вино', cost: 25, profit: 55, risk: 0.35, duration: 4 },
            { target: 'Горные племена', goods: 'Инструменты', cost: 15, profit: 30, risk: 0.15, duration: 2 },
            { target: 'Гильдия купцов', goods: 'Ткани', cost: 30, profit: 50, risk: 0.1, duration: 3 },
        ];
        const available = routes.filter(r => state.reputation[r.target.split(' ')[0].toLowerCase()] || state.reputation.merchantGuild);
        if (available.length === 0) { alert('Нет доступных маршрутов!'); return; }
        const r = available[Math.floor(Math.random() * available.length)];
        if (confirm(`Отправить караван в ${r.target}?\nТовар: ${r.goods}\nВложения: ${r.cost}💰\nПрибыль: ${r.profit}💰\nРиск: ${Math.floor(r.risk*100)}%\nДлительность: ${r.duration} ходов`)) {
            if (startTradeRoute(r.target, r.goods, r.cost, r.profit, r.risk, r.duration)) {
                updateTradeRoutes(); updateUI();
            } else { alert('Недостаточно золота!'); }
        }
    };
    function processTradeRoutes() {
        state.tradeRoutes = state.tradeRoutes.filter(tr => {
            if (tr.turnsLeft > 0) { tr.turnsLeft--; return true; }
            if (Math.random() < tr.risk) { addJournalEntry(`Караван из ${tr.target} ограблен! Потеряно.`); return false; }
            state.gold += tr.profit;
            addJournalEntry(`Караван из ${tr.target} вернулся! +${tr.profit}💰`);
            return false;
        });
    }

    // ===== ГИЛЬДИИ =====
    function upgradeGuild(key) {
        const g = state.guilds[key];
        if (!g || state.gold < g.cost) return false;
        state.gold -= g.cost;
        g.level++;
        g.cost = Math.floor(g.cost * 1.5);
        if (key === 'merchants') state.flags.marketBuilt = true;
        if (key === 'warriors') state.flags.barracksBuilt = true;
        addJournalEntry(`Гильдия "${g.name}" улучшена до ур. ${g.level}!`);
        return true;
    }
    function updateGuilds() {
        const el = document.getElementById('guildsList');
        if (!el) return;
        el.innerHTML = Object.entries(state.guilds).map(([key, g]) => {
            return `<div class="panel-row">
                <span class="row-name">${g.level > 0 ? '✅' : '❌'} ${g.name}</span>
                <span class="guild-level">Ур.${g.level} ${g.bonus}</span>
                ${g.level === 0 ? `<button class="small-btn" onclick="upgradeGuild('${key}')">${g.cost}💰</button>` : `<button class="small-btn" onclick="upgradeGuild('${key}')">↑${g.cost}💰</button>`}
            </div>`;
        }).join('');
    }
    window.upgradeGuild = function(key) { if (upgradeGuild(key)) { updateGuilds();
            updateUI(); } else alert('Недостаточно золота!'); };

    // ===== БОЕВАЯ СИСТЕМА =====
    function startBattle(enemy, enemyStr) {
        let playerStr = 10 + Math.floor(state.population / 20);
        if (state.flags.wallsBuilt) playerStr += 15;
        if (state.flags.barracksBuilt) playerStr += 10;
        if (state.advisors.general.hired) playerStr += 5;
        if (state.guilds.warriors.level > 0) playerStr += state.guilds.warriors.level * 8;
        if (state.artifacts.find(a => a.id === 'sword_of_valor')) playerStr += 20;
        state.battle = { enemy, enemyStrength: enemyStr, playerStrength: playerStr, phase: 'preparation' };
    }
    function getBattleEvent() {
        if (!state.battle) return null;
        if (state.battle.phase === 'preparation') {
            return {
                id: 'battle_prep', title: `⚔️ Битва с ${state.battle.enemy}!`, icon: '⚔️',
                desc: `Враги у ворот!\n\n${state.battle.enemy}: сила ${state.battle.enemyStrength}\nВаша армия: сила ${state.battle.playerStrength}\n\nКак поведём войска?`,
                choices: [
                    { text: 'В атаку! (+20% сила, риск)', hint: 'Риск потерь',
                        action: () => { state.battle.playerStrength = Math.floor(state.battle.playerStrength * 1.2);
                            state.battle.phase = 'resolve';
                            resolveBattle(); } },
                    { text: 'Держать оборону', hint: 'Безопаснее',
                        action: () => { state.battle.playerStrength += 5;
                            state.battle.phase = 'resolve';
                            resolveBattle(); } },
                    { text: 'Хитрый манёвр', hint: '💰-20 | +30% сила',
                        action: () => { state.gold -= 20;
                            state.battle.playerStrength = Math.floor(state.battle.playerStrength * 1.3);
                            state.battle.phase = 'resolve';
                            resolveBattle(); }, cond: () => state.gold >= 20 },
                ]
            };
        }
        return null;
    }
    function resolveBattle() {
        const b = state.battle;
        const playerRoll = b.playerStrength + Math.floor(Math.random() * 20);
        const enemyRoll = b.enemyStrength + Math.floor(Math.random() * 20);

        if (playerRoll >= enemyRoll) {
            const loot = Math.floor(b.enemyStrength * 1.5);
            state.gold += loot;
            state.happiness += 15;
            addJournalEntry(`Победа над ${b.enemy}! +${loot}💰`);
            alert(`⚔️ Победа! Ваша армия разбила ${b.enemy}. Захвачено ${loot} золота.`);
        } else {
            const losses = Math.floor(state.population * 0.1) + 5;
            state.population -= losses;
            state.happiness -= 20;
            state.houses -= Math.floor(state.houses * 0.05);
            addJournalEntry(`Поражение от ${b.enemy}. Потери: ${losses} чел.`);
            alert(`💔 Поражение... ${b.enemy} разграбили город. Потеряно ${losses} жителей.`);
        }
        state.battle = null;
    }

    // ===== ЖУРНАЛ =====
    function addJournalEntry(text) { state.history.unshift({ text, turn: state.turn, season: seasons[state.seasonIndex] }); if (state.history.length > 10) state.history.length = 10;
        updateJournal(); }

    function updateJournal() { const el = document.getElementById('journalEntries'); if (!el) return;
        el.innerHTML = state.history.slice(0, 10).map(h => `<div class="panel-row"><span class="row-name">Год ${h.turn}, ${h.season}:</span> <span class="row-detail">${h.text}</span></div>`).join(''); }

    // ===== СОВЕТНИКИ =====
    function updateAdvisors() { const el = document.getElementById('advisorsList'); if (!el) return;
        el.innerHTML = Object.entries(state.advisors).map(([key, a]) => { const status = a.hired ? '✅' : '❌'; const cost = key ===
                'general' ? '' : ` [${getAdvisorCost(key)}💰]`; return `<div class="panel-row"><span class="row-name">${status} ${a.name}</span><span class="row-detail">${a.bonus} ❤️${a.loyalty}%</span>${!a.hired&&key!=='general'?`<button class="small-btn" onclick="hireAdvisor('${key}')">Нанять${cost}</button>`:''}</div>`; })
            .join(''); }

    function getAdvisorCost(key) { const costs = { treasurer: 30, priest: 25, scholar: 40, spy: 50 }; return costs[key] || 30; }
    window.hireAdvisor = function(key) { const cost = getAdvisorCost(key); if (state.gold >= cost && !state.advisors[key]
            .hired) { state.gold -= cost;
            state.advisors[key].hired = true;
            state.advisors[key].loyalty = 60 + Math.floor(Math.random() * 30);
            addJournalEntry(`Нанят советник: ${state.advisors[key].name}`);
            updateAdvisors();
            updateUI(); } else if (state.gold < cost) { alert('Недостаточно золота!'); } };

    // ===== ТЕХНОЛОГИИ =====
    function updateTech() { const el = document.getElementById('techList'); if (!el) return;
        el.innerHTML = Object.entries(state.technologies).map(([key, t]) => { let cls = 'tech-locked',
                txt = '🔒'; if (t.researched) { cls = 'tech-researched';
                txt = '✅'; } else if (state.science >= t.cost * 0.5 && state.gold >= t.cost) { cls =
                    'tech-available';
                txt = `🔬${t.cost}💰`; } else { txt = `🔒(${Math.floor(t.cost*0.5)}📚)`; } return `<div class="panel-row"><span class="row-name">${t.name}</span><span class="row-detail ${cls}" ${!t.researched&&state.science>=t.cost*0.5&&state.gold>=t.cost?`onclick="researchTech('${key}')"`:''}>${txt}</span></div>`; })
            .join(''); }
    window.researchTech = function(key) { const t = state.technologies[key]; if (!t || t.researched) return; if (state
            .science >= t.cost * 0.5 && state.gold >= t.cost) { state.gold -= t.cost;
            t.researched = true;
            addJournalEntry(`Исследована: ${t.name}`); if (key === 'medicine') state.flags.plagueDealt = true; if (key ===
                'guilds') state.flags.guildBuilt = true;
            updateTech();
            updateUI(); } };

    // ===== РЕПУТАЦИЯ =====
    function updateReputation() { const el = document.getElementById('reputationList'); if (!el) return;
        el.innerHTML = Object.entries(state.reputation).map(([key, r]) => { let cls = 'rep-neutral'; if (r.value >= 70) cls =
                'rep-friendly'; else if (r.value <= 30) cls = 'rep-hostile'; return `<div class="panel-row"><span class="row-name">${r.name}</span><span class="row-value ${cls}">${'▮'.repeat(Math.floor(r.value/10))}${'▯'.repeat(10-Math.floor(r.value/10))} ${r.value}</span></div>`; })
            .join(''); }

    function changeReputation(faction, delta) { if (state.reputation[faction]) { state.reputation[faction].value = Math.min(
            100, Math.max(0, state.reputation[faction].value + delta));
        updateReputation(); } }

    // ===== КВЕСТЫ =====
    function startQuest(id) { if (!state.activeQuests.find(q => q.id === id)) state.activeQuests.push({ id, step: 0 }); }

    function advanceQuest(id) { const q = state.activeQuests.find(q => q.id === id); if (q) q.step++; }

    function completeQuest(id) { state.activeQuests = state.activeQuests.filter(q => q.id !== id);
        state.flags[id] = true;
        addJournalEntry(`Квест завершён: ${id}`); }

    function getCityPhase() { const p = state.population; if (p >= 5000) return '🏛️ Имперская столица'; if (p >= 1500) return '🏰 Крупный город'; if (
            p >= 500) return '🏙️ Город'; if (p >= 150) return '🏘️ Поселение'; if (p >= 50) return '🏡 Деревня'; return '🌱 Поселение'; }

    function getFullContext() { return { pop: state.population, gold: state.gold, happiness: state.happiness,
            houses: state.houses, food: state.food, science: state.science, turn: state.turn,
            season: state.seasonIndex, location: state.flags.location, hasWell: state.flags.wellBuilt,
            hasMarket: state.flags.marketBuilt, hasWalls: state.flags.wallsBuilt,
            hasTemple: state.flags.templeBuilt, hasBarracks: state.flags.barracksBuilt,
            hasLibrary: state.flags.libraryBuilt, hasPort: state.flags.portBuilt,
            hasAqueduct: state.flags.aqueductBuilt, hasGuild: state.flags.guildBuilt,
            hasArena: state.flags.arenaBuilt, tech: state.technologies, advisors: state.advisors,
            rep: state.reputation, flags: state.flags, isStarving: state.food < state.population * 1.5,
            isHungry: state.food < state.population * 3 && state.food >= state.population * 1.5,
            isUnhappy: state.happiness < 30, isSad: state.happiness < 55 && state.happiness >= 30,
            isOvercrowded: state.population > state.houses * 5,
            isTight: state.population > state.houses * 4 && state.population <= state.houses * 5,
            isBroke: state.gold < 5 && state.population > 30,
            isPoor: state.gold < 15 && state.population > 20,
            isRiverLocation: state.flags.location === 'river',
            isHillsLocation: state.flags.location === 'hills',
            isForestLocation: state.flags.location === 'forest',
            isWinter: state.seasonIndex === 3, isSummer: state.seasonIndex === 1,
            hasActiveBattle: !!state.battle, storyPhase: state.storyPhase,
            activeQuests: state.activeQuests, guildLevels: state.guilds,
            hasArtifact: (id) => state.artifacts.some(a => a.id === id),
            activeTradeRoutes: state.tradeRoutes.length, }; }

    function getContextHint() { if (state.storyPhase < 6) return ['📖 Глава I: Основание', '📖 Глава I: Первый кров',
            '📖 Глава I: Обустройство', '📖 Глава I: Выживание', '📖 Глава II: Новые люди',
            '📖 Глава II: Первая угроза'
        ][state.storyPhase] || ''; if (state.battle) return '⚔️ ИДЁТ БИТВА!'; if (state.activeQuests.length > 0)
            return '🎯 Квест: ' + state.activeQuests[0].id; const ctx = getFullContext(); if (ctx.isStarving)
            return '⚠️ Запасы еды на исходе!'; if (ctx.isUnhappy) return '⚠️ Жители на грани бунта!'; if (ctx
            .isOvercrowded) return '⚠️ Страшная перенаселённость!'; if (ctx.isBroke)
        return '⚠️ Казна пуста!'; if (ctx.isHungry) return '📋 Припасы тают.'; if (ctx.isSad)
            return '📋 Дух падает.'; return '🏙️ Город живёт своей жизнью.'; }

    function updateUI() {
        document.getElementById('population').textContent = state.population;
        document.getElementById('gold').textContent = state.gold;
        document.getElementById('happiness').textContent = state.happiness;
        document.getElementById('houses').textContent = state.houses;
        document.getElementById('food').textContent = state.food;
        document.getElementById('science').textContent = state.science;
        const fe = document.getElementById('food'),
            he = document.getElementById('happiness'),
            hoe = document.getElementById('houses'),
            ge = document.getElementById('gold');
        [fe, he, hoe, ge].forEach(el => el.classList.remove('stat-danger', 'stat-warning')); if (state.food < state
            .population * 1.5) fe.classList.add('stat-danger'); else if (state.food < state.population * 3) fe.classList
            .add('stat-warning'); if (state.happiness < 30) he.classList.add('stat-danger'); else if (state.happiness <
            55) he.classList.add('stat-warning'); if (state.population > state.houses * 5) hoe.classList.add(
            'stat-danger'); else if (state.population > state.houses * 4) hoe.classList.add('stat-warning'); if (state
            .gold < 5) ge.classList.add('stat-danger'); else if (state.gold < 15) ge.classList.add('stat-warning');
        document.getElementById('turnDisplay').textContent = `Год ${state.turn}, ${seasons[state.seasonIndex]}`;
        document.getElementById('cityPhase').textContent = getCityPhase();
        const hint = document.getElementById('contextHint');
        hint.textContent = getContextHint();
        hint.className = 'context-hint'; if (state.storyPhase < 6) hint.classList.add('hint-story'); else if (state
            .battle) hint.classList.add('hint-critical'); else if (state.activeQuests.length > 0) hint.classList.add(
            'hint-important');
        else if (getFullContext().isStarving || getFullContext().isUnhappy || getFullContext().isOvercrowded || getFullContext()
            .isBroke) hint.classList.add('hint-critical');
        else hint.classList.add('hint-normal');
        document.getElementById('progressFill').style.width = Math.min(100, Math.floor((state.storyPhase / 6) * 100)) +
        '%';
        const cd = Object.entries(state.cooldowns).filter(([_, c]) => c > 0);
        document.getElementById('cooldownInfo').textContent = cd.length ? '⏳ Кулдаун: ' + cd.map(([id, c]) =>
            `${id}(${c})`).join(' · ') : '';
        renderCityMap();
        updateArtifacts();
        updateTradeRoutes();
        updateGuilds();
        updateAdvisors();
        updateTech();
        updateReputation();
        updateJournal();
    }

    function clamp() { state.population = Math.max(0, state.population);
        state.gold = Math.max(0, state.gold);
        state.happiness = Math.min(100, Math.max(0, state.happiness));
        state.houses = Math.max(0, state.houses);
        state.food = Math.max(0, state.food);
        state.science = Math.max(0, state.science); }

    function checkGameOver() { if (state.population <= 0) { state.gameOver = true;
            state.gameOverMessage = '💀 Город опустел.'; } else if (state.happiness <= 0 && state.population > 15) { state
            .gameOver = true;
            state.gameOverMessage = '🔥 Восстание!'; } else if (state.food <= 0 && state.population > 10) { const l = Math
            .floor(state.population * 0.5);
            state.population -= l;
            state.happiness -= 30;
            state.food = 2;
            alert(`☠️ Голод! ${l} погибло.`); if (state.population <= 2) { state.gameOver = true;
                state.gameOverMessage = '🪦 Вымерли.'; } }
        clamp(); if (state.population > state.houses * 6) state.happiness -= 2; }

    function setCd(id) { state.cooldowns[id] = CD_BASE + Math.floor(Math.random() * (CD_VAR + 1)); }

    function reduceCd() { Object.keys(state.cooldowns).forEach(id => { if (state.cooldowns[id] > 0) state.cooldowns[id]--; if (
            state.cooldowns[id] <= 0) delete state.cooldowns[id]; }); }

    function onCd(id) { return state.cooldowns[id] && state.cooldowns[id] > 0; }

    // ===== СТАРТОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ =====
    function getStoryEvent() { const loc = state.flags.location; const phase = state.storyPhase; if (phase === 0)
            return { id: 'story_location', title: 'Выбор места', icon: '🗺️',
                desc: 'Отряд из 12 человек добрался до долины. Где разбить лагерь?\n\n🌲 Река — плодородно.\n⛰️ Холмы — безопасно.\n🌳 Лес — дичь.',
                choices: [{ text: '🌲 Река', hint: '🌾+12|🏠+1', action: () => { state.food += 12;
                        state.houses += 1;
                        state.flags.location = 'river'; } }, { text: '⛰️ Холмы', hint: '💰+4|😊+5',
                        action: () => { state.gold += 4;
                            state.happiness += 5;
                            state.flags.location = 'hills'; } }, { text: '🌳 Лес', hint: '🌾+20',
                        action: () => { state.food += 20;
                            state.flags.location = 'forest'; } }] }; if (phase === 1) return {
                id: 'story_shelter', title: 'Первое укрытие', icon: '🛖',
                desc: 'Нужно строить жильё.',
                choices: [{ text: 'Общий дом', hint: '🏠+3|😊+8', action: () => { state.houses += 3;
                        state.happiness += 8; } }, { text: 'Хижины', hint: '🏠+5|💰-3', action: () => {
                        state.houses += 5;
                        state.gold -= 3; }, cond: () => state.gold >= 3 }] }; if (phase === 2) { if (loc ===
                    'river') return { id: 'story_water', title: 'Берег', icon: '🌊',
                    desc: 'Вода рядом! Нужны мостки.',
                    choices: [{ text: 'Мостки', hint: '💰-3|😊+12', action: () => { state.gold -= 3;
                            state.happiness += 12;
                            state.flags.wellBuilt = true; }, cond: () => state.gold >= 3 }, { text: 'Выше',
                            hint: '🏠-1', action: () => { state.houses -= 1;
                            state.flags.wellBuilt = true; } }] }; if (loc === 'hills') return {
                    id: 'story_water', title: 'Колодец', icon: '🪣', desc: 'Воды нет. Нужен колодец.',
                    choices: [{ text: 'Рыть', hint: '💰-5|😊+15', action: () => { state.gold -= 5;
                            state.happiness += 15;
                            state.flags.wellBuilt = true; }, cond: () => state.gold >= 5 }, { text: 'Родник',
                            hint: '😊+5', action: () => { state.happiness += 5;
                            state.flags.wellBuilt = true; } }] }; if (loc === 'forest') return {
                    id: 'story_water', title: 'Ручей', icon: '💧', desc: 'Ручей рядом. Расчистить.',
                    choices: [{ text: 'Расчистить', hint: '😊+10', action: () => { state.happiness += 10;
                            state.flags.wellBuilt = true; } }, { text: 'Мостки', hint: '💰-3|😊+15',
                            action: () => { state.gold -= 3;
                                state.happiness += 15;
                                state.flags.wellBuilt = true; }, cond: () => state.gold >= 3 }] }; } if (phase ===
                3) { if (loc === 'river') return { id: 'story_food', title: 'Рыбалка', icon: '🎣',
                    desc: 'Река полна рыбы.',
                    choices: [{ text: 'Сети', hint: '🌾+20', action: () => { state.food += 20;
                            state.flags.firstHunt = true; } }, { text: 'Лодки', hint: '🌾+14', action: () => {
                            state.food += 14;
                            state.flags.firstHunt = true; } }] }; if (loc === 'hills') return {
                    id: 'story_food', title: 'Охота', icon: '🏹', desc: 'В холмах козы.',
                    choices: [{ text: 'Облава', hint: '🌾+18-25', action: () => { state.food += 18 + Math.floor(
                                Math.random() * 8);
                            state.flags.firstHunt = true; } }, { text: 'Группы', hint: '🌾+10',
                            action: () => { state.food += 10;
                                state.flags.firstHunt = true; } }] }; if (loc === 'forest') return {
                    id: 'story_food', title: 'Лес', icon: '🌲', desc: 'Лес богат.',
                    choices: [{ text: 'Охота', hint: '🌾+20-28', action: () => { state.food += 20 + Math.floor(
                                Math.random() * 9);
                            state.flags.firstHunt = true; } }, { text: 'Сбор', hint: '🌾+15',
                            action: () => { state.food += 15;
                                state.flags.firstHunt = true; } }] }; } if (phase === 4) return {
                id: 'story_neighbors', title: 'Гости', icon: '🧔', desc: 'Семья просит приюта.',
                choices: [{ text: 'Принять', hint: '👥+3|😊+8', action: () => { state.population += 3;
                        state.happiness += 8; } }, { text: 'Прогнать', hint: '😊-3', action: () => { state
                        .happiness -= 3; } }] }; if (phase === 5) { if (loc === 'river') return {
                    id: 'story_threat', title: 'Паводок', icon: '🌊', desc: 'Река поднимается.',
                    choices: [{ text: 'Укрепить', hint: '💰-15', action: () => { state.gold -= 15;
                            state.flags.wallsBuilt = true; }, cond: () => state.gold >= 15 }, { text: 'Перенести',
                            hint: '🏠-2', action: () => { state.houses -= 2;
                            state.flags.wallsBuilt = true; } }] }; if (loc === 'hills') return {
                    id: 'story_threat', title: 'Оползень', icon: '⛰️', desc: 'Склон пополз.',
                    choices: [{ text: 'Укрепить', hint: '💰-15', action: () => { state.gold -= 15;
                            state.flags.wallsBuilt = true; }, cond: () => state.gold >= 15 }, { text: 'Перенести',
                            hint: '🏠-1', action: () => { state.houses -= 1;
                            state.flags.wallsBuilt = true; } }] }; if (loc === 'forest') return {
                    id: 'story_threat', title: 'Волки', icon: '🐺', desc: 'Волки утащили овец.',
                    choices: [{ text: 'Частокол', hint: '💰-15', action: () => { state.gold -= 15;
                            state.flags.wallsBuilt = true; }, cond: () => state.gold >= 15 }, { text: 'Дозор',
                            hint: '😊+3', action: () => { state.happiness += 3;
                            state.flags.wallsBuilt = true; } }] }; } return null; }

    // ===== БАЗА СОБЫТИЙ =====
    function getFreePlayEvents() {
        return [
            // КРИЗИСЫ
            { id: 'food_crisis', u: false, title: 'Нехватка еды', icon: '🌾', desc: 'Припасы на исходе.',
                cond: () => { const c = getFullContext(); return c.isStarving && c.storyPhase >= 6; }, prio: 95,
                choices: [{ text: 'Охота', hint: '🌾+20-30', action: () => { state.food += 20 + Math.floor(Math.random() *
                            11); if (Math.random() < 0.15) state.population -= 1; } }, { text: 'Купить',
                        hint: '💰-20|🌾+35', action: () => { state.gold -= 20;
                            state.food += 35; }, cond: () => state.gold >= 20 }] },
            { id: 'overcrowding', u: false, title: 'Перенаселение', icon: '🏚️', desc: 'Людям негде жить.',
                cond: () => { const c = getFullContext(); return c.isOvercrowded && c.storyPhase >= 6; }, prio: 92,
                choices: [{ text: 'Бараки', hint: '💰-20|🏠+6', action: () => { state.gold -= 20;
                        state.houses += 6; }, cond: () => state.gold >= 20 }, { text: 'Землянки', hint: '🏠+4|😊-5',
                        action: () => { state.houses += 4;
                            state.happiness -= 5; } }] },
            // БЫТ
            { id: 'hunting', u: false, title: 'Охота', icon: '🏹', desc: 'Добыть дичи.',
                cond: () => { const c = getFullContext(); return c.isHungry && c.storyPhase >= 6; }, prio: 35,
                choices: [{ text: 'Отправить', hint: '🌾+12-22', action: () => { state.food += 12 + Math.floor(Math.random() *
                        11); if (Math.random() < 0.1) state.population -= 1; } }] },
            // АРТЕФАКТЫ
            { id: 'find_sword', u: true, flag: 'artifactSword', title: 'Древний меч', icon: '🗡️',
                desc: 'В земле нашли сияющий меч!',
                cond: () => { const c = getFullContext(); return !c.flags.artifactSword && c.storyPhase >= 6 && c.pop >=
                        80; }, prio: 55,
                choices: [{ text: 'Взять меч', hint: '💎 Артефакт!', action: () => { addArtifact({ id: 'sword_of_valor',
                            name: 'Меч доблести', icon: '🗡️', bonus: '⚔️ +20 к битвам', desc: 'Древний меч героя' });
                        state.flags.artifactSword = true; } }, { text: 'Оставить', action: () => { state.flags
                        .artifactSword = true; } }] },
            { id: 'find_crown', u: true, flag: 'artifactCrown', title: 'Корона мудрости', icon: '👑',
                desc: 'В руинах нашли золотую корону.',
                cond: () => { const c = getFullContext(); return !c.flags.artifactCrown && c.storyPhase >= 6 && c.pop >=
                        200 && c.hasLibrary; }, prio: 50,
                choices: [{ text: 'Надеть корону', hint: '💎 +20 науки', action: () => { addArtifact({ id: 'crown_of_wisdom',
                            name: 'Корона мудрости', icon: '👑', bonus: '🔬 +20 науки', desc: 'Корона древних королей' });
                        state.flags.artifactCrown = true; } }] },
            // ТОРГОВЛЯ
            { id: 'trade_offer', u: false, title: 'Выгодная сделка', icon: '🤝', desc: 'Купец предлагает особый маршрут.',
                cond: () => { const c = getFullContext(); return c.hasMarket && c.storyPhase >= 6 && c.gold >= 25; },
                prio: 30,
                choices: [{ text: 'Отправить караван', hint: '💰-25|Прибыль', action: () => { startTradeRoute(
                        'Южная империя', 'Специи', 25, 55, 0.25, 3);
                    updateTradeRoutes(); } }] },
            // ГИЛЬДИИ
            { id: 'guild_request', u: false, title: 'Запрос гильдии', icon: '🏛️', desc: 'Гильдия купцов просит поддержки.',
                cond: () => { const c = getFullContext(); return c.guildLevels.merchants.level === 0 && c.storyPhase >=
                        6 && c.gold >= 40; }, prio: 32,
                choices: [{ text: 'Поддержать', hint: 'Основать гильдию', action: () => { upgradeGuild('merchants');
                        updateGuilds(); } }] },
            // БИТВЫ
            { id: 'bandit_raid', u: false, title: 'Нападение бандитов!', icon: '⚔️', desc: 'Банда разбойников у ворот!',
                cond: () => { const c = getFullContext(); return !c.hasActiveBattle && c.storyPhase >= 6 && c.pop >= 60 &&
                        Math.random() < 0.3; }, prio: 80,
                choices: [{ text: 'В бой!', hint: 'Начать битву', action: () => { startBattle('Банда разбойников',
                        25); } }, { text: 'Откупиться', hint: '💰-20', action: () => { state.gold -= 20;
                        state.happiness -= 5; }, cond: () => state.gold >= 20 }] },
            // FALLBACK
            { id: 'quiet_build', u: false, title: 'Застройка', icon: '🔨', desc: 'Расширить город.',
                cond: () => { const c = getFullContext(); return c.storyPhase >= 6 && c.gold >= 6; }, prio: 3,
                choices: [{ text: 'Строить', hint: '💰-6|🏠+2', action: () => { state.gold -= 6;
                        state.houses += 2; } }] },
            { id: 'quiet_rest', u: false, title: 'Передышка', icon: '😌', desc: 'Всё спокойно.',
                cond: () => { const c = getFullContext(); return c.storyPhase >= 6; }, prio: 3,
                choices: [{ text: 'Отдых', hint: '😊+8', action: () => { state.happiness += 8; } }] },
        ];
    }

    // ===== ВЫБОР СОБЫТИЯ =====
    function getNextEvent() {
        if (state.battle) { const be = getBattleEvent(); if (be) return be; }
        if (state.storyPhase < 6) { const se = getStoryEvent(); if (se) return se; }
        const all = getFreePlayEvents();
        const ctx = getFullContext();
        let avail = all.filter(e => { if (!e.condition || !e.condition()) return false; if (e.id === state.lastEventId)
                return false; if (!e.u && onCd(e.id)) return false; if (e.u && e.flag && state.flags[e.flag])
                return false; return true; });
        if (avail.length <= 3) { const sorted = Object.entries(state.cooldowns).filter(([_, cd]) => cd > 0).sort((a,
                b) => b[1] - a[1]); for (let i = 0; i < Math.ceil(sorted.length / 2); i++) delete state.cooldowns[
                sorted[i][0]];
            avail = all.filter(e => { if (!e.condition || !e.condition()) return false; if (e.id === state
                    .lastEventId) return false; if (!e.u && onCd(e.id)) return false; if (e.u && e.flag && state
                    .flags[e.flag]) return false; return true; }); } if (avail.length <= 1) { state.lastEventId =
                null;
            avail = all.filter(e => { if (!e.condition || !e.condition()) return false; if (!e.u && onCd(e.id))
                    return false; if (e.u && e.flag && state.flags[e.flag]) return false; return true; }); } if (avail
            .length === 0) { state.lastEventId = null;
            state.cooldowns = {};
            avail = all.filter(e => (!e.condition || e.condition()) && !(e.u && e.flag && state.flags[e.flag])); }
        const scored = avail.map(e => { let s = e.prio || 0; if (e.id === 'food_crisis' && ctx.isStarving) s +=
                150; if (e.id === 'overcrowding' && ctx.isOvercrowded) s += 150; if (e.id === 'bandit_raid' && !ctx
                .hasActiveBattle) s += 100;
            s += Math.random() * 15; return { event: e, score: s }; });
        scored.sort((a, b) => b.score - a.score);
        const ch = scored[Math.floor(Math.random() * Math.min(4, scored.length))].event;
        state.lastEventId = ch.id; if (!ch.u) setCd(ch.id); return ch;
    }

    // ===== РЕНДЕР =====
    function renderEvent(event) { const area = document.getElementById('eventCardArea');
        let urgClass = 'urgency-story',
            urgText = ''; if (state.storyPhase < 6) urgText = `📖 Глава ${state.storyPhase<4?'I':'II'} · ${state.storyPhase+1}/6`; else if (
            state.battle) { urgClass = 'urgency-battle';
            urgText = '⚔️ БИТВА!'; } else if (['food_crisis', 'overcrowding'].includes(event.id)) { urgClass =
                'urgency-critical';
            urgText = '⚠️ КРИЗИС'; } else if (event.id.startsWith('find_')) { urgClass = 'urgency-quest';
            urgText = '💎 АРТЕФАКТ'; }
        let html = '';
        event.choices.forEach((ch, i) => { let l = ch.cond && !ch.cond();
            html +=
            `<button class="choice-btn${l?' locked':''}" data-idx="${i}" ${l?'disabled':''}>${ch.text}<span class="hint">${ch.hint||''}${l?' (недоступно)':''}</span></button>`; });
        area.innerHTML =
            `<div class="event-card">${urgText?`<div class="event-urgency ${urgClass}">${urgText}</div>`:''}<span class="event-icon">${event.icon}</span><div class="event-title">${event.title}</div><div class="event-description">${event.desc||event.description}</div><div class="choices-container">${html}</div></div>`;
        area.querySelectorAll('.choice-btn:not(.locked)').forEach(btn => { btn.addEventListener('click', function() { const idx =
                    parseInt(this.getAttribute('data-idx')),
                choice = event.choices[idx];
            choice.action(); if (event.u && event.flag) state.flags[event.flag] = true;
            addJournalEntry(`${event.title}: ${choice.text}`); if (state.storyPhase < 6 && event.id.startsWith(
                'story_')) state.storyPhase++;
            advanceTurn(); }); }); }

    function advanceTurn() { state.seasonIndex++; if (state.seasonIndex >= 4) { state.seasonIndex = 0;
            state.turn++; }
        state.globalStep++;
        reduceCd(); if (Object.keys(state.cooldowns).length > 8) Object.keys(state.cooldowns).forEach(id => { if (state
                .cooldowns[id] > 0) state.cooldowns[id]--; if (state.cooldowns[id] <= 0) delete state.cooldowns[
            id]; });
        processTradeRoutes();
        state.food -= Math.floor(state.population / 12) + 1;
        state.gold += Math.floor(state.population / 40);
        state.science += Math.floor(state.population / 80) + 1; if (state.flags.marketBuilt) state.gold += 6; if (state
            .flags.templeBuilt) state.happiness += 2; if (state.advisors.treasurer.hired) state.gold += 3; if (state
            .advisors.priest.hired) state.happiness += 2; if (state.advisors.scholar.hired) state.science += 2; if (state
            .guilds.mages.level > 0) state.science += state.guilds.mages.level * 3; if (state.guilds.merchants.level >
            0) state.gold += state.guilds.merchants.level * 5; if (state.technologies.irrigation && state.technologies
            .irrigation.researched) state.food += 10;
        clamp();
        checkGameOver();
        updateUI(); if (state.gameOver) { document.getElementById('eventCardArea').innerHTML =
                `<div class="game-over-overlay"><h2>⚰️ Конец истории</h2><p>${state.gameOverMessage}</p><p>Город: ${getCityPhase()}</p><p>Лет: ${state.turn}</p><button class="restart-btn" onclick="location.reload()">🔄 Заново</button></div>`; } else { renderEvent(
                getNextEvent()); } }

    function start() { state.population = 12;
        state.gold = 8;
        state.happiness = 60;
        state.houses = 3;
        state.food = 25;
        state.science = 0;
        state.turn = 1;
        state.seasonIndex = 0;
        state.gameOver = false;
        state.chainContext = null;
        state.history = [];
        state.lastEventId = null;
        state.cooldowns = {};
        state.globalStep = 0;
        state.storyPhase = 0;
        state.artifacts = [];
        state.tradeRoutes = [];
        state.battle = null;
        state.activeQuests = [];
        state.eventUsage = {};
        state.lastCategory = '';
        state.guilds = { merchants: { name: 'Гильдия купцов', level: 0, bonus: '💰 Торговля +5', cost: 40 },
            warriors: { name: 'Гильдия воинов', level: 0, bonus: '⚔️ Защита +10%', cost: 50 }, thieves: { name: 'Гильдия теней',
                level: 0, bonus: '🕵️ Информация', cost: 45 }, mages: { name: 'Гильдия магов', level: 0,
                bonus: '🔮 Наука +3', cost: 60 }, artisans: { name: 'Гильдия ремесленников', level: 0,
                bonus: '🏠 Стройка дешевле', cost: 35 } };
        allFlags.forEach(f => state.flags[f] = false);
        state.flags.location = null;
        state.advisors = { general: { name: 'Воевода', loyalty: 70, bonus: '🛡️ Защита', hired: true },
            treasurer: { name: 'Казначей', loyalty: 75, bonus: '💰 Доход', hired: false }, priest: { name: 'Жрец',
                loyalty: 80, bonus: '😊 Счастье', hired: false }, scholar: { name: 'Учёный', loyalty: 65,
                bonus: '🔬 Наука', hired: false }, spy: { name: 'Шпион', loyalty: 50, bonus: '🕵️ Инфо',
            hired: false } };
        state.technologies = { irrigation: { name: 'Орошение', cost: 30, researched: false }, medicine: { name: 'Медицина',
                cost: 40, researched: false }, masonry: { name: 'Каменная кладка', cost: 35,
            researched: false }, engineering: { name: 'Инженерия', cost: 60, researched: false },
            cartography: { name: 'Картография', cost: 45, researched: false }, guilds: { name: 'Гильдии', cost: 50,
                researched: false }, navigation: { name: 'Навигация', cost: 70, researched: false },
            alchemy: { name: 'Алхимия', cost: 80, researched: false } };
        state.reputation = { northKingdom: { name: 'Север', value: 50 }, southEmpire: { name: 'Юг', value: 40 },
            merchantGuild: { name: 'Купцы', value: 60 }, hillTribes: { name: 'Горцы', value: 30 } };
        clamp();
        updateUI();
        renderEvent(getNextEvent()); }
    document.getElementById('restartButton').addEventListener('click', () => { if (confirm('Начать заново?')) start(); });
    start();
})();
</script>
</body>
</html>
