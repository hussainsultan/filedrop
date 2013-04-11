var r = new Resumable({
    target: '/upload'
});

r.assignBrowse($('.browse'));
r.assignDrop($('.droptarget'));

r.on('fileAdded', function(file){
    $('.upload').hide();

    // Add file
    var $file = $('<p>' + file.fileName + ' (' + file.size +' bytes)</p>');
    $('.progressarea').prepend($file);

    $('.progressarea').show();

    // Begin upload
    r.upload();
});

r.on('progress', function() {
    $('progress').attr('value', r.progress()*100);
    $('.progressarea .percentage').html(r.progress()*100 + '%');
});

r.on('fileError', function(file, message) {
    $('.progressarea .error').show();
    $('progress').hide();
});
