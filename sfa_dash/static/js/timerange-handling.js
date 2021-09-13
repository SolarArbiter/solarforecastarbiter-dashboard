/*
 * Contains modified code from Solar Performance Insight
 *  dashboard/src/components/jobs/parameters/DatetimeField.vue
 *
 * See LICENSES/SOLARPERFORMANCEINSIGHT_LICENSE
 *
 *  The MAX_DATA_RANGE_DAYS and MAX_PLOT_DATAPOINTS variables are expected to
 * exist as global variables injected by flask.
 */

function ParseStartEnd(){
    // Parse all inputs and place values into hidden fields if applicable
    const start = parseAndValidateStart();
    if (start) {
        $('[name=start]').val(start.toISO());
    } else {
        $('[name=start]').val("");
    }
    const end = parseAndValidateEnd();
    if (end) {
        $('[name=end]').val(end.toISO());
    } else {
        $('[name=end]').val("");
    }
}

function insertWarning(title, msg){
    $('#form-errors').append(`<li class="alert alert-danger"><p><b>${title}: </b>${msg}</p></li>`);
}

function setDatetimeError(startOrEnd, error) {
    const errorContainer = $(`#datetime-${startOrEnd}-errors`);
    if (error) {
        if (startOrEnd == "start") {
            errorContainer.text("Start: " + error);
        } else {
            errorContainer.text("End: " + error);
        }
        errorContainer.addClass(["alert", "alert-danger"]);
    } else {
        errorContainer.removeClass(["alert", "alert-danger"]);
        errorContainer.text("");
    }
}

function validateAndParseDatetimes(){
    /* Enable or disable form submission, plot range adjustment, and data download.
     */
    $('#form-errors').empty()
    const start = parseAndValidateStart();
    const end = parseAndValidateEnd();
    if (start && end) {
        let miliseconds = end.diff(start);
        const days = miliseconds / (1000 * 60 * 60 * 24);
        if (days > 0){
            // Check for plot range button, if exists not a report form.
            if ($('#plot-range-adjust-submit').length) {
                // limit maximum amount of data to download
                if (days > sfa_dash_config.MAX_DATA_RANGE_DAYS){
                    // disable download and plot update
                    $('#download-submit').attr('disabled', true);
                    $('#plot-range-adjust-submit').attr('disabled', true);
                    insertWarning(
                        'Maximum timerange exceeded',
                        'Maximum of one year of data may be requested at once.'
                    );
                } else {
                    // enable download
                    $('#download-submit').removeAttr('disabled');
                    $('#plot-range-adjust-submit').removeAttr('disabled');
                    // check if within limits for plotting
                    if (typeof metadata !== 'undefined' && metadata.hasOwnProperty('interval_length')){
                        var interval_length = parseInt(metadata['interval_length']);
                    } else {
                        var interval_length = 1;
                    }
                    var intervals = miliseconds / (interval_length * 1000 * 60);

                    if (intervals > sfa_dash_config.MAX_PLOT_DATAPOINTS){
                        $('#plot-range-adjust-submit').attr('disabled', true);
                        insertWarning(
                            'Plotting disabled',
                            `Maximum plottable points exceeded. Timerange includes 
                            ${intervals} data points and the maximum is 
                            ${sfa_dash_config.MAX_PLOT_DATAPOINTS}.`);
                    } else {
                        $('#plot-range-adjust-submit').removeAttr('disabled');
                    }
                }
            }
            // Insert values into hidden start/end input
            ParseStartEnd();
        } else {
            insertWarning('Time range', 'Start must be before end.');
            $('#plot-range-adjust-submit').attr('disabled', true);
            $('#download-submit').attr('disabled', true);
        }
    } else {
        $('#download-submit').attr('disabled', true);
        $('#plot-range-adjust-submit').attr('disabled', true);
    }
}

function getStartValue() {
    const year = $('[name="start year"]').val();
    const month = $('[name="start month"]').val();
    const day = $('[name="start day"]').val();
    const hour = $('[name="start hour"]').val();
    const minute= $('[name="start minute"]').val();

    if (year && month && day && hour && minute) {
        let timezoneInput = $('select[name=timezone]').val();
        let timezone = timezoneInput ? timezoneInput : "UTC";

        return luxon.DateTime.fromObject({
           year: year,
           month: month,
           day: day,
           hour: hour,
           minute: minute,
        },{
           zone: timezone
        });
    } else {
        return null;
    }
}

function getEndValue() {
    const year = $('[name="end year"]').val();
    const month = $('[name="end month"]').val();
    const day = $('[name="end day"]').val();
    const hour = $('[name="end hour"]').val();
    const minute = $('[name="end minute"]').val();

    if (year && month && day && hour && minute) {
        let timezoneInput = $('select[name=timezone]').val();
        let timezone = timezoneInput ? timezoneInput : "UTC";

        return luxon.DateTime.fromObject({
            year: year,
            month: month,
            day: day,
            hour: hour,
            minute: minute,
        },{
            zone: timezone
        });
    } else {
        return null;
    }
}

function getDateValues(){
    /* Returns the current start and end values as Date objects */
    const start = parseAndValidateStart();
    const end = parseAndValidateEnd();
    return [start, end]
}

function initDatetimeValues() {
    // check hidden elements for values filled by python and pre-fill.
    let start = $("[name=start]").val();
    let end = $("[name=end]").val();
    let startObject;
    let endObject;
    let timezone = $('select[name=timezone]').val();
    if (start != "") {
        try {
          startObject = luxon.DateTime.fromISO(start, {zone: "UTC"});
        } catch {
          console.error("Could not parse start time: ", start);
        }
    }
    if (end != "") {
        try {
          endObject = luxon.DateTime.fromISO(end, {zone: "UTC"});
        } catch {
          console.error("Could not parse end time: ", end);
        }
    }
    if (startObject) {
        if (timezone) {
            startObject = startObject.setZone(timezone);
        }
        $('[name="start year"]').val(startObject.year);
        $('[name="start month"]').val(startObject.month);
        $('[name="start day"]').val(startObject.day);
        $('[name="start hour"]').val(startObject.hour);
        $('[name="start minute"]').val(startObject.minute);
    }
    if (endObject) {
        if (timezone) {
            endObject = endObject.setZone(timezone);
        }
        $('[name="end year"]').val(endObject.year);
        $('[name="end month"]').val(endObject.month);
        $('[name="end day"]').val(endObject.day);
        $('[name="end hour"]').val(endObject.hour);
        $('[name="end minute"]').val(endObject.minute);
    }
}

function parseAndValidateStart() {
    let start;
    const errorContainer = $("#datetime-start-errors");
    try {
      start = getStartValue();
    } catch(error) {
      setDatetimeError("start", "Invalid date or time information.");
      return null;
    }
    if (start && !start.isValid) {
      setDatetimeError("start", cleanError(start.invalid.explanation));
      return null;
    } else {
      setDatetimeError("start");
      return start;
    }
}

function parseAndValidateEnd() {
    let end;
    try {
      end = getEndValue();
    } catch {
      setDatetimeError("end", "Invalid date or time information.");
      return null;
    }
    if (end && !end.isValid) {
      setDatetimeError("end", cleanError(end.invalid.explanation));
      return null;
    } else {
      setDatetimeError("end");
      return end;
    }
}

function cleanError(errorMessage) {
    return errorMessage.replace(/\(of type .*\)/, "");
}

$(document).ready(function(){
    initDatetimeValues();
    $('[name="start year"]').change(validateAndParseDatetimes);
    $('[name="start month"]').change(validateAndParseDatetimes);
    $('[name="start day"]').change(validateAndParseDatetimes);
    $('[name="start hour"]').change(validateAndParseDatetimes);
    $('[name="start minute"]').change(validateAndParseDatetimes);

    $('[name="end year"]').change(validateAndParseDatetimes);
    $('[name="end month"]').change(validateAndParseDatetimes);
    $('[name="end day"]').change(validateAndParseDatetimes);
    $('[name="end hour"]').change(validateAndParseDatetimes);
    $('[name="end minute"]').change(validateAndParseDatetimes);
});
