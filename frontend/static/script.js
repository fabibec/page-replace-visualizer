const api = document.getElementById('url-base').getAttribute('data-name')  + 'api/';
const refStrInpt = document.getElementById('refStrInpt');
const refStringForm = document.getElementById('refStringForm');
const faultForm = document.getElementById('faultForm');
const faultRangeForm = document.getElementById('faultRangeForm');
const memoryViewForm = document.getElementById('memoryViewForm');

const chartBackgroundColors = [
    'rgba(255, 99, 132, 0.2)', // red
    'rgba(255, 159, 64, 0.2)', // orange
    'rgba(255, 205, 86, 0.2)', // yellow
    'rgba(75, 192, 192, 0.2)', // green
    // 'rgb(54, 162, 235, 0.2)', // blue
    // 'rgb(153, 102, 255, 0.2)', // purple
    // 'rgb(201, 203, 207, 0.2)' // grey

];
const chartBorderColors = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    // 'rgb(54, 162, 235)', // blue
    // 'rgb(153, 102, 255)', // purple
    // 'rgb(201, 203, 207)' // grey
 ];
const fifoColor = {
    backgroundColor: chartBackgroundColors[0],
    borderColor: chartBorderColors[0]
};
const scColor = {
    backgroundColor: chartBackgroundColors[1],
    borderColor: chartBorderColors[1]
};
const lruColor = {
    backgroundColor: chartBackgroundColors[2],
    borderColor: chartBorderColors[2]
};
const optColor = {
    backgroundColor: chartBackgroundColors[3],
    borderColor: chartBorderColors[3]
};

//
function flagRefStrInptField(){
  let el = refStrInpt;
  let msg = document.getElementById('refStrInptMsg');
  if (el.value) {
    el.parentElement.classList.add('has-success');
    el.parentElement.classList.remove('has-error');
    msg.style.display = 'none';
  } else {
    el.parentElement.classList.remove('has-success');
    el.parentElement.classList.add('has-error');
    msg.style.display = 'block';
  }
}


// Updating RefString Slider
function updateSliderValue(sliderID, valueID){
  let length = document.getElementById(sliderID).valueAsNumber;
  document.getElementById(valueID).innerHTML = '<b>' + length + '</b>';
}



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
    flagRefStrInptField();
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
        console.log(resData);
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
      updateFaultComparisonChart(resData);

  } catch (err) {
      console.log(err.message);
  }

  button.classList.toggle('loading');

});

function updateFaultComparisonChart(resData) {
      const labels = [];
      const data = [];
      const backgroundColor = [];
      const borderColor = [];
      for (key in resData) {
        labels.push(key);
        data.push(resData[key]);
        const color = getColorForAlgorithm(key);
        backgroundColor.push(color.backgroundColor);
        borderColor.push(color.borderColor);
      }
      faultComparisonChart.data.labels = labels;
      faultComparisonChart.data.datasets[0].data = data;
      faultComparisonChart.data.datasets[0].backgroundColor = backgroundColor;
      faultComparisonChart.data.datasets[0].borderColor = borderColor;
      faultComparisonChart.update();
      faultComparisonCanvas.style.display = 'block';
}

function getColorForAlgorithm(algorithm) {
  switch(algorithm) {
    case ('FIFO'):
      return fifoColor;
    case ('SC'):
      return scColor;
    case ('LRU'):
      return lruColor;
    case ('OPT'):
      return optColor;
    default:
      return fifoColor;
  }
}

const faultComparisonCanvas = document.getElementById('faultComparisonCanvas');
faultComparisonCanvas.style.display = 'none';

let faultComparisonChart = new Chart(faultComparisonCanvas, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: 'Page Faults',
        data: [],
        borderWidth: 2,
        backgroundColor: [],
        borderColor: [],
        maxBarThickness: 250
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

  function init(){
    updateSliderValue('refStrSize', 'refStrSizeValue');
    updateSliderValue('faultsFrameSize', 'FrameSizeValue');
    updateSliderValue('memoryFrameSize', 'memoryFrameSizeValue');
    flagRefStrInptField();
  }