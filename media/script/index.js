(function($){

    jQuery(function(){

        var elements = {
            body: jQuery('body')
        };

        function cycleBackgroundColor(){
            var colors = ["#0c50dc",
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
            var index = Math.floor(Math.random() * colors.length);
            console.log(index);
            var color = colors[index];
            console.log("changing color to: " + color);
            elements.body.animate({backgroundColor: color}, 2000);
            console.log("changing color");
        }

        setInterval(cycleBackgroundColor, 6000);
    });

})(jQuery);

