const labels = []
const data1 = [], data2 = [], data3 = []

function read_data(){
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
				var label = data[row][0].substr(11, 5);
				labels.push(label);
				data1.push(Number(data[row][1]));
				data2.push(Number(data[row][2]));
				data3.push(Number(data[row][3]));
			}
		}

		get_graphs();
	}
}
Chart.defaults.global.hover.mode = 'nearest';
//Chart.defaults.global.tooltips.mode = 'index';
//Chart.defaults.global.tooltips.position = 'nearest';
//Chart.defaults.global.tooltips.intersect = false;
//Chart.defaults.global.responsive = true;
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

var dic_options = {
	tooltip: {
		enabled: false,
    },
	maintainAspectRatio: false,
	title: {
		display: false,
	},
	legend: {
		display: false
	},
	scales: {
		yAxes: [{
            display: true,
            scaleLabel: {
               display: false,
			},
			ticks: {
				beginAtZero: true,
			}
		}],
		xAxes: [{
            display: true,
            stacked: false,
            gridLines: {
               display: false
            },
			ticks: {
				// 自動的に回転する角度を固定する
				maxRotation: 90,
				minRotation: 90,
			  }
		  
		}],
	},
	elements: {
		line: {
			tension: 0, // ベジェ曲線を無効にする
		}
	}
};

var dic_data = {
	labels: labels,
	datasets: [{
		label: 'CO2濃度', data: data1,
		borderColor: 'red', backgroundColor: 'red'
	},],
};

function getConf(){
	return {
    type: 'line',
    data: dic_data,
    options: dic_options,
	};
};


function get_graphs() {
	dic_options["scales"]["yAxes"][0]["scaleLabel"]["labelString"] = "ppm"
	dic_data["datasets"][0]["label"] = "CO2濃度"
	dic_data["datasets"][0]["data"] = data1
	conf = getConf();
	const chart1 = new Chart(document.getElementById('graph1').getContext('2d'), conf);
	chart1.update();

	dic_options["scales"]["yAxes"][0]["scaleLabel"]["labelString"] = "℃"
	dic_data["datasets"][0]["label"] = "温度"
	dic_data["datasets"][0]["data"] = data2
	conf = getConf();
	const chart2 = new Chart(document.getElementById('graph2').getContext('2d'), conf);
	chart2.update();

	dic_options["scales"]["yAxes"][0]["scaleLabel"]["labelString"] = "％"
	dic_data["datasets"][0]["label"] = "湿度"
	dic_data["datasets"][0]["data"] = data3
	conf = getConf();
	const chart3 = new Chart(document.getElementById('graph3').getContext('2d'), conf);
	chart3.update();
}

function refreshImage() {
	var now = new Date().getTime();
	var img1 = new Image();
	document.getElementById("image1").src = "./static/image1.jpg" +"?v=" + now;
	document.getElementById("image2").src = "./static/image2.jpg" +"?v=" + now;
}


function refreshChart() {
	refreshImage();
//	read_data();
//	get_graphs();

}

read_data();
setInterval(refreshChart, 60*100);		//0.1分ごとにグラフを更新する