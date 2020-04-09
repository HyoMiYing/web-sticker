// Show/Hide game rules

let instructionsText = document.getElementById('id_game_rules');
let instructionsLink = document.getElementById('id_instructions_link');

instructionsLink.addEventListener('click', showInstructions);

function showInstructions() {
    if (instructionsText.style.visibility == 'visible') {
        instructionsText.style.visibility = 'hidden';
        instructionsLink.textContent = 'Show instructions';
    } else {
        instructionsText.style.visibility = 'visible';
        instructionsLink.textContent = 'Hide instructions';
    }
}

// Select only cards from the same row

let allCards = document.querySelectorAll('label[for^="id_row"]');

for (let index = 0, len = allCards.length; index < len; index++) {
	allCards[index].addEventListener('click', uncheckCardsInOtherRows);
};

function uncheckCardsInOtherRows (e) {
	let currentRow = e.target.getAttribute('for').slice(3, 7);
	for (let index = 0, len = allCards.length; index < len; index++) {
		if (allCards[index].getAttribute('for').slice(3, 7) == currentRow) {
			
		} else {
			var inputId = allCards[index].getAttribute('for');
			document.getElementById(inputId).checked = false;
		}
	}
}

