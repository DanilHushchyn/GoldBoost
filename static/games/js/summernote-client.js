

$(document).ready(function() {
    $("[summernote='true']").each(function() {
        console.log('hello')
        // Do something with each element
        $(this).summernote({
           lang: 'ru-RU',
            height: "200",
        });
        let prevElement =  $(this).prev('.border');
        prevElement.hide()

    });
});
