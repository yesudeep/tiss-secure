(function($){
    jQuery(function(){
        jQuery("#chained").scrollable({
          size: 4,
          speed: 800,
          easing: 'easeInOutQuint'
        })
        .autoscroll({
            steps: 4,
            interval: 800
        })
        .circular();
    });
})(jQuery);

