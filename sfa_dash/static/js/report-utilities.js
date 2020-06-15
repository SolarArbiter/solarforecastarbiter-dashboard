/******************************************************************************
 * Makes common report form handling functions available via the report_utils
 * global variable
 *****************************************************************************/
report_utils = new Object();

report_utils.fill_existing_pairs = function(){
    /*
     * Fill object pairs from the parsed form data.
     */
    try{
        var object_pairs = form_data['report_parameters']['object_pairs'];
    } catch(error) {
        return;
    }
    // Create a list to unpack as arguments of addPair. This allows passing
    // extra args for cdf forecasts.
    var pair_container = $('.object-pair-list');
    object_pairs.forEach(function(pair){
        var pair_args = [];
        if (pair.hasOwnProperty('observation')){
            var truth_type = 'observation';
        } else {
            var truth_type = 'aggregate';
        }
        pair_args.push(truth_type);

        let truth_id = pair[truth_type];
        let truth_metadata = report_utils.searchObjects(truth_type+'s', truth_id);
        pair_args.push(truth_metadata['name']);
        pair_args.push(truth_id);

        let forecast_id = pair['forecast'];
        let forecast_metadata = report_utils.searchObjects('forecasts', forecast_id);
        pair_args.push(forecast_metadata['name']);
        pair_args.push(forecast_id);

        let reference_forecast_id = pair['reference_forecast'];
        if (reference_forecast_id){
            var reference_forecast_metadata = report_utils.searchObjects(
                'forecasts',
                reference_forecast_id);
        } else {
            var reference_forecast_metadata = {'name': 'Unset'};
        }
        pair_args.push(reference_forecast_metadata['name']);
        pair_args.push(reference_forecast_id);

        [uncertainty_label, uncertainty_value] = report_utils.parseDeadband(
            pair['uncertainty']);
        pair_args.push(uncertainty_label);
        pair_args.push(uncertainty_value);

        forecast_type = pair['forecast_type'];
        pair_args.push(forecast_type);

        if (forecast_type.startsWith('probabilistic_')){
            console.log(forecast_type);
            if (forecast_type == 'probabilistic_forecast'){
                var distribution_id = forecast_metadata['forecast_id'];
                var constant_value_label = 'Distribution';
            } else {
                var distribution_id = forecast_metadata['parent'];
                var constant_value_label = report_utils.constant_value_label(
                    forecast_metadata, forecast_metadata['constant_value']);
            }
            pair_args.push(constant_value_label);
            pair_args.push(distribution_id);
        }
        pair = addPair(...pair_args);
        $(".empty-reports-list").attr('hidden', 'hidden');
        report_utils.set_units(forecast_metadata['variable']);
    });
}

// toggle_reference_dependent_metrics
report_utils.toggle_reference_dependent_metrics = function(){
    /*
     * Disables and de-selects the forecast skill metric if not all of the
     * object pairs have reference foreasts.
     */
    var reference_exist = $('.reference-forecast-value').map(function(){
        return $(this).val();
    }).get().some(x=>x!='null');
    var skill = $('[name=metrics][value=s]');
    if (reference_exist){
        // show skill remove warning
        $('#reference-warning').remove();
    } else {
        // hide skill, insert warning
        if ($('#reference-warning').length == 0){
            $(`<span id="reference-warning" class="warning-message">
               (Requires reference forecast selection)</span>`
             ).insertAfter(skill.next());
        }
    }
}

/******************************************************************************
 *
 * Set and unset current units based on a variable.
 *
 *****************************************************************************/
//global current_units variable
current_units = null;


report_utils.unset_units = function(){
    /* Set units to null when the last pair is removed */
    current_units = null;
    report_utils.setVariables()
}

report_utils.set_units = function(variable){
    units = sfa_dash_config.VARIABLE_UNIT_MAP[variable];
    if(units){
        current_units = units;
    }
    report_utils.setVariables();
}

report_utils.searchObjects = function(object_type, object_id){
    /* Get a json object from the page_data object.
     *
     * @param {string} object_type - The type of the object to search for.
     *     One of 'forecasts', 'sites', 'observations', 'aggregates'.
     *
     * @param {string} object_id - UUID of the object to search for
     *
     * @returns {Object} An object containing the SFA object's metadata.
     */
    try{
        var objects = page_data[object_type];
        if (object_type == 'forecasts'
            && page_data.hasOwnProperty('constant_values')){
            // If constant values are present, and we're searching for a
            // forecast, merge the constant values.
            objects = objects.concat(page_data['constant_values']);
            console.log('added constant values');
        }
        var id_prop = object_type.slice(0, -1) + '_id';
        var metadata = objects.find(e => e[id_prop] == object_id);
    }catch(error){
        return null;
    }
    return metadata;
}

report_utils.setVariables = function(){
	/* Displays or hides options in the variable <select> element based on the
     * current units.
     */
    variable_options = $('#variable-select option');
    variable_options.removeAttr('hidden');
    variable_options.removeAttr('disabled');
    if (current_units){
        variable_options.each(function(){
            units = sfa_dash_config.VARIABLE_UNIT_MAP[$(this).attr('value')]
            if(units != current_units){
                $(this).attr('hidden', true);
                $(this).attr('disabled', true);
            }
        });
    }
    $('#variable-select').val(variable_options.filter(":not([hidden])").val());
}

report_utils.changeVariable = function(){
    report_utils.setVariables();
    filterForecasts();
}


report_utils.createVariableSelect = function(){
    /*
     * Returns a JQuery object containing a select list of variable options.
     */
    variables = new Set();
    for (fx in page_data['forecasts']){
        var new_var = page_data['forecasts'][fx].variable;
        if (!current_units ||
            sfa_dash_config.VARIABLE_UNIT_MAP[new_var] == current_units ||
            !sfa_dash_config.VARIABLE_UNIT_MAP[new_var]){
            variables.add(page_data['forecasts'][fx].variable);
        }
    }
    variable_select = $('<select id="variable-select" class="form-control half-width"><option selected value>All Variables</option></select>');
    variables.forEach(function(variable){
        variable_select.append(
            $('<option></option>')
                .html(sfa_dash_config.VARIABLE_NAMES[variable])
                .val(variable));
    });
    return variable_select
}

// insertErrorMessage
// validateReport
report_utils.insertErrorMessage = function(title, msg){
    $('#form-errors').append(
        $('<li></li')
            .addClass('alert alert-danger')
            .html(`<p><b>${title}: </b>${msg}</p>`)
    );
}

report_utils.validateReport = function(){
    /*
     * Callback before the report form is submitted. Any js validation should
     * occur here.
     */
    // remove any existing errors
    $('#form-errors').empty();
    var errors = 0;
    // assert at least one pair was selected.
    if ($('.object-pair').length == 0){
        insertErrorMessage(
            "Analysis Pairs",
            "Must specify at least one Observation, Forecast pair.");
        errors++;
    }
    if (errors){
        return false;
    }
}

// registerDatetimeValidator
report_utils.registerDatetimeValidator = function(input_name){
    /*
     * Applies a regex validator to ensure ISO8601 compliance. This is however, very strict. We
     * will need a better solution.
     */
    $(`[name="${input_name}"]`).keyup(function (){
        if($(`[name="${input_name}"]`).val().match(
              /(\d{4})-(\d{2})-(\d{2})T(\d{2})\:(\d{2})\Z/
        )) {
              $(`[name="${input_name}"]`)[0].setCustomValidity("");
        } else {
              $(`[name="${input_name}"]`)[0].setCustomValidity('Please enter a datetime in the format "YYYY-MM-DDTHH:MMZ');
        }
    });
}

// searchSelect
report_utils.searchSelect = function(inputSelector, selectSelector, offset=0){
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

report_utils.applyFxDependentFilters = function(){
    filterObservations();
    filterAggregates();
    filterReferenceForecasts();
}

// newSelector
report_utils.newSelector = function(field_name, depends_on=null, required=true){
    /*
     * Returns a JQuery object containing labels and select elements for appending options to.
     * Initializes with one default and one optional select option:
     *     Always adds an option containing "No matching <field_Type>s
     *     If depends_on is provided, inserts a "Please select a <depends_on> option>
     */
    var field_type = field_name.toLowerCase().replace(/ /g, '-');
    return $(`<div class="form-element full-width ${field_type}-select-wrapper">
                <label>Select a ${field_name} ${required ? "" : "(Optional)"}</label>
                  <div class="report-field-filters"><input id="${field_type}-option-search" class="form-control half-width" placeholder="Search by ${field_name} name"/></div><br>
                <div class="input-wrapper">
                  <select id="${field_type}-select" class="form-control ${field_type}-field" name="${field_type}-select" size="5">
                  ${depends_on ? `<option id="no-${field_type}-${depends_on}-selection" disabled> Please select a ${depends_on}.</option>` : ""}
                  <option id="no-${field_type}s" disabled hidden>No matching ${field_name}s</option>
                </select>
                </div>
              </div>`);
}

//
// deadbandSelector
//
// parseDeadband
report_utils.deadbandSelector = function(){
    /*
     * Create a radio button and text input for selecting an uncertainty
     * deadband
     */
    var deadbandSelect= $(
        `<div><b>Uncertainty:</b><br>
         <input type="radio" name="deadband-select" value="null" checked> Ignore uncertainty<br>
         <input type="radio" name="deadband-select" value="observation_uncertainty"> Set deadband to observation uncertainty: <span id="selected-obs-uncertainty">No observation selected</span><br>
         <input type="radio" name="deadband-select" value="user_supplied"> Set deadband to:
         <input id="custom-deadband" type="number" step="any" min=0.0 max=100.0 name="deadband-value"> &percnt;<br></div>`);
    // deadbandSelect.find('[name="deadband-value"]')[0].setCustomValidity(
    //     "Must be a value from 0.0 to 100.0");
    var db_wrapper = $('<div class="form-element full-width deadband-select-wrapper"></div>')
    db_wrapper.append(deadbandSelect);
    return db_wrapper;
}


report_utils.parseDeadband = function(value=null){
    /*
     * Parses the deadband widgets into a readable display value, and a
     * valid string value.
     */
    if(!value){
        var source = $('[name="deadband-select"]:checked').val();
        if (source == "null"){
            return ["Ignore uncertainty", "null"]
        } else if (source == "user_supplied"){
            var val = $('[name="deadband-value"]').val();
            if(!$('[name="deadband-value"]')[0].reportValidity()){
                throw 'Deadband out of range';
            }
        } else if (source == "observation_uncertainty"){
            var obs_id = $('#observation-select').val();
            var obs = report_utils.searchObjects("observations", obs_id);
            if(obs){
                var val = obs['uncertainty']
            }
        }
    }else{
        var val = value;
    }
    var str_val = `${val}&percnt;`
    return [str_val, val];
}


report_utils.constant_value_label = function(forecast, value){
    let units = report_utils.determine_forecast_units(forecast);
    if(units == '%'){
        return `Prob( x ) = ${value} ${units}`;
    } else {
       return `Prob( x <= ${value} ${units} )`;
    }
}

report_utils.determine_forecast_units = function(forecast){
    var units = '%';
    if (!forecast.hasOwnProperty('axis') || forecast['axis'] == 'y'){
        units = sfa_dash_config.VARIABLE_UNIT_MAP[forecast['variable']];
    }
    return units;
}
