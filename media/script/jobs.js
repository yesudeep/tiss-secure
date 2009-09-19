jQuery(function(){
    jQuery('#new_job').live('submit', function(event){
        event.preventDefault();
        event.stopPropagation();

        return false;
    });
});

