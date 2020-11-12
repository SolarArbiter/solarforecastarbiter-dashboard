$(document).ready(function() {
    $('.report-details-expander').click(function(){
        // Close any other open report details
        $('div.report-metadata-popup[hidden!=hidden]').attr('hidden', true);
        $(this).next().removeAttr('hidden');
    });
    $('.report-details-closer').click(function(){
        $(this).parent().attr('hidden', true);
    });
})
$(document).click(function(event){
    let target = $(event.target);
    // first check that the user didn't click the expander button
    if (!target.closest('.report-details-expander').length){
        // if there is no popup in the target, close all popups.
        if (!target.closest('div.report-metadata-popup').length){
            $('div.report-metadata-popup[hidden!=hidden]').attr('hidden', true);
        }
    }

});
