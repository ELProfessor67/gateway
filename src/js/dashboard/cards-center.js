

(function($) {
    /* "use strict" */
	
 var dlabChartlist = function(){
	
	var screenWidth = $(window).width();	

	var polarChart = function(){
		 var ctx = document.getElementById("polarChart").getContext('2d');
			//Chart.defaults.global.legend.display = false;
			var myChart = new Chart(ctx, {
				type: 'polarArea',
				data: {
					labels: ["Mon", "Tue", "Wed", "Thu"],
					datasets: [{
						backgroundColor: [
							"#496ecc",
							"#68e365",
							"#ffa755",
							"#c8c8c8"
						],
						data: document.getElementById("polarChart").getAttribute("data-data").split("-").map(ele => +ele)
					}]
				},
				options: {
					plugins:{
						legend:false,
						tooltip:{
							enabled:false,
						}
					},
					maintainAspectRatio: false,
					
						scales: {
						r:{
							ticks: {
								display: false,
							},
							grid: {
								display: false,
							},
						},
                        
                   
					},
					
				}
			});
	}
 
	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				polarChart();
				
					
			},
			
			resize:function(){
			}
		}
	
	}();

	
		
	jQuery(window).on('load',function(){
		setTimeout(function(){
			dlabChartlist.load();
		}, 1000); 
		
	});

     

})(jQuery);