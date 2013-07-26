var r = new Resumable({
    target: '/upload',
    chunkSize: 10*1024*1024
});

var slug_id;

r.assignBrowse($('.browse'));
r.assignDrop($('.droptarget'));

r.on('fileAdded', function(file) {

    $.get('/api/request-slug', function(data) {

        slug_id = data.response.id;

        // Reserve slug ID
        r.opts.query = {
            'slug': data.response.id
        };

        $('.upload').hide();

        // Add file
        var $file = $('<p>' + file.fileName + ' (' + file.size +' bytes)</p>');
        $('.progressarea').prepend($file);

        $('.progressarea').show();

        // Begin upload
        r.upload();

    });
});

r.on('fileRetry', function(file) {
    file.abort();
});

r.on('progress', function() {
    $('progress').attr('value', r.progress()*100);
    $('.progressarea .percentage').html(r.progress()*100 + '%');
});

r.on('fileError', function(file, message) {
    $('.progressarea .error').show();
    $('progress').hide();
});

r.on('fileSuccess', function(file) {
    var link = $('<a/>').attr('href', '/file/' + slug_id);
    $('.url').html('URL: ' + link.get(0).href);
});
