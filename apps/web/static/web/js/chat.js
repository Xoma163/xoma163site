$('input[name="command"]').on('keypress', function (e) {
    if (e.which == 13) {
        sendCommand();
    }
});


function sendCommand() {
    let command = $('input[name="command"]').val();
    console.log(command);


    $.ajax({
        url: '/api/',
        headers: {
            'Client-Id': 'ANONYMOUS',
        },
        method: 'GET',
        dataType: 'json',
        data: {
            msg: command,
            send: false
        },
        success: function (data, status) {
            console.log(data, status);
            if (status === "success") {
                $('textarea[name="result"]').val(data['res']);

            } else {
                console.log(data, status)
            }
        }
    });
}