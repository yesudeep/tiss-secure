(function($){

    jQuery(function(){

        var elements = {
            body: jQuery('body')
        },
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

        /**
         * Cycles the background color
         */
        function cycleBackgroundColor(){
            var c = colors;
            elements.body.animate({
                backgroundColor: c[Math.floor(Math.random() * c.length)]
            }, 2000);
        }
        setInterval(cycleBackgroundColor, 3000);
    });

})(jQuery);

