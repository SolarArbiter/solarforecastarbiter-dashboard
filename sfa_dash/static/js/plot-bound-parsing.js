function ParseStartEnd(){
    // Slice until 16th character to drop implicit javascript utcoffset
    $('#start').val(new Date($('#start-date').val() + ' ' + $('#start-time').val()).toISOString().slice(0,16));
    $('#end').val(new Date($('#end-date').val() + ' ' + $('#end-time').val()).toISOString().slice(0,16));
}
$(document).ready(function(){
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('start')){
        start = new Date(urlParams.get('start'))
        day = start.getDate().toString().padStart(2, 0);
        month = start.getMonth().toString().padStart(2, 0);
        $('#start-date').val(start.getFullYear()+"-"+(month)+"-"+(day));
        hours = start.getHours().toString().padStart(2, 0);
        minutes = start.getMinutes().toString().padStart(2, 0);
        $('#start-time').val(hours+':'+minutes);
    }
    if (urlParams.has('end')){
        end = new Date(urlParams.get('end'))
        day = end.getDate().toString().padStart(2, 0);
        month = end.getMonth().toString().padStart(2, 0);
        $('#end-date').val(end.getFullYear()+"-"+(month)+"-"+(day));
        hours = end.getHours().toString().padStart(2, 0);
        minutes = end.getMinutes().toString().padStart(2, 0);
        $('#end-time').val(hours+':'+minutes);
    }
})
