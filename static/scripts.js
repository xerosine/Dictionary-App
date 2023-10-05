window.onload = function() {
    $('#modal').modal('show')

    $('#word-index, #add-cancel, #logo-cancel').click(function() {
        $('#word-add, #logo-add').removeClass('side-active')
        $('#word-index').addClass('side-active')
        $('#word-add-form, #logo-add-form').hide()
    })

    //add operation
    $('#word-add').click(function() {
        $('#word-index, #logo-add').removeClass('side-active')
        $(this).addClass('side-active')
        $('#word-add-form').show()
        $('#logo-add-form').hide()
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

    //logo add operation
    $('#logo-add').click(function() {
        $('#word-index, #word-add').removeClass('side-active')
        $(this).addClass('side-active')
        $('#logo-add-form').show()
        $('#word-add-form').hide()
    })

    $('#logo-add-form').submit(function() {
        let data = new FormData()
        data.append('file', $('#logo')[0].files[0])

        $.ajax({
            url: '/add_logo',
            type: 'POST',
            enctype: 'multipart/form-data',
            data: data,
            processData: false,
            contentType: false,
            success: () => location.reload(),
            error: (err) => console.log(err)
        })
    })

    //delete operation
    $('.delete').click(function() {
        let word_id = $(this).attr('id')

        $.ajax({
            url: '/word/' + word_id + '/delete',
            type: 'POST',
            success: () => { location.reload() },
            error:(err) => { console.log(err) }
        })
    })

    //edit operation
    var word, meaning

    $('.edit').click(function() {
        let parent = $(this).parents('tr')
        parent.find('.edit-word, .edit-meaning').show()
        parent.find('.dict-word, .dict-meaning').hide()
        parent.find('.td-submit, .td-cancel').show()
        parent.find('.edit, .delete').parent().hide()
        word = parent.find('input').val()
        meaning = parent.find('textarea').val()
    })

    $('.cancel').click(function() {
        let parent = $(this).parents('tr')
        parent.find('.edit-word, .edit-meaning').hide()
        parent.find('.dict-word, .dict-meaning').show()
        parent.find('.td-submit, .td-cancel').hide()
        parent.find('.edit, .delete').parent().show()
        parent.find('input').val(word)
        parent.find('textarea').val(meaning)
    })

    $('.update-form').submit(function() {
        let parent = $(this).parents('tr')
        let newWord = parent.find('input').val()
        let newMeaning = parent.find('textarea').val()
        let word_id = parent.find('.submit').attr('id')

        $.ajax({
            url: '/word/' + word_id + '/edit',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'word': newWord,
                'meaning': newMeaning
            }),
            contentType: 'application/json',
            success: () => { location.reload() },
            error: (err) => { console.log(err) }
        })
    })

}