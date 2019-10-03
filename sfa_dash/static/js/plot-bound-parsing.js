function ParseStartEnd(){
    // Manually parse this string to avoid the implicit tz conversion based on
    // the users browser. This was causing errors in the different ways the js
    // front end and python backend were handling datetimes
    startYear = $('#start-date').val().slice(0, 4);
    startMonth = $('#start-date').val().slice(5, 7);
    startDay = $('#start-date').val().slice(-2);
    $('#start').val(startYear+'-'+startMonth+'-'+startDay+'T'+$('#start-time').val());

    endYear = $('#end-date').val().slice(0, 4);
    endMonth = $('#end-date').val().slice(5, 7);
    endDay = $('#end-date').val().slice(-2);
    $('#end').val(endYear+'-'+endMonth+'-'+endDay+'T'+$('#end-time').val());
}
$(document).ready(function(){
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('start')){
        start = new Date(urlParams.get('start'))
        day = start.getDate().toString().padStart(2, 0);
        month = (start.getMonth()+1).toString().padStart(2, 0);
        $('#start-date').val(start.getFullYear()+"-"+(month)+"-"+(day));
        hours = start.getHours().toString().padStart(2, 0);
        minutes = start.getMinutes().toString().padStart(2, 0);
        $('#start-time').val(hours+':'+minutes);
    }
    if (urlParams.has('end')){
        end = new Date(urlParams.get('end'))
        day = end.getDate().toString().padStart(2, 0);
        month = (end.getMonth()+1).toString().padStart(2, 0);
        $('#end-date').val(end.getFullYear()+"-"+(month)+"-"+(day));
        hours = end.getHours().toString().padStart(2, 0);
        minutes = end.getMinutes().toString().padStart(2, 0);
        $('#end-time').val(hours+':'+minutes);
    }
})
