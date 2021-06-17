var ec_c1 = echarts.init(document.getElementById("c1"));

var color=['#00EE00','#ff9f7f','#FFD700','#00ced1','#4682B4','#FF0000','#000000']

var option_c1 = {

      	// backgroundColor: '#FFF0F5',

      	title: {
      		text: 'Residential Mortgage Regional Delinquency',
      		// subtext: '模拟数据',
      		// x: 'center',
			textStyle: {
				color: 'gray',
				fontSize: 15
			},
			left: 'left'
      	},

      	legend: {
      		// orient 设置布局方式，默认水平布局，可选值：'horizontal'（水平） ¦ 'vertical'（垂直）
      		// orient: 'horizontal',
      		// x 设置水平安放位置，默认全图居中，可选值：'center' ¦ 'left' ¦ 'right' ¦ {number}（x坐标，单位px）
      		// x: 'left',
      		// y 设置垂直安放位置，默认全图顶端，可选值：'top' ¦ 'bottom' ¦ 'center' ¦ {number}（y坐标，单位px）
      		// y: 'top',
			orient: 'vertical',
			x: 'right',
			y: 'top',
      		data: [],
			// left: 'center',
			textStyle: {
				color: 'gray'
			}
      	},

      	//  图表距边框的距离,可选值：'百分比'¦ {number}（单位px）
      	grid: {
      		top: '15%', // 50 等价于 y: '16%'
      		left: '5%',
      		right: '12%',
      		bottom: '12%',
      		containLabel: true
      	},

      	// 提示框
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
      		// name: '周几',
      		type: 'category',
			// splitNumber: 0,
			axisLine: {
				show: true,
				lineStyle: {
					// 设置y轴颜色
					color: 'gray'
				}
			},
			axisLabel: {
				show: true,
				color: 'gray',
				fontSize: 12,
				rotate: 0,
				interval: 0 //设置X轴数据间隔几个显示一个，为0表示都显示
			},
      		// // boundaryGap值为false的时候，折线第一个点在y轴上
      		// boundaryGap: false,
      		data: []
      	},

      	yAxis: {
      		name: '% Delinquency Rate',
			nameLocation: 'middle',
			nameGap: 50,
      		type: 'value',
      		// min: 0, // 设置y轴刻度的最小值
      		// max: 1800, // 设置y轴刻度的最大值
      		splitNumber: 0, // 设置y轴刻度间隔个数
      		axisLine: {
				show: true,
      			lineStyle: {
      				// 设置y轴颜色
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
      			// 设置小圆点消失 symbol: 'none',
      			// 注意：设置symbol: 'none'以后，拐点不存在了，设置拐点上显示数值无效
      			// 设置折线弧度，取值：0-1之间
				color: '#00EE00',
      			smooth: false
      		}
      	]
    };

ec_c1.setOption(option_c1)

window.addEventListener("resize",function(){
	   ec_c1.resize();
});