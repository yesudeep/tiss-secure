// common.js should be included before this file.

function createItemHTML(job){
    return dataListEntry(job, job.title, defaultActions('jobs', job), defaultTags());
}

function editItem(){

}

jQuery(function(){
    jQuery.getJSON('/api/jobs/list/', {}, function(jobs){
        var job = {};
        var html = [];
        for (var i = 0, len = jobs.length; i < len; ++i){
            job = jobs[i];
            html.push(createItemHTML(job));
        }
        jQuery('#data-list').html(html.join(''));
    });
});

