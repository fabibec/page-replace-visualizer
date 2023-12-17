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

Chart.register(ChartDataLabels);
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