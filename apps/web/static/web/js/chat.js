function sendCommand() {
    let CSRFTOKEN = $("input[name='csrfmiddlewaretoken']").val();

    let command = $('input[name="command"]').val();
    console.log(command);
    $.post(`/api/`,
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            msg: command,
            send: false
        },
        function (data, status) {
            if (status === "success") {
                $('textarea[name="result"]').val(data['res']);
            }
        })
}