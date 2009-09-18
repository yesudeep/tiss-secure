// common.js should be included before this file.

function createItemHTML(article){
    return dataListEntry(article, article.title, defaultActions('news', article), defaultTags());
}

function editItem(){

}

jQuery(function(){
    jQuery.getJSON('/api/news/list/', {}, function(news){
        var article = {};
        var html = [];
        for (var i = 0, len = news.length; i < len; ++i){
            article = news[i];
            html.push(createItemHTML(article));
        }
        jQuery('#data-list').html(html.join(''));
    });
});

