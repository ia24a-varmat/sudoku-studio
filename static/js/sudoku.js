"use strict";

// ======================================================
// ELEMENTE
// ======================================================

const grid = document.querySelector("#sudoku");

const original = JSON.parse(grid.dataset.original);
const puzzleId = grid.dataset.puzzleId;

const fields = [...grid.querySelectorAll("input")];

const feedback = document.querySelector("#feedback");
const timerLabel = document.querySelector("#timer");

const nameGate = document.querySelector("#nameGate");
const gameArea = document.querySelector("#gameArea");

const checkButton = document.querySelector("#check");
const saveButton = document.querySelector("#submit");
const resetButton = document.querySelector("#reset");
const continueButton = document.querySelector("#continue");
const hintButton = document.querySelector("#hint");
const eraseButton = document.querySelector("#erase");

const digitButtons = [
    ...document.querySelectorAll(".digit-button")
];


// ======================================================
// SPIELSTATUS
// ======================================================

let player = "";

let selectedIndex = null;

let mistakes = 0;
let hints = 0;

let submitted = false;
let solved = false;
let busy = false;

let elapsedMs = 0;
let runningSince = null;

let lastWrongBoard = null;


// ======================================================
// TIMER
// ======================================================

function secondsPlayed() {

    const current = runningSince === null
        ? 0
        : performance.now() - runningSince;

    return Math.floor((elapsedMs + current) / 1000);
}


function renderTimer() {

    const total = secondsPlayed();

    const minutes = String(
        Math.floor(total / 60)
    ).padStart(2, "0");

    const seconds = String(
        total % 60
    ).padStart(2, "0");

    timerLabel.textContent = `${minutes}:${seconds}`;
}


function pauseTimer() {

    if (runningSince !== null) {

        elapsedMs += performance.now() - runningSince;

        runningSince = null;
    }

    renderTimer();
}


function startTimer() {

    if (
        runningSince === null &&
        player &&
        !submitted &&
        !solved
    ) {
        runningSince = performance.now();
    }

    renderTimer();
}


// ======================================================
// SUDOKU-DATEN
// ======================================================

function boardData() {

    return Array.from(
        { length: 9 },

        (_, row) => Array.from(
            { length: 9 },

            (_, col) => {

                const index = row * 9 + col;

                return Number(fields[index].value) || 0;
            }
        )
    );
}


// ======================================================
// MELDUNGEN
// ======================================================

function message(text, type = "info") {

    feedback.textContent = text;

    feedback.className = `game-feedback ${type}`;
}


// ======================================================
// ZAHLEN ZÄHLEN
// ======================================================

function updateCounters() {

    const counts = Array(10).fill(0);

    fields.forEach(field => {

        const number = Number(field.value);

        if (number >= 1 && number <= 9) {
            counts[number]++;
        }
    });


    digitButtons.forEach(button => {

        const number = Number(button.dataset.digit);

        const remaining = Math.max(
            0,
            9 - counts[number]
        );

        document.querySelector(
            `#remaining-${number}`
        ).textContent = `${remaining} übrig`;

        button.setAttribute(
            "aria-label",
            `Zahl ${number}, ${remaining} übrig`
        );

        button.classList.toggle(
            "complete-digit",
            remaining === 0
        );
    });


    document.querySelector(
        "#mistakeCount"
    ).textContent = String(mistakes);

    document.querySelector(
        "#hintCount"
    ).textContent = String(hints);
}


// ======================================================
// DOPPELTE ZAHLEN ERKENNEN
// ======================================================

function findConflicts() {

    const board = boardData();

    const conflicts = new Set();


    function inspect(indices) {

        const locations = new Map();

        indices.forEach(index => {

            const row = Math.floor(index / 9);
            const col = index % 9;

            const value = board[row][col];

            if (value === 0) {
                return;
            }

            if (locations.has(value)) {

                conflicts.add(index);
                conflicts.add(locations.get(value));

            } else {

                locations.set(value, index);
            }

        });
    }


    // Zeilen und Spalten
    for (let n = 0; n < 9; n++) {

        inspect(
            Array.from(
                { length: 9 },
                (_, col) => n * 9 + col
            )
        );

        inspect(
            Array.from(
                { length: 9 },
                (_, row) => row * 9 + n
            )
        );
    }


    // 3x3-Blöcke
    for (let boxRow = 0; boxRow < 3; boxRow++) {

        for (let boxCol = 0; boxCol < 3; boxCol++) {

            const indices = [];

            for (let r = 0; r < 3; r++) {

                for (let c = 0; c < 3; c++) {

                    indices.push(
                        (boxRow * 3 + r) * 9 +
                        boxCol * 3 + c
                    );
                }
            }

            inspect(indices);
        }
    }

    return conflicts;
}


// ======================================================
// FELDER HERVORHEBEN
// ======================================================

function updateHighlights() {

    const selected = selectedIndex === null
        ? null
        : fields[selectedIndex];

    const row = selected === null
        ? -1
        : Number(selected.dataset.row);

    const col = selected === null
        ? -1
        : Number(selected.dataset.col);

    const value = selected === null
        ? ""
        : selected.value;

    const conflicts = findConflicts();


    fields.forEach((field, index) => {

        const r = Number(field.dataset.row);
        const c = Number(field.dataset.col);

        const peer =
            r === row ||
            c === col ||
            (
                Math.floor(r / 3) === Math.floor(row / 3) &&
                Math.floor(c / 3) === Math.floor(col / 3)
            );


        field.classList.toggle(
            "peer",
            selected !== null && peer
        );

        field.classList.toggle(
            "same-number",
            !!value && field.value === value
        );

        field.classList.toggle(
            "selected",
            index === selectedIndex
        );

        field.classList.toggle(
            "conflict",
            conflicts.has(index)
        );
    });


    digitButtons.forEach(button => {

        button.classList.toggle(
            "active-digit",
            !!value && button.dataset.digit === value
        );
    });
}


function selectCell(index) {

    selectedIndex = index;

    updateHighlights();
}


// ======================================================
// ZAHLEN EINGEBEN
// ======================================================

function isEditable(index = selectedIndex) {

    return (
        player &&
        !busy &&
        !submitted &&
        !solved &&
        runningSince !== null &&
        index !== null &&
        !fields[index].classList.contains("fixed")
    );
}


function updateBoard() {

    lastWrongBoard = null;

    updateCounters();
    updateHighlights();

    message("Eingabe aktualisiert. Du kannst weiter spielen.");
}


function enterDigit(digit) {

    if (!isEditable()) {

        message(
            "Wähle ein freies Feld. Falls du pausiert hast, klicke auf Weiter spielen."
        );

        return;
    }

    fields[selectedIndex].value =
        digit === null ? "" : String(digit);

    updateBoard();

    fields[selectedIndex].focus();
}


// ======================================================
// SPIELFELD SPERREN / FREIGEBEN
// ======================================================

function lockBoard(locked) {

    fields.forEach(field => {

        if (!field.classList.contains("fixed")) {
            field.readOnly = locked;
        }
    });


    digitButtons.forEach(button => {
        button.disabled = locked;
    });

    eraseButton.disabled = locked;
    hintButton.disabled = locked || busy;

    grid.classList.toggle("board-paused", locked);
}


function refreshControls() {

    const paused = runningSince === null;

    lockBoard(
        paused || busy || solved || submitted
    );

    checkButton.disabled =
        !player || busy || submitted || solved;

    saveButton.disabled =
        !player || busy || submitted;

    resetButton.disabled =
        !player || busy || submitted;

    continueButton.hidden =
        !player || submitted || solved || !paused;

    continueButton.disabled = busy;
}


// ======================================================
// FLASK API
// ======================================================

async function postJson(url, body) {

    const response = await fetch(url, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)
    });

    const data = await response.json();

    return {
        ok: response.ok,
        data
    };
}


// ======================================================
// ANIMATION: FALSCH
// ======================================================

function burstWrong() {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }

    grid.classList.remove("board-shake");

    void grid.offsetWidth;

    grid.classList.add("board-shake");

    setTimeout(() => {
        grid.classList.remove("board-shake");
    }, 500);


    const burst = document.createElement("div");

    burst.className = "wrong-burst";
    burst.textContent = "💥";

    document.body.appendChild(burst);

    setTimeout(() => burst.remove(), 1100);
}


// ======================================================
// ANIMATION: KONFETTI
// ======================================================

function celebrate() {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }

    const layer = document.querySelector(
        "#celebrationLayer"
    );

    const colors = [
        "#7c65ff",
        "#ffbb55",
        "#ff7697",
        "#49bfac",
        "#79bfff"
    ];


    for (let i = 0; i < 65; i++) {

        const piece = document.createElement("span");

        piece.className = "confetti-piece";

        piece.style.left =
            `${Math.random() * 100}%`;

        piece.style.backgroundColor =
            colors[i % colors.length];

        piece.style.animationDelay =
            `${Math.random() * 0.45}s`;

        piece.style.animationDuration =
            `${2 + Math.random() * 1.1}s`;

        layer.appendChild(piece);

        setTimeout(() => piece.remove(), 4000);
    }
}


// ======================================================
// EINGABE MIT TASTATUR
// ======================================================

fields.forEach((field, index) => {

    field.addEventListener("focus", () => {
        selectCell(index);
    });

    field.addEventListener("click", () => {
        selectCell(index);
    });


    field.addEventListener("input", () => {

        if (!isEditable(index)) {
            return;
        }

        field.value = field.value
            .replace(/[^1-9]/g, "")
            .slice(-1);

        updateBoard();
    });


    field.addEventListener("keydown", event => {

        const moves = {
            ArrowLeft: -1,
            ArrowRight: 1,
            ArrowUp: -9,
            ArrowDown: 9
        };


        if (event.key in moves) {

            event.preventDefault();

            const next = Math.max(
                0,
                Math.min(
                    80,
                    index + moves[event.key]
                )
            );

            fields[next].focus();

        } else if (
            (
                event.key === "Backspace" ||
                event.key === "Delete"
            ) &&
            isEditable(index)
        ) {

            event.preventDefault();

            enterDigit(null);
        }
    });
});


// ======================================================
// ZAHLENBUTTONS
// ======================================================

digitButtons.forEach(button => {

    button.addEventListener("click", () => {

        enterDigit(
            Number(button.dataset.digit)
        );
    });
});


eraseButton.addEventListener("click", () => {
    enterDigit(null);
});


// ======================================================
// NAME VOR SPIELBEGINN
// ======================================================

document.querySelector("#nameForm").addEventListener(
    "submit",
    event => {

        event.preventDefault();

        const proposed = document.querySelector(
            "#playerInput"
        ).value.trim().replace(/\s+/g, " ");


        if (!proposed || proposed.length > 30) {

            document.querySelector(
                "#nameError"
            ).textContent =
                "Bitte gib einen Namen mit maximal 30 Zeichen ein.";

            return;
        }


        player = proposed;

        document.querySelector(
            "#playerDisplay"
        ).textContent = player;


        nameGate.hidden = true;

        gameArea.removeAttribute("inert");

        startTimer();

        refreshControls();


        const firstEmpty = fields.find(
            field => !field.classList.contains("fixed")
        );

        if (firstEmpty) {
            firstEmpty.focus();
        }
    }
);


// ======================================================
// SUDOKU PRÜFEN
// ======================================================

checkButton.addEventListener("click", async () => {

    if (!player || busy || submitted || solved) {
        return;
    }

    // Timer sofort stoppen
    pauseTimer();

    busy = true;
    refreshControls();


    try {

        const result = await postJson(
            `/api/check/${encodeURIComponent(puzzleId)}`,
            {
                board: boardData()
            }
        );


        if (!result.ok || !result.data.valid) {

            const signature = JSON.stringify(boardData());

            if (
                result.ok &&
                signature !== lastWrongBoard
            ) {

                mistakes++;
                lastWrongBoard = signature;
            }

            updateCounters();

            message(
                `💥 ${result.data.message || "Da stimmt etwas nicht."}`,
                "error"
            );

            burstWrong();

        } else if (result.data.complete) {

            solved = true;

            message(
                "🎉 Juhu! Dein Sudoku ist vollständig und korrekt. Speichere jetzt dein Ergebnis!",
                "success"
            );

            celebrate();

        } else {

            message(
                "✨ Bisher keine Regel verletzt! Der Timer ist pausiert. Klicke auf Weiter spielen.",
                "success"
            );
        }

    } catch (error) {

        message(
            "Verbindung fehlgeschlagen. Der Timer bleibt pausiert.",
            "error"
        );

    } finally {

        busy = false;

        refreshControls();
    }
});


// ======================================================
// WEITER SPIELEN
// ======================================================

continueButton.addEventListener("click", () => {

    if (busy || solved || submitted) {
        return;
    }

    startTimer();

    message("Viel Erfolg! Der Timer läuft wieder.");

    refreshControls();
});


// ======================================================
// ERGEBNIS SPEICHERN
// ======================================================

saveButton.addEventListener("click", async () => {

    if (!player || busy || submitted) {
        return;
    }

    // Timer sofort stoppen
    pauseTimer();

    busy = true;
    refreshControls();


    try {

        const result = await postJson(
            `/api/submit/${encodeURIComponent(puzzleId)}`,
            {
                board: boardData(),

                player: player,

                seconds: Math.min(
                    secondsPlayed(),
                    86400
                ),

                mistakes: mistakes
            }
        );


        if (result.ok && result.data.saved) {

            submitted = true;
            solved = true;

            message(
                `🏆 Super gemacht, ${player}! Dein Ergebnis wurde gespeichert.`,
                "success"
            );

            celebrate();

        } else {

            const signature = JSON.stringify(boardData());

            if (signature !== lastWrongBoard) {
                mistakes++;
                lastWrongBoard = signature;
            }

            updateCounters();

            message(
                `💥 ${result.data.error || "Das Ergebnis konnte nicht gespeichert werden."}`,
                "error"
            );

            burstWrong();
        }

    } catch (error) {

        message(
            "Verbindung fehlgeschlagen. Dein Ergebnis wurde nicht gespeichert.",
            "error"
        );

    } finally {

        busy = false;

        refreshControls();
    }
});


// ======================================================
// SPIEL NEU STARTEN
// ======================================================

resetButton.addEventListener("click", () => {

    if (!player || busy || submitted) {
        return;
    }

    const confirmed = window.confirm(
        "Sudoku wirklich neu starten? Alle Eingaben und die Zeit werden zurückgesetzt."
    );

    if (!confirmed) {
        return;
    }


    fields.forEach((field, index) => {

        const row = Math.floor(index / 9);
        const col = index % 9;

        field.value = original[row][col] || "";
    });


    mistakes = 0;
    hints = 0;

    lastWrongBoard = null;

    solved = false;

    elapsedMs = 0;
    runningSince = performance.now();


    updateCounters();
    updateHighlights();

    message("Sudoku neu gestartet. Viel Erfolg!");

    refreshControls();
});


// ======================================================
// HINWEIS ANZEIGEN
// ======================================================

hintButton.addEventListener("click", async () => {

    if (
        !player ||
        busy ||
        submitted ||
        solved ||
        runningSince === null
    ) {
        return;
    }


    busy = true;
    refreshControls();


    try {

        const selected = selectedIndex === null
            ? null
            : [
                Math.floor(selectedIndex / 9),
                selectedIndex % 9
            ];


        const result = await postJson(
            `/api/hint/${encodeURIComponent(puzzleId)}`,
            {
                board: boardData(),
                selected: selected
            }
        );


        if (!result.ok) {

            message(
                result.data.error || "Kein Hinweis verfügbar.",
                "error"
            );

            return;
        }


        const { row, col, value } = result.data;

        const index = row * 9 + col;

        const field = fields[index];

        field.value = String(value);

        field.classList.add("hinted");

        setTimeout(() => {

            field.classList.remove("hinted");

        }, 950);


        hints++;

        lastWrongBoard = null;

        field.focus();

        selectCell(index);

        updateCounters();


        message(
            "💡 Eine richtige Zahl wurde eingetragen. Weiter so!",
            "success"
        );

    } catch (error) {

        message(
            "Hinweis konnte nicht geladen werden.",
            "error"
        );

    } finally {

        busy = false;

        refreshControls();
    }
});


// ======================================================
// INITIALISIERUNG
// ======================================================

setInterval(renderTimer, 250);

updateCounters();

updateHighlights();

refreshControls();

document.querySelector("#playerInput").focus();