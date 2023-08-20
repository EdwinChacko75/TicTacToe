let gameBoard = [['', '', ''], ['', '', ''], ['', '', '']];
let player = 'X';
let computer = 'O';
let firstMove = player;

function resetGame() {
    gameBoard = [['', '', ''], ['', '', ''], ['', '', '']];
    player = 'X';
    computer = 'O';
    const pTags = document.querySelectorAll('p');
    pTags.forEach(pTag => {
        pTag.innerHTML = '';

        if (pTag.classList.contains('filled')) {    
            pTag.classList.remove('filled');
        }
    });
    document.getElementById('reset').style.display = 'none';
    document.getElementById('overMessage').style.display = 'none';
}

async function clickEvent(element) {
    const clickedPTag = element.target.querySelector('p');

    if (!clickedPTag.classList.contains('filled')) {
        makePlayerMove(clickedPTag, player);
        const computerMove = await requestComputerMove();
        if (computerMove) {
            makePlayerMove(computerMove, computer);
        }
    }
}

function makePlayerMove(clickedPTag, player) {
    const clickedElementId = clickedPTag.parentNode.id.split('') ;

    clickedPTag.innerHTML = player;
    clickedPTag.classList.add('filled');
    gameBoard[clickedElementId[0]][clickedElementId[1]] = player;
}

async function requestComputerMove() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch('/tttgame/api/makeMove/', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
               'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ board: gameBoard, player: computer }),
        });
        const data = await response.json();

        if (data.isOver) {
            data.message = data.winner ? `${data.winner} wins!` : 'Draw!';
            document.getElementById('overMessage').innerHTML = data.message;
            document.getElementById('overMessage').style.display = 'flex';
            document.getElementById('reset').style.display = 'flex';
        } 
        if (data.move) {
            return document.getElementById(data.move).querySelector('p');
        }
        
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var boardElement = document.getElementById('board');
    boardElement.addEventListener('click', clickEvent);    
});