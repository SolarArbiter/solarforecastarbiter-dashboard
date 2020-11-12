$(document).ready(function(){
    // Add a "Copy UUID" to clipboard button
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
    // If metadata is defined and the metadata display block exists, create
    // a metadata download button
    if (typeof metadata !== 'undefined' && $('.data-metadata')) {
        function downloadMetadata(){
            const filename = metadata.name.replace(/ /g, '_') + '.json';
            const contents = new Blob(
                [JSON.stringify(metadata, null, 2)],
                { type: 'application/json;charset=utf-8;'});

            if (navigator.msSaveBlob) {
                navigator.msSaveBlob(contents, filename)
            } else {
                const link = document.createElement('a')
                link.href = URL.createObjectURL(contents)
                link.download = filename
                link.target = '_blank'
                link.style.visibility = 'hidden'
                link.dispatchEvent(new MouseEvent('click'))
                link.remove();
            }
        }
        let download_link = $('<a>')
            .text('Download Metadata')
            .attr("role", "button")
            .css("color", "#007bff")
            .css("position", "absolute")
            .css("right", "1em")
            .css("top", "1em")
            .click(downloadMetadata);
        $('.data-metadata').append(download_link);
    }

});
