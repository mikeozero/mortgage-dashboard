var ec_c2 = echarts.init(document.getElementById("c2"));

var option_c2 = {
    title: {
        text: 'New Uninsured Mortgage: Authorized Amount',
        textStyle: {
            color: 'gray',
            fontSize: 15
        },
        subtext: 'Distribution by Amortization Range',
        subtextStyle: {
            color: 'gray',
            fontSize: 12
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        },
        formatter: '{b0}<br/>{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%'
    },
    legend: {
        x: 'left',
		y: 'bottom',
        left: 'center',
        textStyle: {
            color: 'gray'
        },
        data: ['20 yrs or Less', '20 to 25 yrs', 'More than 25yrs']
    },
    grid: {
        top: '23%',
        left: '6%',
        right: '5%',
        bottom: '12%',
        containLabel: true
    },
    toolbox: {
        show: false,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: [
        {
            type: 'category',
            axisTick: {show: false},
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
            data: ['Q4-13', 'Q1-14', 'Q2-14', 'Q3-14', 'Q4-14']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'Percent',
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
            name: '20 yrs or Less',
            type: 'bar',
            barGap: 0,
            label: {show: true,color: 'gray',fontSize: 11,position: 'top',formatter: '{c}%'},
            emphasis: {
                focus: 'series'
            },
            color: 'steelblue',
            data: [320, 332, 301, 334, 390]
        },
        {
            name: '20 to 25 yrs',
            type: 'bar',
            label: {show: true,color: 'gray',fontSize: 11,position: 'top',formatter: '{c}%'},
            emphasis: {
                focus: 'series'
            },
            color: '#CD5C5C',
            data: [220, 182, 191, 234, 290]
        },
        {
            name: 'More than 25yrs',
            type: 'bar',
            label: {show: true,color: 'gray',fontSize: 11,position: 'top',formatter: '{c}%'},
            emphasis: {
                focus: 'series'
            },
            color: '#ADCD7E',
            data: [150, 232, 201, 154, 190]
        }
    ]
};

ec_c2.setOption(option_c2);

window.addEventListener("resize",function(){
	   ec_c2.resize();
});
window.addEventListener("click",function(){
	   ec_c2.resize();
});