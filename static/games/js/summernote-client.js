

$(document).ready(function() {
    let images = $('input[type="file"]')
    images.attr('accept','.svg,.png,.jpeg,.jpg,.webp')
    $(images).on('change', function() {
        var validExtensions = ["jpg","webp","jpeg","svg","png"]
        var file = $(this).val().split('.').pop();
        if (validExtensions.indexOf(file) == -1) {
            alert("Only formats are allowed : "+validExtensions.join(', '));
            $(this).val(null)
            // $(this).after(images)
            // this.files = []
            return false

        }


      if (this.files[0].size>1000000){
          alert('File size have to be not more than 1MB')
          $(this).val(null)
          // $(this).after(images)
          // this.files = []
          return false
      }
    });
    $("[summernote='true']").each(function() {
        console.log('hello123')
        // Do something with each element
        // Do something with each element
        // Do something with each element
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
