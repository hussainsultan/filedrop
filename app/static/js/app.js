/**
 * Utility functions.
 */
var Util = {
    /**
     * Return whether or not the client browser is running on a Mac.
     */
    isMacintosh: function() {
        return navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    },

    /**
     * Format bytes into a human-readable number.
     */
    readablizeBytes: function(bytes) {
        var s = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
        var e = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, e)).toFixed(2) + " " + s[e];
    }
};


/**
 * UploadWidget module: used on the main upload and invite upload pages.
 */
var UploadWidget = {

    // Slug identifier
    slug: null,

    // Resumable obj
    r: new Resumable({
        target: '/api/upload',
        chunkSize: 10*1024*1024,
        maxFiles: 1
    }),

    /**
     * UploadWidget init(): called on the upload page.
     */
    init: function(slug) {

        this.slug = slug;

        _.bindAll(this, 'prepareFileUpload', 'handleFileUpload', 'updateProgress', 'uploadError', 'uploadSuccess', 'uploadStopped');

        // Customise tooltip depending on whether this is a PC or Mac.
        if (Util.isMacintosh()) {
            $('.url input').attr('title', 'Press ⌘-C to copy');
        }

        // Resumable has builtin init functions for easy set up of file
        // browsing and drop targets
        this.r.assignBrowse($('.browse'));
        this.r.assignDrop($('.droptarget'));

        $('.browse').on('click', function() {
            $('input[type="file"]').get(0).click();
            e.preventDefault();
        });

        // Supplement the drop target with our own handlers that change the
        // background colour on hover
        $('.droptarget').on('dragover', function() {
            $(this).addClass('hover');
        });
        $('.droptarget').on('dragleave', function() {
            $(this).removeClass('hover');
        });

        // Set up event handlers
        this.r.on('fileAdded', this.prepareFileUpload);
        this.r.on('progress', this.updateProgress);
        this.r.on('fileError', this.uploadError);
        this.r.on('fileSuccess', this.uploadSuccess);

        this.r.on('fileSuccess', this.uploadStopped);
        this.r.on('fileError', this.uploadStopped);

        $('.url input').on('focus', function(e) {
            $(this).tooltip('show');
        });
        $('.url input').on('blur', function(e) {
            $(this).tooltip('hide');
        });
        $('.url input').on('mouseup', function(e) {
            this.select();
            e.preventDefault();
        });
    },

    /**
     * Carries out pre-upload checks to ensure we've got all we need to upload.
     *
     * To upload, we need a valid slug reserved. The slug is either reserved
     * by an authenticated user (hence bootstrapped into the slug var on the
     * page) or we'll have to request one via the API as part of this method.
     */
    prepareFileUpload: function(file) {

        var callback = this.handleFileUpload;

        // Check if a global slug ID is present
        if (typeof(this.slug) !== 'undefined') {
            callback(file, this.slug);
        } else {
            // Request a valid slug ID when a file is dropped
            $.get('/api/request-slug', function(data) {
                this.slug = data.response.id;
                callback(file, this.slug);
            });
        }
    },

    /**
     * Begins the upload process. Sets up the UI and calls on Resumable.js to
     * upload.
     */
    handleFileUpload: function(file, slug) {
        this.slug = slug;

        // Include slug ID in upload chunks
        this.r.opts.query = {
            'slug': slug
        };

        // Show file name and upload progress
        var $file = $('<p>Uploading <code>' + file.fileName + '</code> (' + Util.readablizeBytes(file.size) + ')</p>');
        $('.filename').prepend($file);

        // Switch tab
        this.showTab('#progress');

        // Begin upload
        this.r.upload();
    },

    /**
     * Event callback. Called when the progress percentage in Resumable.js has
     * changed. This method updates the progress bar percentage.
     */
    updateProgress: function() {
        var percentage = Math.round(this.r.progress()*100) + '%';
        $('.progress-bar').width(percentage);
        $('.percentage').html(percentage);
    },

    /**
     * Event callback. Called when there's an upload error.
     */
    uploadError: function(file, message) {
        // Hide progress bar and show error message instead
        this.showTab('#error');
    },

    /**
     * Event callback: called when the upload completes successfully (all
     * chunks have been uploaded).
     */
    uploadSuccess: function(file) {

        // Generate an A tag and set the href relatively. We can use this to
        // get the FULL URL by reading .href from the browser.
        var link = $('<a/>').attr('href', '/file/' + this.slug);
        $('.url input').val(link.get(0).href);

        this.showTab('#success');

        $('.url input').select();
        $('.url input').focus();
    },

    /**
     * Generic tasks to be performed when an upload is complete (either success
     * or fail).
     *
     * Individual success/fail callbacks are above.
     */
    uploadStopped: function() {
        $('.progress').removeClass('active');
    },

    /**
     * Hide all UI tabs/screens apart from the one specified.
     */
    showTab: function(tab) {
        $('.tab-pane').removeClass('active');
        $(tab).addClass('active');
    }
};


/**
 * InviteWidget module: used on the invite page.
 */
var InviteWidget = {
    init: function() {
        _.bindAll(this, 'createInvite');
        $('.invite-button').on('click', this.createInvite);

        // Customise tooltip depending on whether this is a PC or Mac.
        if (Util.isMacintosh()) {
            $('.url input').attr('title', 'Press ⌘-C to copy');
        }

        $('.url input').on('focus', function(e) {
            $(this).tooltip('show');
        });
        $('.url input').on('blur', function(e) {
            $(this).tooltip('hide');
        });
        $('.url input').on('mouseup', function(e) {
            this.select();
            e.preventDefault();
        });
    },

    createInvite: function() {
        var cb = this.setLink;
        // Request a valid slug ID when a file is dropped
        $.ajax('/api/request-slug', {
            success: function(data) {
                $('.tab-pane').removeClass('active');
                $('#invite-generated').addClass('active');
                cb('.url input', data.response['id']);
            }
        });
    },

    setLink: function(el, slug) {
        $el = $(el);

        // Generate an A tag and set the href relatively. We can use this to
        // get the FULL URL by reading .href from the browser.
        var link = $('<a/>').attr('href', '/invite/' + slug);
        $el.val(link.get(0).href);

        $el.select();
        $el.focus();
    }
};
