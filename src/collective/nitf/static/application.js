/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */

/*jslint nomen: true */
/*global $ */

(function ($) {
    $(document).ready(function() {
        'use strict';

        // Initialize the jQuery File Upload widget:

        //$('#fileupload').fileupload({uploadTemplate: upload_tmpl, downloadTemplate: download_tmpl, autoUpload: false,});

/*
 * AQUANTUM Demo Application
 * http://aquantum-demo.appspot.com/file-upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $ */

        var Application = function (settings) {
            'use strict';

            // Generic:
            // --------
            var upload_tmpl =
                '<tr class="template-upload{{if error}} ui-state-error{{/if}}"><td class="preview"></td><td class="name">${name}</td><td class="size">${sizef}</td>{{if error}}<td class="error" colspan="2">Error:{{if error === "maxFileSize"}}File is too big{{else error === "minFileSize"}}File is too small{{else error === "acceptFileTypes"}}Filetype not allowed{{else error === "maxNumberOfFiles"}}Max number of files exceeded{{else}}${error}{{/if}}</td>{{else}}<td class="progress"><div></div></td><td class="start"><button>Start</button></td>{{/if}}<td class="cancel"><button>Cancel</button></td></tr>';

            var download_tmpl =
                '<tr class="template-download{{if error}} ui-state-error{{/if}}">{{if error}}<td></td><td class="name">${name}</td><td class="size">${sizef}</td><td class="error" colspan="2">Error:{{if error === 1}}File exceeds upload_max_filesize (php.ini directive){{else error === 2}}File exceeds MAX_FILE_SIZE (HTML form directive){{else error === 3}}File was only partially uploaded{{else error === 4}}No File was uploaded{{else error === 5}}Missing a temporary folder{{else error === 6}}Failed to write file to disk{{else error === 7}}File upload stopped by extension{{else error === "maxFileSize"}}File is too big{{else error === "minFileSize"}}File is too small{{else error === "acceptFileTypes"}}Filetype not allowed{{else error === "maxNumberOfFiles"}}Max number of files exceeded{{else error === "uploadedBytes"}}Uploaded bytes exceed file size{{else error === "emptyResult"}}Empty file upload result{{else}}${error}{{/if}}</td>{{else}}<td class="preview">{{if thumbnail_url}}<a href="${url}" target="_blank"><img src="${thumbnail_url}"></a>{{/if}}</td><td class="name"><a href="${url}"{{if thumbnail_url}} target="_blank"{{/if}}>${name}</a></td><td class="size">${sizef}</td><td colspan="2"></td>{{/if}}<td class="delete"><button data-type="${delete_type}" data-url="${delete_url}">Delete</button></td></tr>';

            $('html:first').removeClass('no-js');

            // Initialize imagegallery plugin:
            //$('a[rel=gallery]').imagegallery();
            // File Upload:
            // ------------
            //$('#fileupload').fileupload({uploadTemplate: upload_tmpl, downloadTemplate: download_tmpl, autoUpload: false,});
            $('#fileupload').fileupload({
                maxFileSize: settings.max_file_size,
                uploadTemplate: upload_tmpl,
                downloadTemplate: download_tmpl,
                autoUpload: false,
                authenticityTokenName: settings.authenticity_token &&
                    settings.authenticity_token.name
            });

            /*
            $('#radio').buttonset();
            $('#radio input').click(function (e) {
                $('#fileupload').fileupload(
                    'option',
                    'autoUpload',
                    $(this).val() === 'auto'
                );
            });
            */

            // Create jQuery UI buttons for existing files:
            $('#fileupload .files .delete button').button({
                text: false,
                icons: {primary: 'ui-icon-trash'}
            });
            /*
            // Enable drag-to-desktop for existing files:
            $('#fileupload .files .template-download a').each(
                $.blueimpUIX.fileupload.prototype._enableDragToDesktop
            );*/
            //$.getJSON($('#fileupload form').prop('action'), function (files) {
            $.getJSON('./api', function (files) {
                var fu = $('#fileupload').data('fileupload');
                fu._adjustMaxNumberOfFiles(-files.length);
                fu._renderDownload(files)
                    .appendTo($('#fileupload .files'))
                    .fadeIn(function () {
                        // Fix for IE7 and lower:
                        $(this).show();
                    });
            });

            // Open download dialogs via iframes,
            // to prevent aborting current uploads:
            $('#fileupload .files a:not([rel^=gallery])').live('click', function (e) {
                e.preventDefault();
                $('<iframe style="display:none;"></iframe>')
                    .prop('src', this.href)
                    .appendTo('body');
            });

            // Home page:
            // ----------
            $('#home .demos a').button();
            
            // Login page:
            // -----------
            $('#login button.openid-provider').button({icons: {primary: 'icon-openid'}});
            $('#login #openid-provider-generic button, #logout-link').button();

        };
        Application({"max_file_size":5000000,"authenticity_token":{"name":"request_authenticity_token","value":"v1GPBqU-ep4iSmnP2x40HmlnP2EW7r5h"}});
        // Load existing files:
        /*
        // Open download dialogs via iframes,
        // to prevent aborting current uploads:
        $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
            e.preventDefault();
            $('<iframe style="display:none;"></iframe>')
                .prop('src', this.href)
                .appendTo('body');
        });
*/
    });
})(jQuery);
