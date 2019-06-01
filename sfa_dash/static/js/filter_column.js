$(document).ready(function() {
    var availableOrgs = new Set([]);
    var orgs = $(".provider-column");
    for (i = 0; i < orgs.length; i++) {
        availableOrgs.add(orgs[i].textContent);
    }
    //$(".provider-th")
    var filter_div = $("<div class='org-filters'>org-filters</div>");
    filter_div.appendTo(".observation-tools");
    availableOrgs.forEach(function (e) {$(".org-filters").append(`<input class="org-filter-option"value="${e}" type="checkbox" checked>${e}`)});
    
    $(".org-filter-option").change(function() {
        console.log(`${this.checked}`);
        console.log(` content: ${this.value}`);
        if (this.checked) {
            $(`.provider-column:contains("${this.value}")`).parent().show();
        } else {
           $(`.provider-column:contains("${this.value}")`).parent().hide();
        }
    });
});
