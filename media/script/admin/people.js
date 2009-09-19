// common.js should be included before this file.

function createItemHTML(person){
    return dataListEntry(person, person.first_name + ' ' + person.last_name, defaultActions('people', person), defaultTags());
}

function editItem(){

}

jQuery(function(){
    jQuery.getJSON('/api/people/list', {}, function(people){
        var person, html = [];
        for (var i = 0, len = people.length; i < len; ++i){
            person = people[i];
            html.push(createItemHTML(person));
        }
        jQuery('#data-list').html(html.join(''));
    });
});

