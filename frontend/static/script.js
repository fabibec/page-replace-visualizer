const api = document.getElementById('url-base').getAttribute('data-name')  + 'api/';

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


document.getElementById('faultsCompareBtn').addEventListener('click', function (event) {

    event.preventDefault();
    const all = document.getElementById('faultsAllSlct').checked;
    const fifo = document.getElementById('faultsFifoSlct').checked;
    const opt = document.getElementById('faultsOptSlct').checked;
    const sc = document.getElementById('faultsScSlct').checked;
    const lru = document.getElementById('faultsLruSlct').checked;
    const refString = btoa(document.getElementById('refStringInpt').value);
    const frames = document.getElementById('frameInpt').value;
    const query = 'referenceString=' + refString + '&frames=' + frames + '&fifo=' + (fifo||all) + '&opt=' + (opt||all) + '&sc=' + (sc||all) + '&lru=' + (lru||all) + '&base64=' + 'true';
    console.log(query);
    fetch(api + 'faults/compare?' + query)
        .then(response => response.json())
        .then(data => {

            console.log(data);
            //chart.js logic

                    })
        .catch(err => console.log(err));
});
