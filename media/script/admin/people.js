// common.js should be included before this file.

function personActions(person){
    return defaultActions('people', person) +
        '<a class="awesome-button" rel="add" href="/api/people/' + person.key + '/phones/new/" title="Add Phone"><span class="symbol">+</span> Add Phone</a>\
        <a class="awesome-button" rel="add" href="/api/people/' + person.key + '/addresses/new/" title="Add Address"><span class="symbol">+</span> Add Address</a>';
}

function createItemHTML(person){
    return dataListEntry(person, person.first_name + ' ' + person.last_name, personActions(person), defaultTags());
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

