/*
 *  Creates inputs for defining observation, forecast pairs for a report.
 */
$(document).ready(function() {
    function searchSelect(inputSelector, selectSelector, offset=0){
        /*
         * Retrieves the value the <input> element identified by inputSelector and
         * returns a jquery list of the <option> elements inside the element
         * identified by selectSelector that do not contain the value.
         * Passing an offset ignores the first offset items.
         */
        var searchTerm = $(inputSelector).val();
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('");
        return $(selectSelector + " option").slice(offset).not(":containsi('" + searchSplit + "')");
    }


    function addObservation(obsName, obsId){
        /*
         * Returns a Jquery object containing 4 input elements representing a forecast,
         * observation pair:
         */
        var new_observation = $(`<div class="aggregate-observation aggregate-observation-${observation_index}">
                <div class="input-wrapper">
                  <div class="col-md-12">
                    <input type="text" class="form-control observation-field" name="observation-name-${observation_index}" required disabled value="${obsName}"/>
                    <input type="hidden" class="form-control observation-field" name="observation-id-${observation_index}" required value="${obsId}"/>
                  </div>
                 </div>
                 <a role="button" class="observation-delete-button">x</a>
               </div>`);
        var remove_button = new_observation.find(".observation-delete-button");
        remove_button.click(function(){
            console.log('i do');
            new_observation.remove();
            if ($('.observation-list .aggregate-observation').length == 0){
                $('.empty-aggregate-observation-list')[0].hidden = false;
            }
        });
        return new_observation;
    }


    function newSelector(depends_on=null){
        /*
         * Returns a JQuery object containing labels and select elements for appending options to.
         * Initializes with one default and one optional select option:
         *     Always adds an option containing "No matching <field_Type>s
         *     Inserts a "Please enter an Interval Length" disabled option.
         */
        return $(`<div class="form-element full-width observation-select-wrapper">
                    <label>Select an Observation</label>
                      <div class="aggregate-observation-filters"><input id="observation-option-search" class="form-control half-width" placeholder="Search"/></div><br>
                    <div class="input-wrapper">
                      <select id="observation-select" class="form-control observation-field" name="observation-select" size="5">
                      <option id="no-interval-length-selection" disabled> Please enter an Interval Length </option>
                      <option id="no-observations" disabled hidden>No matching Observations</option>
                    </select>
                    </div>
                  </div>`);
    }

    function calculate_interval_length(){
        value = $('.interval_length-value-field').val();
        units = $('.interval_length-units-field').val();
        if (units == 'minutes'){
            minutes = value;
        }else if (units == 'hours'){
            minutes = value * 60;
        }else if (units == 'days'){
            minutes = value * 1440;
        }else {
            minutes = 0;
        }
        return parseInt(minutes);
    }
    function createObservationSelector(){
        /*
         * Creates a selectable list of observations for injecting into the DOM
         */
        
        /*
         *  Filtering Functions
         *      Callbacks for hidding/showing select list options based on the searchbars
         *      for each field and previously made selections
         */
        function filterObservations(){
            observations = $('#observation-select option').slice(2);
            // Show all of the observations
            observations.removeAttr('hidden');
            // retrieve the current site id and variable from the selected forecast

            if ($('.interval_length-value-field').val()){
                // remove any border highlighting
                $('.interval_length-value-field').css('border', '');
                $('#no-interval-length-selection').attr('hidden', 'true');
                variable = variable_select.val();
                interval_length = calculate_interval_length();
                
                // Build the list of options to hide by creating a set from
                // the lists of elements to hide from search, site id and variable
                var toHide = searchSelect('#observation-option-search', '#observation-select', 2);
                toHide = toHide.add(observations.not(`[data-variable=${variable}]`));
                toHide = toHide.add(observations.filter(function(index){
                    return parseInt(this.dataset.intervalLength) > interval_length;
                }));
                toHide.attr('hidden', true);
            }else{
                $('.interval_length-value-field').css('border', '2px solid #F99');
                $('#no-interval-length-selection').removeAttr('hidden');
                observations.attr('hidden', true);
            }

            // if the current selection is hidden, deselect it
            if (toHide && toHide.filter(':selected').length){
                observation_select.val('');
            }
            if (toHide && toHide.length == observations.length){
                $('#no-observations').removeAttr('hidden');
            } else {
                $('#no-observations').attr('hidden', true);
            }
        }

        // Declare handles to each field's input widgets, and insert a variable select
        // widget for Forecast filtering.
        var widgetContainer = $('<div class="pair-selector-wrapper collapse"></div>');
        var obsSelector = newSelector();
        var addButton = $('<a role="button" class="btn btn-primary" id="add-object-pair" style="padding-left: 1em">Add a Forecast, Observation pair</a>');

        // Add the elements to the widget Container, so that the single container may
        // be inserted into the DOM
        widgetContainer.append(obsSelector);
        widgetContainer.append(addButton);

        // Register callback functions
        obsSelector.find('#observation-option-search').keyup(filterObservations);

        // create variables pointing to the specific select elements
        var observation_select = obsSelector.find('#observation-select');
        var variable_select = $('.variable-field');
        variable_select.change(filterObservations);
        $('.interval_length-value-field').change(filterObservations);
        $('.inverval_length-units-field').change(filterObservations);

        // insert options from page_data into the select elements
        
        $.each(Object.values(page_data), function(){
            observation_select.append(
                $('<option></option>')
                    .html(this.name)
                    .val(this.observation_id)
                    .attr('hidden', true)
                    .attr('data-site-id', this.site_id)
                    .attr('data-variable', this.variable)
                    .attr('data-interval-length', this.interval_length)
                    .attr('data-interval-value-type', this.interval_value_type));
        });
        
        addButton.click(function(){
            /*
             * 'Add a Forecast, Observation pair button on button click
             *
             * On click, appends a new pair of inputs inside the 'pair_container' div, initializes
             * their select options and increment the pair_index.
             */
            if (observation_select.val()){
                // If both inputs contain valid data, create a pair and add it to the DOM
                var selected_observation = observation_select.find('option:selected')[0];
                observation = addObservation(selected_observation.text,
                                             selected_observation.value);

                observation_list_container.append(observation);
                observation_index++;
                $(".empty-aggregate-observation-list")[0].hidden = true;
                observation_select.css('border', '');
            } else {
                // Otherwise apply a red border to alert the user to need of input
                if (observation_select.val() == null){
                    observation_select.css('border', '2px solid #F99');
                }
            }
        });
        return widgetContainer;
    }
    /*
     * Initialize global variables
     * observation_index - used for labelling listed observations
     * observation_container - JQuery handle for the ul to hold observations
     * observation_control_container - JQuery handle for div to hold the select widgets to
     *     add new observations to an aggregate.
     */
    observation_list_container = $('.aggregate-observation-list');
    observation_control_container = $('.aggregate-observation-control');
    observation_index = 0;
    // call the function to initialize the pair creation widget and insert it into the DOM
    observation_selection_element = createObservationSelector();
    observation_control_container.append($('<a role="button" class="full-width object-pair-button collapsed" data-toggle="collapse" data-target=".pair-selector-wrapper">Add observations</a>'));
    observation_control_container.append(observation_selection_element);
    variable_select = $('.variable-field');
});
