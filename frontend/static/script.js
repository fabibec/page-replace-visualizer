
// local testing
// const api = 'http://localhost:8000/api/';
// production
const api = 'https://os.remberger.dev/api/';

document.getElementById('generateBtn').addEventListener('click', function (event) {

    const length = document.getElementById('lengthInpt').value;

    if (length >= 4 && length <= 30) {
        event.preventDefault();
    } else {
        return;
    }

    const locality = document.getElementById('localizationTggl').checked;
    const input = document.getElementById('refStringInpt');

    fetch(api + 'refString?length=' + length + '&locality=' + locality)
        .then(response => response.json())
        .then(data => {

            input.value = data.ReferenceString;

        })
        .catch(err => console.log(err));
    }
);


