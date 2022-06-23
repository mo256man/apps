const label = [], num = [], ct = [];

const timeUnix = (time1, time2) => {
    const n_time = new Date(time1);
    const time = n_time.getTime();
    return time;
}

const req = new XMLHttpRequest();
req.open("GET", "./static/data.csv", true);
req.send(null);

req.onload = () => {
    if (req.status != 404) {
        const line = req.responseText.split("\n");
        const data = [];
        for (let i = 0; i < line.length - 1; ++i) {
            const cells = line[i].split(",");
            data.push(cells);
        }
        for (let row in data) {
            label.push(timeUnix(data[row][0], data[row][1]));
            num.push(data[row][2]);
            ct.push(data[row][3]);
        }
    }
}

Chart.defaults.global.defaultFontSize = 16;
Chart.defaults.global.tooltips.mode = 'index';
Chart.defaults.global.tooltips.position = 'nearest';
Chart.defaults.global.tooltips.intersect = false;
Chart.defaults.global.responsive = true;
Chart.defaults.global.legend.labels.boxWidth = 10;

Chart.defaults.global.elements.point = {
    radius: 0,
    pointHitRadius: 10,
};

Chart.defaults.global.elements.line = {
    tension: 0,
    borderWidth: 2,
    fill: false,
    borderDash: [],
};

const conf = {
    type: 'line',
    data: {
        labels: label,
        datasets: [{
            label: '実績数', data: num, yAxisID: 'y-1',
            borderColor: 'red', backgroundColor: 'red'
        },{
            label: 'C/T', data: ct,  yAxisID: 'y-2',
            borderColor: 'blue', backgroundColor: 'blue'
        },],
    },
    options: {
        title: {
            display: true,
            text: '職場環境',
            fontSize: 30
        },
        scales: {
            yAxes: [{
                id: 'y-1',
                position: 'right',
                gridLines: {
                    drawOnChartArea: false
                },
            },{
                id: 'y-2',
                position: 'left',
                scaleLabel: {
                    display: true,
                    labelString: 'sec'
                },
                ticks: {
                    min: 0,
                    max: 100,
                    stepSize: 20
                },
            },],
            xAxes: [{
                type: 'time',
                time: {
                    displayFormat: 'h:mm'
                },
            },],
        },
    },
};

const chart = new Chart(document.getElementById('graph').getContext('2d'), conf);