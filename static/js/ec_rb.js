var ec_rb = echarts.init(document.getElementById("rb"));

var color=['#00EE00','#ff9f7f','#FFD700','#00ced1','#4682B4','#FF0000','#000000']

var option_rb = {

      	title: {
      		text: 'Credit Cards - Reportable Delinquency (%)',
			textStyle: {
				color: 'gray',
				fontSize: 15
			},
			left: 'left'
      	},

      	legend: {
			x: 'left',
			y: 'bottom',
			left: 'center',
      		data: [],
			textStyle: {
				color: 'gray'
			}
      	},

      	grid: {
      		top: '15%', // 50 等价于 y: '16%'
      		left: '6%',
      		right: '5%',
      		bottom: '20%',
      		containLabel: true
      	},

      	tooltip: {
      		trigger: 'axis',
			axisPointer: {
				type: 'line',
				lineStyle: {
					color: '#7171C6'
				}
			},
			formatter: '{b0}<br/>{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%<br />{a3}: {c3}%<br />{a4}: {c4}%<br />{a5}: {c5}%<br />{a6}: {c6}%'
      	},

      	xAxis: {
      		type: 'category',
			axisLine: {
				show: true,
				lineStyle: {
					color: 'gray'
				}
			},
			axisLabel: {
				show: true,
				color: 'gray',
				fontSize: 12,
				rotate: 0,
				interval: 0
			},
      		data: []
      	},

      	yAxis: {
      		name: '% Delinquency',
			nameLocation: 'middle',
			nameGap: 35,
      		type: 'value',
      		splitNumber: 0,
      		axisLine: {
				show: true,
      			lineStyle: {
      				color: 'gray'
      			}
      		},
			axisLabel: {
				show: true,
				color: 'gray',
				fontSize: 12,
				formatter: '{value}%'
			},
			splitLine: {
				show: false,
				lineStyle: {
					color: '#172738',
					width: 1,
					type: 'solid'
				}
			}
      	},

      	series: [{
      			name: 'xxx',
      			data: [],
      			type: 'line',
				color: '#00EE00',
      			smooth: false
      		}
      	]
    };

ec_rb.setOption(option_rb)

window.addEventListener("resize",function(){
	   ec_rb.resize();
});
window.addEventListener("click",function(){
	   ec_rb.resize();
});