

$(document).ready(function() {
    $("[summernote='true']").each(function() {
        console.log('hello123')
        // Do something with each element
        $(this).summernote({
            lang: 'ru-RU',
            height: "200",
            width: "400",
                toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
        ['fontname', ['fontname']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['insert', ['link', 'picture', 'video']],
        ['view', ['codeview']],
    ]
        });
        let prevElement =  $(this).prev('.border');
        $(this).addClass('text-gray-500')
        $('.note-editing-area').addClass('text-gray-500')
        prevElement.hide()

    });
});
