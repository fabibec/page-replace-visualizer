const api = document.getElementById('url-base').getAttribute('data-name')  + 'api/';
const refStringForm = document.getElementById('refStringForm');
const faultForm = document.getElementById('faultForm');
const faultRangeForm = document.getElementById('faultRangeForm');
const memoryViewForm = document.getElementById('memoryViewForm');

// Updating RefString Slider
function updateSliderValue(sliderID, valueID){
  let length = document.getElementById(sliderID).valueAsNumber;
  document.getElementById(valueID).innerHTML = '<b>' + length + '</b>';
}
updateSliderValue('refStrSize', 'refStrSizeValue');
updateSliderValue('faultsFrameSize', 'FrameSizeValue');
updateSliderValue('memoryFrameSize', 'memoryFrameSizeValue');


// Select all checkboxes -not working as of now
function toggleAllCheckboxes(source, destName) {
    checkboxes = document.getElementsByName(destName);
    for(var checkbox in checkboxes)
      checkbox.checked = source.checked;
}

// RefString form validation
refStringForm.addEventListener('submit', async event => {
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
  
});

function createTableHeader(key) {
  th = document.createElement('th');
  th.appendChild(document.createTextNode(key));
  return th;
}

function createMemoryTableObj(htmlTableObj, memoryTableObj, algorithm) {
  
  for (const [key, v] of Object.entries(memoryTableObj[0].MemoryView)) {
    tr = document.createElement('tr');
    // Header
    tr.appendChild(createTableHeader('Frame ' + key))

    memoryTableObj.forEach(item => {
      if (algorithm !== 'SC') {
        td = document.createElement('td');
        if (item.MemoryView[key] == null) {
          icon = document.createElement('i');
          icon.classList.add('icon', 'icon-minus');
          td.appendChild(icon);
        } else {
          td.appendChild(document.createTextNode(item.MemoryView[key]));
        }
        tr.appendChild(td);
      } 
    });
    htmlTableObj.appendChild(tr);
  }     
}

// Memory View form validation
memoryViewForm.addEventListener('submit', async event => {
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
    let button = document.getElementById('memoryViewBtn');
    
    button.classList.toggle('loading');

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

        console.log(resData);

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
            default:
              tr = document.createElement('tr');
              tr.appendChild(createTableHeader(key));
          };

          // Insert the data
          resData.MemoryTable.forEach(item => {
              switch(key) {
                case ('MemoryView'):
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

        tableInsert = document.getElementById('memoryTable');
        console.log(table);
        tableInsert.replaceChildren(table);
    } catch (err) {
        console.log(err.message);
    }

    button.classList.toggle('loading');

});

// Faults form validation
faultForm.addEventListener('submit', async event => {
  event.preventDefault();

  let opt = document.getElementById('faultsOptSlct').checked;
  let fifo = document.getElementById('faultsFifoSlct').checked;
  let sc = document.getElementById('faultsScSlct').checked;
  let lru = document.getElementById('faultsLruSlct').checked;
  let refString = btoa(document.getElementById('refStrInpt').value);
  let frames = document.getElementById('faultsFrameSize').value;
  let button = document.getElementById('faultsCompareBtn');
  
  button.classList.toggle('loading');

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
      document.getElementById('faultsReturn').innerHTML = resData;
  } catch (err) {
      console.log(err.message);
  }

  button.classList.toggle('loading');

});

// Chart js test
const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
