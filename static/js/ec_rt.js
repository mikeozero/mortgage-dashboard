var ec_rt = echarts.init(document.getElementById("rt"));

var option_rt = {
        title: {
            text: 'Total Limit, New Credit Card Bookings',
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
            formatter: '{b0}<br/>{a0}: ${c0}<br />{a1}: ${c1}'
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
            data: ['Visa Total Limit', 'Amex Total Limit'],
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
            name: 'Millions',
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
				formatter: '${value}'
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
                name: 'Visa Total Limit',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '${c}'
                },
                emphasis: {
                    focus: 'series'
                },
                color: 'steelblue',
                data: [2.7, 6.0, 5.0, 3.0, 8.0]
            },
            {
                name: 'Amex Total Limit',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '${c}'
                },
                emphasis: {
                    focus: 'series'
                },
                color: '#CD5C5C',
                data: [7.3, 7.0, 10.0, 5.0, 4.0]
            }
        ]
    };

ec_rt.setOption(option_rt);

['resize','click'].forEach(function (item) {
    window.addEventListener(item,function(){
	   ec_rt.resize();
    });
});