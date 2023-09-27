window.onload = function() {

    $('#word-index, #add-cancel').click(function() {
        $('#word-add').removeClass('side-active')
        $('#word-index').addClass('side-active')
        $('#word-add-form').hide()
    })

    $('#word-add').click(function() {
        $('#word-index').removeClass('side-active')
        $(this).addClass('side-active')
        $('#word-add-form').show()
    })

    $('#word-add-form').submit(function() {
        let word = $('#word').val()
        let meaning = $('#meaning').val()

        $.ajax({
            url: '/word',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'word': word,
                'meaning': meaning
            }),
            contentType: 'application/json',
            success: () => location.reload(),
            error: (err) => console.log(err)
        })
    })

    $('.delete').click(function() {
        let word_id = $(this).attr('id')

        $.ajax({
            url: '/word/' + word_id + '/delete',
            type: 'POST',
            success: () => { location.reload() },
            error:(err) => { console.log(err) }
        })
    })

}