(function($){
    jQuery(function(){
        var elements = {
            external_links: jQuery('a[href^="http://"]'),
            body: jQuery('body'),
            nav: jQuery('nav'),
            nav_tabs: jQuery('nav > div.handle > div > ul'),
            nav_panes: jQuery('nav > div > ul.panes'),
            google_talk_wrapper: jQuery('#google_talk_wrapper'),
            exposables: jQuery('.companies, .awesome-button')
        };
        elements.exposables.hover(function(){
                jQuery(this).expose({api:true, loadSpeed: 100, color: '#000'}).load();
            }, function(){
                jQuery(this).expose({api:true, closeSpeed: 100}).close();
            });
        elements.external_links.attr('target', '_blank').attr('title', 'Opens the link a new tab/window.');
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
        elements.google_talk_wrapper.toggle(function(){
            jQuery('#google_talk').css('height', '246px');
        }, function(){
            jQuery('#google_talk').css('height', '0px');
        });
        jQuery("#tabs").tabs("#panes > li", {
          effect: 'fade'
        });
        jQuery("#transparent_tabs").tabs("#panes > li", {
          effect: 'fade'
        });
        jQuery("#accordion").tabs("#accordion div.pane", {
          tabs: 'h2',
          effect: 'slide',
          initialIndex: null
        });
    });
})(jQuery);
