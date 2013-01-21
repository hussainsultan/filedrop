var r = new Resumable({
    target: '/upload'
});

r.assignBrowse($('button.browse'));
r.assignDrop($('.droptarget'));

r.on('fileAdded', function(file){
    $('div.upload').hide();

    // Add file
    var $file = $('<p>' + file.fileName + ' (' + file.size +' bytes)</p>');
    $('div#progress').prepend($file);

    $('div#progress').show();

    // Begin upload
    //r.upload();
});

r.on('progress', function() {
    $('div#progress progress').attr('value', r.progress()*100);
    $('#progress .percentage').html(r.progress()*100 + '%');
});
