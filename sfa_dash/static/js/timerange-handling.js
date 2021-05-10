/* The MAX_DATA_RANGE_DAYS and MAX_PLOT_DATAPOINTS variables are expected to
 * exist as global variables injected by flask.
 */
function ParseStartEnd(){
    // Manually parse this string to avoid the implicit tz conversion based on
    // the users browser. We're asking users for UTC so, manually add Z to the end of
    // the dt string.
    start = parseAndValidateStart();
    $('.start').val(start.toISO());
    end = parseAndValidateEnd();
    $('.end').val(end.toISO());
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

function toggleDownloadUpdate(){
    /* Enable or disable download and update graph buttons based on the current
     * selected timerange.
     */
    $('#form-errors').empty()
    const start = parseAndValidateStart();
    const end = parseAndValidateEnd();
    if (start && end) {
        miliseconds = end.diff(start);
        days = miliseconds / (1000 * 60 * 60 * 24);
        if (days > 0){
            // limit maximum amount of data to download
            if (days > sfa_dash_config.MAX_DATA_RANGE_DAYS){
                // disable download and plot update
                $('#download-submit').attr('disabled', true);
                $('#plot-range-adjust-submit').attr('disabled', true);
                $("button[type=submit]").attr('disabled', true);
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
        } else {
            insertWarning('Time range', 'Start must be before end.');
            $('#plot-range-adjust-submit').attr('disabled', true);
            $('#download-submit').attr('disabled', true);
            $("button[type=submit]").attr('disabled', true);
        }
    } else {
        $('#download-submit').attr('disabled', true);
        $('#plot-range-adjust-submit').attr('disabled', true);
        $("button[type=submit]").attr('disabled', true);
    }
}

function getStartValue() {
     const year = $('[name="start year"]').val();
     const month = $('[name="start month"]').val();
     const day = $('[name="start day"]').val();
     const hour = $('[name="start hour"]').val();
     const minute= $('[name="start minute"]').val();

     return luxon.DateTime.fromObject({
        year: year,
        month: month,
        day: day,
        hour: hour,
        minute: minute,
        zone: "UTC"
    });
}

function getEndValue() {
    const year = $('[name="end year"]').val();
    const month = $('[name="end month"]').val();
    const day = $('[name="end day"]').val();
    const hour = $('[name="end hour"]').val();
    const minute = $('[name="end minute"]').val();


    return luxon.DateTime.fromObject({
        year: year,
        month: month,
        day: day,
        hour: hour,
        minute: minute,
        zone: "UTC"
    });
}

function getDateValues(){
    /* Returns the current start and end values as Date objects */
    const start = parseAndValidateStart();
    const end = parseAndValidateEnd();
    return [start, end]
}

function initDatetimeValues() {
    $('[name="start year"]').val();
    $('[name="start month"]').val();
    $('[name="start day"]').val();
    $('[name="start hour"]').val();
    $('[name="start minute"]').val();

    $('[name="end year"]').val();
    $('[name="end month"]').val();
    $('[name="end day"]').val();
    $('[name="end hour"]').val();
    $('[name="end minute"]').val();
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
    if (!start.isValid && start.invalid) {
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
    if (!end.isValid && end.invalid) {
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
    $('[name="start year"]').change(toggleDownloadUpdate);
    $('[name="start month"]').change(toggleDownloadUpdate);
    $('[name="start day"]').change(toggleDownloadUpdate);
    $('[name="start hour"]').change(toggleDownloadUpdate);
    $('[name="start minute"]').change(toggleDownloadUpdate);

    $('[name="end year"]').change(toggleDownloadUpdate);
    $('[name="end month"]').change(toggleDownloadUpdate);
    $('[name="end day"]').change(toggleDownloadUpdate);
    $('[name="end hour"]').change(toggleDownloadUpdate);
    $('[name="end minute"]').change(toggleDownloadUpdate);
});
