function sendCommand() {
    let command = $("input[name=\"command\"]").val();
    $.ajax({
        url: "/api/",
        headers: {
            "Client-Id": "ANONYMOUS",
        },
        method: "GET",
        dataType: "json",
        data: {
            msg: command,
            send: false
        },
        success: function (data, status) {
            if (status === "success") {
                $("textarea[name=\"result\"]").val(data["res"]);

            }
        }
    });
}

$("input[name=\"command\"]").on("keypress", function (e) {
    if (e.which === 13) {
        sendCommand();
    }
});
