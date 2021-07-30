var ec_lb = echarts.init(document.getElementById("lb"));

var option_lb = {
        title: {
            text: 'Credit Card Risk Composition - CRI',
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
      		top: '18%',
      		left: '4%',
      		right: '6%',
      		bottom: '15%',
      		containLabel: true
      	},
        legend: {
            x: 'left',
			y: 'bottom',
            data: ['A+B', 'C', 'D+E'],
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
                name: '% Share of Outstandings',
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
            }
        ],

        series: [
            {
                name: 'A+B',
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
                data: [25, 25, 28]
            },
            {
                name: 'C',
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
                data: [10, 11, 10]
            },
            {
                name: 'D+E',
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
                data: [16, 15, 15]
            }
        ]
    };

ec_lb.setOption(option_lb);

['resize','click'].forEach(function (item) {
    window.addEventListener(item,function(){
	   ec_lb.resize();
    });
});