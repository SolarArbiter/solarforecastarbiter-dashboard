/* Jquery for filtering and searching tables.
 * Defines filter functions that return a jquery object list of items that need to be hidden
 * from the table. The functions should be registered in the `toHideFns` list to be called by
 * callback functions. At the end of the file, your widgets should have their callback set to
 * the `applyTableFilters` function
 *
 * The containsi filter was borrowed from the below codepen:
 * https://codepen.io/adobewordpress/pen/gbewLV
 */
$(document).ready(function() {
    /* Add containsi filter to JQuery selectors that selects for any word in a phrase */
    $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
            return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
        }
    });
    
    // list of functions to use to build the list of rows to hide
    var toHideFns = []

    function searchTable() {
        /* Reads the value of the search input and creates a list of rows to hide
         * based on which rows do not contain the search term
         */
        var searchTerm = $(".search").val();
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
        return $(".results tbody tr").not(":containsi('" + searchSplit + "')")
    }
    toHideFns.push(searchTable);

    function filteredOrgs() {
        orgsToHide = $([]);
        $('.org-filter-option').each(function (e){
            if (!this.checked){
                orgsToHide = orgsToHide.add($(`.provider-column:contains("${this.value}")`).parent());
            }
        });
        return orgsToHide
    }
    if ($('#provider-header').length){
        // check for the id of the table header for the provider(organization field)
        // and insert checkboxes to hide/display the table rows
        var availableOrgs = new Set([]);
        var orgs = $(".provider-column")
        for (i = 0; i < orgs.length; i++) {
            availableOrgs.add(orgs[i].textContent);
        }
        var filter_div = $("<div id='org-filters' class='collapse'>Filter by Organization <a href='#' role='button' id='org-filter-collapse'></a><br/><hr><ul class='org-filter-options'></ul></div>");
        filter_div.appendTo("#provider-header");
        availableOrgs.forEach(function (e) {$(".org-filter-options").append(`<li><input class="org-filter-option"value="${e}" type="checkbox" checked>${e}</li>`)});
        $('#org-filter-collapse').click(function() {
            $('#org-filters').collapse('toggle');
        });
        toHideFns.push(filteredOrgs);
    }
   
    function allHiddenElements(){
        /* Returns a JQuery object list of rows that need to be hidden
         * concatenating the results of calls to the toHideFns
         */
        elements = $([]);
        toHideFns.forEach(function(e){
            elements = elements.add(e());
        });
        return elements
    }
    function applyTableFilters() {
        /* Gets a list of table rows, and then builds a list of all the
         * rows to be excluded due to filters, removes the rows to hide
         * from all rows, sets the remainder to visible and hides the
         */ others.
        allRows = $(".results tbody tr").not('.warning.no-result');
        rowsToHide = allHiddenElements();
        visibleRows = allRows.not(rowsToHide);
        visibleRows.attr('visible', 'true');
        rowsToHide.attr('visible', 'false');
        
        var jobCount = $('.results tbody tr[visible="true"]').length;
        if(jobCount == '0') {$('.no-result').show();}
        else {$('.no-result').hide();}
    }
    
    /*
     * Register dom element callbacks
     */
    $(".search").keyup(applyTableFilters);
    if ($(".search").val() != null){
        // on page load, check for values in the search field.
        // if they exist, run the filtering function
        applyTableFilters();
    }
    $(".org-filter-option").change(applyTableFilters);

});
