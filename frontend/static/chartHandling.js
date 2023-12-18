const chartBackgroundColors = [
    'rgba(49, 56, 102, 0.2)', //
    'rgba(80, 64, 153, 0.2)', //
    'rgba(151, 78, 195, 0.2)', //
    'rgba(254, 123, 229, 0.2)', //
    // 'rgb(54, 162, 235, 0.2)', // blue
    // 'rgb(153, 102, 255, 0.2)', // purple
    // 'rgb(201, 203, 207, 0.2)' // grey

];
const chartBorderColors = [
    'rgba(49, 56, 102)', //
    'rgba(80, 64, 153)', //
    'rgba(151, 78, 195)', //
    'rgba(254, 123, 229)', //
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

function updateFaultComparisonChart(resData) {
      //reset chart
      faultComparisonChart.data.datasets = [];

      for (key in resData) {
        const color = getColorForAlgorithm(key);

        const newDataset = {
          label: key,
          data: [resData[key]],
          backgroundColor: color.backgroundColor,
          borderColor: color.borderColor,
          borderWidth: 2,
          maxBarThickness: 250
        };

        faultComparisonChart.data.datasets.push(newDataset);
      }

      faultComparisonChart.data.labels = [document.getElementById('faultsFrameSize').value];
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

Chart.register(ChartDataLabels);
let faultComparisonChart = new Chart(faultComparisonCanvas, {
  type: 'bar',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    scales: {
      y: {
        ticks: {
          color: "#3b4351",
          beginAtZero: true,
          stepSize: 1
        },
        grid: {
          drawTicks: false,
        },
        border: {
          dash: [5, 10],
        },
      },
      x: {
        ticks: {
          color: "#3b4351",
        },
        grid: {
          display: false,
        },
        border: {
          display: false,
        },
      },
    },
    plugins: {
        datalabels: {
          color: 'blackS',
          font: {
            weight: 'bold'
          }
        }
    }
  }
});

function updateFaultRangeComparisonChart(resData) {
  const labels = [];
  let data = [];
  let i = 0; //to detect first element --> duplicate labels

  //reset chart
  faultRangeComparisonChart.data.datasets = [];

  for (key in resData) {
    resData[key].forEach((item) => {
      data.push(item.Faults);
      if (i === 0){
        labels.push(item.Frames);
      }
    })

    i = 1;

    const color = getColorForAlgorithm(key);

    const newDataset = {
      label: key,
      data: data,
      backgroundColor: color.backgroundColor,
      borderColor: color.borderColor,
      borderWidth: 2,
      fill: false
    };

    faultRangeComparisonChart.data.datasets.push(newDataset);
  }

  faultRangeComparisonChart.data.labels = labels;
  faultRangeComparisonChart.update();
  faultRangeComparisonCanvas.style.display = 'block';
}

const faultRangeComparisonCanvas = document.getElementById('faultRangeComparisonCanvas');
faultRangeComparisonCanvas.style.display = 'none';

Chart.register(ChartDataLabels);

let faultRangeComparisonChart = new Chart(faultRangeComparisonCanvas, {
type: 'bar',
data: {
    labels: [],
    datasets: []
},
options: {
    scales: {
      y: {
        ticks: {
          color: "#3b4351",
          beginAtZero: true,
          stepSize: 1
        },
        grid: {
          drawTicks: false,
        },
        border: {
          dash: [5, 10],
        },
      },
      x: {
        ticks: {
          color: "#3b4351",
        },
        grid: {
          display: false,
        },
        border: {
          display: false,
        },
      },
    },
    plugins: {
        datalabels: {
          color: 'blackS',
          font: {
            weight: 'bold'
          }
        }
    }
  }
});
