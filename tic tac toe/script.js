const boardElement = document.getElementById('board');
const cells = document.querySelectorAll('.cell');
const messageElement = document.getElementById('message');
const restartButton = document.getElementById('restartButton');

let xState = Array(9).fill(0);
let oState = Array(9).fill(0);
let currentPlayer = 'X';

// Winning combinations
const winningCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

// Handle user clicks on the board
cells.forEach(cell => {
    cell.addEventListener('click', handleClick);
});

function handleClick(e) {
    const index = e.target.dataset.index;

    if (xState[index] === 0 && oState[index] === 0) {
        if (currentPlayer === 'X') {
            xState[index] = 1;
            e.target.textContent = 'X';
            if (checkWin(xState)) {
                messageElement.textContent = "X Wins!";
                disableBoard();
            } else if (checkTie()) {
                messageElement.textContent = "It's a tie!";
            } else {
                currentPlayer = 'O';
                computerMove();
            }
        }
    }
}

// Check for winning conditions
function checkWin(state) {
    return winningCombos.some(combo => {
        return combo.every(index => {
            return state[index] === 1;
        });
    });
}

// Check for tie
function checkTie() {
    return [...xState, ...oState].every(val => val !== 0);
}

// Computer's move (O's turn)
function computerMove() {
    let availableMoves = [];
    xState.forEach((val, index) => {
        if (val === 0 && oState[index] === 0) {
            availableMoves.push(index);
        }
    });
    
    const randomIndex = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    oState[randomIndex] = 1;
    cells[randomIndex].textContent = 'O';

    if (checkWin(oState)) {
        messageElement.textContent = "O Wins!";
        disableBoard();
    } else if (checkTie()) {
        messageElement.textContent = "It's a tie!";
    } else {
        currentPlayer = 'X';
    }
}

// Disable the board after a win
function disableBoard() {
    cells.forEach(cell => {
        cell.removeEventListener('click', handleClick);
    });
}

// Restart game logic
restartButton.addEventListener('click', () => {
    xState.fill(0);
    oState.fill(0);
    cells.forEach(cell => {
        cell.textContent = '';
        cell.addEventListener('click', handleClick);
    });
    messageElement.textContent = '';
    currentPlayer = 'X';
});
