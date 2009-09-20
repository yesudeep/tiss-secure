(function($){

    jQuery(function(){

        var elements = {
            body: jQuery('body'),
            nav: jQuery('nav'),
            nav_tabs: jQuery('nav > div.handle > div > ul'),
            nav_panes: jQuery('nav > div > ul.panes'),
            google_talk_minimize: jQuery('#google_talk_wrapper a[href="#google_talk"]'),
        }; /*,
        colors = [
                "#362d1d",
                "#0c50dc",
                "#7cb306",
                "#800080",
                "#602414",
                "#321e0b",
                "#aebd87",
                "#ba6e87",
                "#5e3a49",
                "#62671a",
                "#38927c",
                "#ae6ad2",
                "#6a8efd",
                "#818fd7",
                "#6f59d6",
                "#306fb8",
                "#85b91e",
                "#8dccdc",
                "#84b2dc",
                "#19400f",
                "#1e1f82",
                "#7061eb",
                "#55315c",
                "#685f7d",
                "#2f4385",
                "#5c3c0f"
                ];
        // Cycles the background color
        function cycleBackgroundColor(){
            var c = colors;
            elements.body.animate({
                backgroundColor: c[Math.floor(Math.random() * c.length)]
            }, 1000);
        }
        setInterval(cycleBackgroundColor, 10000);
        */
        elements.nav.hoverIntent(function(){
            //elements.nav.stop().animate({top: "0px"}, 800, "easeInOutQuint");
        },
        function(){
            elements.nav.stop().animate({top: "-200px"}, 400, "easeInOutQuint");
        });
        jQuery('a', elements.nav_tabs).click(function(event){
            event.preventDefault();
            event.stopPropagation();
            elements.nav.stop().animate({top: "0px"}, 400, "easeInOutQuint");
            return false;
        });
        elements.nav_tabs.tabs('nav > div > ul.panes > li', {
            event: 'mouseover'
        });
        elements.google_talk_minimize.toggle(function(){
            jQuery('#google_talk').css('height', '0px');
        }, function(){
            jQuery('#google_talk').css('height', '246px');
        });
        jQuery("#tabs").tabs("#panes > li", {
          effect: 'fade'
        });
    });

})(jQuery);

