var ec_lt = echarts.init(document.getElementById("lt"));

var option_lt = {
        title: {
            text: 'Credit Card Delinquency',
            textStyle: {
                color: 'gray',
                fontSize: 15
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: '{b0}<br/>{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'
        },
        grid: {
      		top: '15%',
      		left: '6%',
      		right: '5%',
      		bottom: '15%',
      		containLabel: true
      	},
        legend: {
            x: 'left',
			y: 'bottom',
            data: ['>90 dpd', '31-90 dpd', 'Reportable Delinquency'],
            left: 'center',
			textStyle: {
				color: 'gray'
			}
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
				fontSize: 12
			},
            data: ['Q4-13','Q1-14','Q2-14','Q3-14','Q4-14']
        },
        yAxis: {
            type: 'value',
            // scale: true,
            name: '% Delinquency',
            nameLocation: 'middle',
            nameGap: 35,
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
					color: '#808080',
					width: 1,
					type: 'solid'
				}
			}
        },
        series: [
            {
                name: '>90 dpd',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '{c}%'
                },
                emphasis: {
                    focus: 'series'
                },
                color: 'steelblue',
                data: [2.7, 6.0, 5.0, 3.0, 8.0]
            },
            {
                name: '31-90 dpd',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '{c}%'
                },
                emphasis: {
                    focus: 'series'
                },
                color: '#CD5C5C',
                data: [7.3, 7.0, 10.0, 5.0, 4.0]
            },
            {
                name: 'Reportable Delinquency',
                type: 'line',
                label: {
                    show: true,
                    formatter: '{c}%'
                },
                symbol: 'circle',
                color: 'black',
                data: [10.0, 13.0, 15.0, 8.0, 12.0]
            }
        ]
    };

ec_lt.setOption(option_lt);

['resize','click'].forEach(function (item) {
    window.addEventListener(item,function(){
	   ec_lt.resize();
    });
});