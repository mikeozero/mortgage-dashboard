var ec_r1 = echarts.init(document.getElementById("r1"));

var option_r1 = {
        title: {
            text: 'LTV of New Uninsured Mortgages',
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
            formatter: '{b0}<br/>{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%<br />{a3}: {c3}%<br />{a4}: {c4}%'
        },
        grid: {
      		top: '15%',
      		left: '4%',
      		right: '6%',
      		bottom: '18%',
      		containLabel: true
      	},
        legend: {
            x: 'left',
			y: 'bottom',
            data: ['Less than 50%', '50.01 to 60%', '60.01 to 70%', '70.01 to 80%', 'Avg LTV'],
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
        yAxis: [
            {
                type: 'value',
                // scale: true,
                name: 'Percent',
                max: 100,
                nameLocation: 'middle',
                nameGap: 40,
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
            {
                type: 'value',
                // scale: true,
                name: 'Avg LTV',
                min: 45,
                max: 60,
                nameRotate: 270,
                nameLocation: 'middle',
                nameGap: 40,
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
                }
            }
        ],

        series: [
            {
                name: 'Less than 50%',
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
                data: [25, 25, 28, 29, 29]
            },
            {
                name: '50.01 to 60%',
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
                data: [10, 11, 10, 10, 10]
            },
            {
                name: '60.01 to 70%',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '{c}%'
                },
                emphasis: {
                    focus: 'series'
                },
                color: '#ADCD7E',
                data: [16, 15, 15, 15, 15]
            },
            {
                name: '70.01 to 80%',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: '{c}%'
                },
                emphasis: {
                    focus: 'series'
                },
                color: '#816D9B',
                data: [48, 49, 46, 46, 46]
            },
            {
                name: 'Avg LTV',
                type: 'line',
                symbol: 'circle',
                yAxisIndex: 1,
                color: 'black',
                data: [66, 64, 60, 59, 58]
            }
        ]
    };
	  
ec_r1.setOption(option_r1);

['resize','click'].forEach(function (item) {
    window.addEventListener(item,function(){
	   ec_r1.resize();
    });
});