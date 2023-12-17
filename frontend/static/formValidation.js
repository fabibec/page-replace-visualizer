/* Constant Elements */
const api = document.getElementById('url-base').getAttribute('data-name')  + 'api/';
const refStrInpt = document.getElementById('refStrInpt');
const refStringForm = document.getElementById('refStringForm');
const faultForm = document.getElementById('faultForm');
const faultRangeForm = document.getElementById('faultRangeForm');
const memoryViewForm = document.getElementById('memoryViewForm');
const faultsRangeMinVal = document.getElementById('faultsRangeMinVal');
const faultsRangeMaxVal = document.getElementById('faultsRangeMaxVal');

/* General Validation functions*/
const showError = (input, message) => {
    // get the form-field element
    const formField = input.parentElement;
    // add the error class
    formField.classList.remove('has-success');
    formField.classList.add('has-error');

    // show the error message
    const error = formField.querySelector('.form-input-hint');
    error.textContent = message;
};

const showSuccess = (input) => {
    // get the form-field element
    const formField = input.parentElement;

    // remove the error class
    formField.classList.remove('has-error');
    formField.classList.add('has-success');

    // hide the error message
    const error = formField.querySelector('.form-input-hint');
    error.textContent = '';
}

const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        // cancel the previous timer
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        // setup a new timer
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};

const isRefStringValid = (refStr) => {
    const re = /^[\w\s]+(,[\w\s]+)*$/;
    return re.test(refStr);
};

const isEmpty = value => value === '' ? true : false;

/* Reference String Form */
refStringForm.addEventListener('submit', async event => {
    submitReferenceString(event);
});

// Validate Reference String input from user
refStringForm.addEventListener('input', debounce(function (e) {
    let refString = document.getElementById('refStrInpt').value;
    if(!isRefStringValid(refString) || isEmpty(refString)){
        showError(refStrInpt, 'Please provide or generate a valid reference string.');
        return;
    } else {
        showSuccess(refStrInpt);
    }
}))

async function submitReferenceString(event) {
    event.preventDefault();

    let length = document.getElementById('refStrSize').value;
    let locality = document.getElementById('localityTggl').checked;
    let input = document.getElementById('refStrInpt');
    let button = document.getElementById('generateRefStr');

    button.classList.toggle('loading');

    try {
        const res = await fetch(api + 'refString?length=' + length + '&locality=' + locality);
        const resData = await res.json();
        input.value = resData.ReferenceString;
    } catch (err) {
        console.log(err.message);
    }

    button.classList.toggle('loading');
}

/* Faults From */
faultForm.addEventListener('submit', async event => {submitFaults(event)});

async function submitFaults(event) {
    event.preventDefault();

    let refString = document.getElementById('refStrInpt').value;

    // validate Ref String
    if(!isRefStringValid(refString) || isEmpty(refString)){
        showError(refStrInpt, 'Please provide or generate a valid reference string.');
        return;
    }

    showSuccess(refStrInpt);

    let opt = document.getElementById('faultsOptSlct').checked;
    let fifo = document.getElementById('faultsFifoSlct').checked;
    let sc = document.getElementById('faultsScSlct').checked;
    let lru = document.getElementById('faultsLruSlct').checked; 
    let frames = document.getElementById('faultsFrameSize').value;
    let msg = document.getElementById('faultsMsg');
    refString = btoa(refString);

    // Show error if item is empty
    if (!(opt || fifo || sc || lru)){
        showError(msg, 'Please select at least one algorithm');
        return;
    };

    showSuccess(msg);
    
    try {
        const res =
            await fetch(
                api + 'faults/compare?referenceString=' + refString
                + '&frames=' + frames
                + '&FIFO=' + fifo
                + '&SC=' + sc
                + '&LRU=' + lru
                + '&OPT=' + opt
                + '&base64=' + true);
        const resData = await res.json();
        updateFaultComparisonChart(resData);
    
    } catch (err) {
        console.log(err.message);
    }
}

/* Faults by Range Form */

faultsRangeMinVal.addEventListener('change', validateMax);
faultsRangeMinVal.addEventListener('input', validateMax);
faultsRangeMinVal.addEventListener('keyup', validateMax);
faultsRangeMinVal.addEventListener('paste', validateMax);

function validateMax () {
    if (faultsRangeMaxVal.value > faultsRangeMinVal.max + 1) {
        
    }
    faultsRangeMaxVal.min = faultsRangeMinVal.max + 1; 


}


/* Memory View Form */
memoryViewForm.addEventListener('submit', async event => {submitMemoryView(event)});

async function submitMemoryView(event) {
    event.preventDefault();
    let selectVal = document.getElementById('algorithmSelect').value;
    let AlgorithmVals = new Array(4).fill(false);

    switch(selectVal) {
      case 'FIFO':
        AlgorithmVals[0] = true;
        break;
      case 'SC':
        AlgorithmVals[1] = true;
        break;
      case 'LRU':
        AlgorithmVals[2] = true;
        break;
      case 'OPT':
        AlgorithmVals[3] = true;
        break;
      default:
        AlgorithmVals[0] = true;
    }

    let refString = btoa(document.getElementById('refStrInpt').value);
    let frames = document.getElementById('memoryFrameSize').value;

    try {
        const res =
            await fetch(
                api + 'faults/memory?referenceString=' + refString
                + '&frames=' + frames
                + '&FIFO=' + AlgorithmVals[0]
                + '&SC=' + AlgorithmVals[1]
                + '&LRU=' + AlgorithmVals[2]
                + '&OPT=' + AlgorithmVals[3]
                + '&base64=' + true);
        const resData = await res.json();

        // Create Table Element
        let table = document.createElement('table');
        table.classList.add('table', 'table-scroll');

        // Iterate over MemoryFrame every key in MeomoryFrame list
        for (const [key, v] of Object.entries(resData.MemoryTable[0])) {

          // The left column always contains the name
          switch(key) {
            case ('MemoryView'):
              createMemoryTableObj(table, resData.MemoryTable, resData.PageReplaceAlgorithm);
              break;
            case ('ModifiedBits'):
            case ('CursorPosition'):
                break;
            default:
              tr = document.createElement('tr');
              tr.appendChild(createTableHeader(key));
          };

          // Insert the data
          resData.MemoryTable.forEach(item => {
              switch(key) {
                case ('MemoryView'):
                case ('ModifiedBits'):
                case ('CursorPosition'):
                  break;
                case ('PageFault'):
                  td = document.createElement('td');
                  if (item[key]) {
                    icon = document.createElement('i');
                    icon.classList.add('icon', 'icon-cross');
                    td.appendChild(icon);
                  } else {
                    td.appendChild(document.createTextNode("\u00b7"))
                  }
                  tr.appendChild(td);
                  break;
                default:
                  td = document.createElement('td');
                  td.appendChild(document.createTextNode(item[key]));
                  tr.appendChild(td);
              };
            }
          );

          table.appendChild(tr)
        }
        localStorage.setItem('memTable', table);
        tableInsert = document.getElementById('memoryTable');
        tableInsert.replaceChildren(table);
    } catch (err) {
        console.log(err.message);
    }
}

function createTableHeader(key) {
    th = document.createElement('th');
    th.appendChild(document.createTextNode(key));
    return th;
}

function createMemoryTableObj(htmlTableObj, memoryTableObj, algorithm) {

    for (const [key, v] of Object.entries(memoryTableObj[0].MemoryView)) {
      tr = document.createElement('tr');
      // Header
      tr.appendChild(createTableHeader('Frame ' + (Number(key) + 1)));
      // Data
      memoryTableObj.forEach(item => {
        td = document.createElement('td');
        if (algorithm === 'SC') {
          // Add cursor icon
          if (item.CursorPosition === Number(key)) {
            cursor = document.createElement('icon');
            console.log('Key=' + key + ' | index=' + item.CursorPosition)
            cursor.classList.add('icon', 'icon-forward', 'cursor');
            td.appendChild(cursor);
          }
          // Null icon replacement
          if(item.MemoryView[key] == null) {
            td.appendChild(document.createTextNode("\u00b7"));
          } else {
            td.appendChild(document.createTextNode(item.MemoryView[key]));
            // Add modified Bit for SC
            mdBit = document.createElement('sub');
            mdBit.appendChild(document.createTextNode('(' + item.ModifiedBits[key] +')'));
            td.appendChild(mdBit);
          } 
        } else {
          if(item.MemoryView[key] == null) {
            td.appendChild(document.createTextNode("\u00b7"));
          } else {
            td.appendChild(document.createTextNode(item.MemoryView[key]));
          }
        }
        tr.appendChild(td);
      });
      htmlTableObj.appendChild(tr);
    }
}

