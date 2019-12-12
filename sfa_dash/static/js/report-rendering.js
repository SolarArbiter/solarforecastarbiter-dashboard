/* 
 * Adds functionality for searching/nesting metrics plots. Plots should be
 * wrapped in a <div> element with class "metric-block" and the following data
 * attributes:
 *     data-category: The metric category, e.g. total, hourly.
 *     data-metric: The metric described in the plot.
 *     data-forecast: Name of the forecast.
 *
 * The content inside of the metric-block is arbitrary, this code only alters
 * the layout of the page.
 */

function hideMetricsOnSearch(){
    /*
     * Hides metrics whose forecasts names do not match the search term.
     */
    searchTerm = $(".search").val().toLowerCase();
    $('.metric-block').removeAttr('hidden');
    $('[class*="collapse-forecast-"]').removeAttr('hidden');
    noMatch = $('.metric-block').filter(function(i, el){
        plotForecast = el.dataset.forecast.toLowerCase();
        return plotForecast != 'all' && plotForecast.indexOf(searchTerm) < 0;
    });

    noMatchHeaderClasses = new Set(noMatch.map(function(){return $(this).data('forecast')}));
    noMatchHeaderClasses.forEach(function(fx){
        headers = $(`.collapse-forecast-${fx.replace(/ /g,"-").toLowerCase()}`);
        noMatch = noMatch.add(headers);
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
    collapse_button = $(`<a role="button" data-toggle="collapse" class="report-plot-section-heading collapse-${type.toLowerCase()}-${value.replace(/ /g,"-").toLowerCase()} collapsed"
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
    /*
     * Returns a selector for the proper container to insert the metricBlock
     * in to.
     */
    firstType = sortOrder[0].toLowerCase();
    firstValue = metricBlock.dataset[firstType].replace(/\s+/g, '-').toLowerCase();
    secondType = sortOrder[1].toLowerCase();
    secondValue = metricBlock.dataset[secondType].replace(/\s+/g, '-').toLowerCase();
    return `.data-wrapper-${firstType}-${firstValue} .data-wrapper-${secondType}-${secondValue}`;
}

function getSortedMetricBlocks(){
    /*
     * Builds and returns the new nested div structure based on the current
     * state of the sorting list.
     */
    
    // Determine the current order of the sorting list.
    sortOrder = $('.metric-sort .metric-sort-value').map(function(){
        return $(this).text();
    });

    // Create Sets from the unique metrics, categories and forecasts in the
    // report. These Sets will be used to create unique containers.
    categories = new Set($('.metric-block').map(function(){return this.dataset.category;}));
    metrics = new Set($('.metric-block').map(function(){return this.dataset.metric;}));
    forecasts = new Set($('.metric-block').map(function(){return this.dataset.forecast;}));

    // Create an ordered list of Sets based upon the current sorting order so
    // we can create containers from all permutations of the first two sets.
    orderedSets = sortOrder.map(function(){
        if (this == 'Category'){
            return categories;
        }else if(this == 'Forecast'){
            return forecasts;
        }else{
            return metrics;
        }
    });

    // Sort the metric blocks. Blocks should remain in order when they are
    // later sorted into their respective containers.
    sortedMetricBlocks = $('.metric-block').sort(selectSortFn(sortOrder[-1]));

    // Build nested divs for the first two sets of sorting attributes
    nestedContainers = createSubsetContainers(sortOrder, orderedSets);

    // Insert each metric block into it's container.
    $('.metric-block').each(function(){
        nestedContainers.find(containerSelector(sortOrder, this)).append(this);
    });
    return nestedContainers;
}

function applySorting(event, ui){
    /*
     * Callback fired when the sorting order changes. Replaces the html within
     * the outermost wrapper div with the sorted result.
     */
    $("#metric-plot-wrapper").html(getSortedMetricBlocks());
}

function sortingLi(sortBy){
    /*
     * Generate a list element with prefixed up/down arrows for controlling the
     * sorting order.
     */
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
    // Move the current element's parent li before the next li in the list.
    $(this).parent().prev().before($(this).parent());
    applySorting();
}


function downButtonCallback(){
    // Move the current element's parent li after the next li in the list.
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
    $('#metric-sorting').prepend($('<div><b>Use the arrows below to reorder the metrics plots.</b><div>'));
    applySorting();
});
