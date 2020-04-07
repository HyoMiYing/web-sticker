let instructionsText = document.getElementById('id_instructions_text');
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


var rows = document.getElementsByClassName('row');
console.log(rows)

function getAllRowsButThisOne(clickedRow) {
    for (let row of rows) {
        console.log(clickedRow)
        if (row == clickedRow) {
        } else {
            var allInputsInRow = row.getElementsByTagName('input');
            for (let input of allInputsInRow) {
                input.checked = false;
            }
        }
    }
}
        
for (let row of rows) {
    row.addEventListener('click', function () {

        getAllRowsButThisOne(row);
    });
}

function uncheckBoxesInOtherRows() {
    console.log(pa.id);
    // var allRowsButThisOne = rows - 

}