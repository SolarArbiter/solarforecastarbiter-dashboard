/*
 * 
 */

function hideMetricsOnSearch(){
    /*
     * Hides metrics whose forecasts names do not match the search term.
     */
    searchTerm = $(".search").val();
    $('.metric-block').removeAttr('hidden');
    noMatch = $('.metric-block').filter(function(i, el){
        plotForecast = el.dataset.forecast.toLowerCase();
        return plotForecast.indexOf(searchTerm) < 0;
    });
    noMatch.attr('hidden', true);
}
function genericSort(a, b){
    if (a > b){
        return -1;
    } else if (a < b){
        return 1;
    }
    return 0;
}

function sortByMetric(a, b){
    return genericSort(a.dataset.metric, b.dataset.metric);
}

function sortByCategory(a, b){
    return genericSort(a.dataset.category, b.dataset.category);
}

function sortByForecast(a,b){
    return genericSort(a.dataset.forecast, b.dataset.forecast);
}

function selectSortFn(type){
    if (type == 'Category'){
        return sortByCategory;
    }else if (type == 'Forecast'){
        return sortByForecast;
    }else if (type == "Metric"){
        return sortByMetric;
    }
}

function createContainerDiv(parentValue, type, value){
    /* Creates a heading and div for the type and value. The heading acts as a
     * collapse button for each div. When parentValue is not null, parentValue
     * is appended as a class to the div to differentiate between sub sections.
     *
     * e.g. If we are nesting by metrics->category->forecast, we need to be
     * able to select the 'total' category in each metric section without
     * expanding them all at once. So passing in the metric's value allows us
     * to select the specific category to expand like so:
     *     'data-wrapper-category-total.{metric name}'
     */
    wrapper_class = `data-wrapper-${type.toLowerCase()}-${value.replace(/ /g,"-").toLowerCase()}${parentValue ? ' '+parentValue: ''}`
    collapse_button = $(`<a role="button" data-toggle="collapse" class="report-plot-section-heading collapsed"
                            data-target=".${wrapper_class.replace(/ /g,".")}">
                         <h3 class="report-plot-section-heading-text">${type}: ${value}</h3></a>`)
    wrapper = $(`<div class="plot-attribute-wrapper ${wrapper_class} collapse"></div>`);
    return [wrapper, collapse_button]
}

function createSubsetContainers(sortOrder, valueSet){
    /* Builds the containing divs based on the first two elements of the 
     * sort order such that each nested container has a 
     * data-wrapper-{field}-{value} class for later selection. Nested divs
     * will have the value of their parent div added as a class to
     * differentiate targets for collapsing.
     *
     * example:
     *   <div class="data-wrapper-metric-mae">
     *     <div class="data-wrapper-category-total mae">
     *     </div>
     *   </div>
     */
    container = $('<div class="plot-container"></div>');
    valueSet[0].forEach(function (firstSetItem){
        [top_level, top_collapse] = createContainerDiv(null, sortOrder[0], firstSetItem);
        valueSet[1].forEach(function (secondSetItem){
            [second_level, second_collapse] = createContainerDiv(firstSetItem, sortOrder[1], secondSetItem)
            top_level.append(second_collapse);
            top_level.append(second_level);
        })
        container.append(top_collapse);
        container.append(top_level);
    });
    container.find('a:first').removeClass('collapsed');
    firstElement = container.find('div.plot-attribute-wrapper:first');
    firstElement.addClass('show');
    firstElement.find('a').removeClass('collapsed');
    firstElement.find('div.plot-attribute-wrapper').addClass('show');
    return container;
}

function containerSelector(sortOrder, metricBlock){
    firstType = sortOrder[0].toLowerCase();
    firstValue = metricBlock.dataset[firstType].toLowerCase();
    secondType = sortOrder[1].toLowerCase();
    secondValue = metricBlock.dataset[secondType].toLowerCase();
    return `.data-wrapper-${firstType}-${firstValue} .data-wrapper-${secondType}-${secondValue}`;
}
function subsetMetricBlocks(sortOrder){
    // First create a Sets from the unique metrics, categories and forecasts
    // in the report
    categories = new Set($('.metric-block').map(function(){return this.dataset.category;}));
    metrics = new Set($('.metric-block').map(function(){return this.dataset.metric;}));
    forecasts = new Set($('.metric-block').map(function(){return this.dataset.forecast;}));

    // Create an ordered list of the set values based upon the current sorting
    // order.
    orderedSets = sortOrder.map(function(){
        if (this == 'Category'){
            return categories;
        }else if(this == 'Forecast'){
            return forecasts;
        }else{
            return metrics;
        }
    });
    // pre-sort the blocks they should remain sorted when they are placed in
    // their respective divs
    sortedMetricBlocks = $('.metric-block').sort(selectSortFn(sortOrder[-1]));
    nestedContainers = createSubsetContainers(sortOrder, orderedSets);
    $('.metric-block').each(function(){
        nestedContainers.find(containerSelector(sortOrder, this)).append(this);
    });
    $('#metric-plot-wrapper').html(nestedContainers);
}

function applySorting(event, ui){
    var sortOrder = $('.metric-sort .metric-sort-value').map(function(){
        return $(this).text();
    });
    $("#metric-plot-wrapper").html(subsetMetricBlocks(sortOrder));
}

function sortingLi(sortBy){
    liElem = $('<li class="metric-sort"></li>');
    upButton = $('<a role="button" class="arrow-up"></a>');
    upButton.click(upButtonCallback);
    downButton = $('<a role="button" class="arrow-down"></a>');
    downButton.click(downButtonCallback);
    liElem.append(upButton);
    liElem.append(downButton);
    liElem.append(`<span class="metric-sort-value">${sortBy}</span>`);
    return liElem;
}
function upButtonCallback(){
    $(this).parent().prev().before($(this).parent());
    applySorting();
}
function downButtonCallback(){
    $(this).parent().next().after($(this).parent());
    applySorting();
}
$(document).ready(function(){
    /* Create sorting widgets to insert into the template, we do this here
     * because there may be cases where we won't include js, and want to
     * statically print all of the metrics.
     */
    sortingWidgets = $('<ul id="metrics-sort-list"></ul>');
    sortingWidgets.append(sortingLi("Metric"));
    sortingWidgets.append(sortingLi("Category"));
    sortingWidgets.append(sortingLi("Forecast"));
    searchBar = $('<input type="text" placeholder="Search by forecast name" class="search">');
    searchBar.keyup(hideMetricsOnSearch);
    $('#metric-sorting').prepend(searchBar);
    $('#metric-sorting').prepend(sortingWidgets);
    // Add help text
    $('#metric-sorting').prepend($('<div><b>Use the arrows below to reorder the metrics plots.</b><div>'));
    applySorting();
});
