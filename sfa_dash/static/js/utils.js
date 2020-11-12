$(document).ready(function(){
    if ($("#object_uuid").length) {
        // Add a button link to copy uuids
        $("#object_uuid").after(
            $("<br/>"),
            $("<a>")
                .attr("role", "button")
                .css("color", "#007bff")
                .text("Copy UUID")
                .click(function(){
                    window.getSelection().removeAllRanges();
                    let uuid_container = document.getElementById("object_uuid");
                    let range = document.createRange();
                    range.selectNode(uuid_container);
                    window.getSelection().addRange(range);
                    document.execCommand("copy");
                })
        );
    }

});
