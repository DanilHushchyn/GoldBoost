$(document).ready(function() {
    let images = $('input[type="file"]')
    images.attr('accept', '.svg,.png,.jpeg,.jpg,.webp')
    $(images).on('change', function () {
        if (this.files[0].size > 1000000) {
            alert('File size have to be not more than 1MB')
            $(this).val(null)
            $(this).after(images)
            this.files = []
            return false
        }
    });
})