const boardElement = document.getElementById('board');
const cells = document.querySelectorAll('.cell');
const messageElement = document.getElementById('message');
const restartButton = document.getElementById('restartButton');

// Current state and player
let currentPlayer = 'X';

// Handle user clicks on the board
cells.forEach(cell => {
    cell.addEventListener('click', handleClick);
});

async function handleClick(e) {
    const index = e.target.dataset.index;

    // Player's turn (X)
    if (currentPlayer === 'X') {
        const response = await fetch('http://127.0.0.1:8000/move/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ index: parseInt(index) })
        });
        const result = await response.json();

        if (result.message === 'Move registered') {
            e.target.textContent = 'X';
            if (result.winner) {
                messageElement.textContent = `${result.winner} Wins!`;
                disableBoard();
            } else if (result.message === "It's a tie!") {
                messageElement.textContent = "It's a tie!";
            } else {
                currentPlayer = 'O';
                await computerMove();
            }
        } else {
            messageElement.textContent = result.message; // e.g., Not player's turn
        }
    }
}

// Computer's move (O's turn) - GET request
async function computerMove() {
    const response = await fetch('http://127.0.0.1:8000/computer/');
    const result = await response.json();

    if (result.message === 'Computer moved') {
        const index = result.move;
        cells[index].textContent = 'O';

        if (result.winner) {
            messageElement.textContent = `${result.winner} Wins!`;
            disableBoard();
        } else if (result.message === "It's a tie!") {
            messageElement.textContent = "It's a tie!";
        } else {
            currentPlayer = 'X';
        }
    } else {
        messageElement.textContent = result.message; // e.g., Not computer's turn
    }
}

// Disable the board after a win
function disableBoard() {
    cells.forEach(cell => {
        cell.removeEventListener('click', handleClick);
    });
}

// Restart game logic - POST request to reset the game
restartButton.addEventListener('click', async () => {
    const response = await fetch('http://127.0.0.1:8000/reset/', {
        method: 'POST'
    });
    const result = await response.json();

    if (result.message === 'Game reset') {
        cells.forEach(cell => {
            cell.textContent = '';
            cell.addEventListener('click', handleClick);
        });
        messageElement.textContent = '';
        currentPlayer = 'X';
    }
});
