jQuery(function(){
    //make some charts
    jQuery('#summer_pie_chart, #final_pie_chart').visualize({
        type: 'pie', 
        pieMargin: 40, 
        title: 'Sector Wise Split',
        width: 800,
        height:350,
        colors: ['#5a0000','#740101', '#8f0b0b', '#a43200', '#ba4917', '#ba5c17', '#d9742b', '#e08727', '#ed891e', '#ed9d1e']
    });	
});
