function gettime(){
	$.ajax({
		url:"/time",
		timeout:10000,
		success:function(data){
			$("#tim h2").html(data)
		},
		error:function(xhr,type,errorThrown){						
		}
	})
}

function get_l1_data(){
	$.ajax({
		url:"/l1",
		success:function(data){
			option_l1.xAxis.data = data.quarters
			option_l1.series[0].data = data.gt90
			option_l1.series[1].data = data.gt30
			option_l1.series[2].data = data.rpt
			ec_l1.setOption(option_l1)
		},
		error:function(xhr,type,errorThrown){
		}
	})
}

function get_c1_data(){
	$.ajax({
		url:"/c1",
		success:function(data){
			option_c1.legend.data = data.regions
			option_c1.xAxis.data = data.quarters
			var series = [];
			for(var i=0;i<data.regions.length;i++){
				series.push({
					name: data.regions[i],
					data: data.values[i],
					type: 'line',
					symbol: 'emptyCircle',
					symbolSize: 5,
					color: color[i],
					// smooth: true
				})
			}
			option_c1.series = series
			ec_c1.setOption(option_c1)
		},
		error:function(xhr,type,errorThrown){						
		}
	})
}
function get_r1_data(){
	$.ajax({
		url:"/r1",
		success:function(data){
			option_r1.xAxis.data = data.quarters
			option_r1.series[0].data = data.l5rt
			option_r1.series[1].data = data.b56rt
			option_r1.series[2].data = data.b67rt
			option_r1.series[3].data = data.b78rt
			option_r1.series[4].data = data.avg
			ec_r1.setOption(option_r1)
		},
		error:function(xhr,type,errorThrown){						
		}
	})
}

// 初始化运行一次
gettime()
get_l1_data()
get_c1_data()
get_r1_data()

setInterval(gettime,1000)
setInterval(get_l1_data,1000*86400)
setInterval(get_c1_data,1000*86400)
setInterval(get_r1_data,1000*86400)