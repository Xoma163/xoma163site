let SESSION_ID;
let CSRFTOKEN;
$(document).ready(function () {
    console.log("ready!");

    $("#order tr:not(:last) input,#order tr:not(:last) select").change(function (event) {
        saveRow(this)
    });

    SESSION_ID = $("input[name='session_id']").val();
    CSRFTOKEN = $("input[name='csrfmiddlewaretoken']").val()
    // let csrftoken = getCookie('csrftoken');
});


function addRow() {
    let order = $("#order tbody");
    // Берём предпоследний!
    let preLastRow = $("#order tbody tr:nth-last-child(-2n+2)");
    let lastRow = $("#order tbody tr:last");
    let lastRowClone = $(lastRow).clone();
    let realLastRow = $(lastRow).clone();

    let product = {
        name: $(lastRow).find("input[name='name']").val(),
        count: $(lastRow).find("input[name='count']").val(),
        tare_id: $(lastRow).find("select[name='tare']").val(),
        price: $(lastRow).find("input[name='price']").val(),
        user_id: $(lastRow).find("select[name='user']").val(),
        is_bought: $(lastRow).find("input[name='is_bought']").prop("checked")
    };

    $.post("add_row",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
            product: JSON.stringify(product)
        },
        function (data, status) {
            let oldRowNum = 1;
            if ($(preLastRow).length) {
                oldRowNum = parseInt($(preLastRow[0].cells[0]).html()) + 1;
            }
            $(lastRowClone[0].cells[0]).html(`${oldRowNum}<input type="hidden" value="${data.id}" name="id">`);

            // Копирование селектов
            var originalSelects = $(lastRow[0].cells[3]).find('select');
            $(lastRowClone[0].cells[3]).find('select').each(function (index, item) {
                $(item).val(originalSelects.eq(index).val());
            });
            var originalSelects = $(lastRow[0].cells[5]).find('select');
            $(lastRowClone[0].cells[5]).find('select').each(function (index, item) {
                $(item).val(originalSelects.eq(index).val());
            });

            $(lastRowClone[0].cells[7]).empty().append(`<i class="fa fa-times" onclick="delRow(this)" style="color:red;cursor:pointer;"></i>`);
            $(realLastRow[0].cells[1]).find("input").val("");
            $(realLastRow[0].cells[2]).find("input").val("0");
            $(realLastRow[0].cells[3]).find("select option:first").prop("selected", true);
            $(realLastRow[0].cells[4]).find("input").val("0");
            $(realLastRow[0].cells[6]).find("input").prop("checked", false);

            $(lastRow).remove();
            order.append(lastRowClone);
            order.append(realLastRow);

            // $("#order input:last-of-type,#order select:last-of-type").change(function (event) {
            $("#order tr:nth-last-child(2) input,#order tr:nth-last-child(2) select").change(function (event) {
                saveRow(this)
            });
        });
}

function delRow(_this) {
    let tr = $(_this).parents("tr");
    let id = $(tr).find("input[name='id']").val();

    $.post("del_row",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
            id: id
        },
        function (data, status) {
            $(tr).remove();
        })
}

function saveRow(_this) {
    let tr = $(_this).parents("tr");
    let order = {
        product: {
            id: $(tr).find("input[name='id']").val(),
            name: $(tr).find("input[name='name']").val(),
            count: $(tr).find("input[name='count']").val(),
            tare_id: $(tr).find("select[name='tare']").val(),
            price: $(tr).find("input[name='price']").val(),
            user_id: $(tr).find("select[name='user']").val(),
            is_bought: $(tr).find("input[name='is_bought']").prop("checked")
        }
    };

    let orders = [order];
    $.post("save_rows",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            // csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
            session_id: SESSION_ID,
            orders: JSON.stringify(orders)
        },
        function (data, status) {
        })
}

// function saveRows() {
//     let session_id = 1;
//     let csrftoken = getCookie('csrftoken');
//
//     let trs = $("#order tbody tr");
//     let orders = [];
//     for (let i = 0; i < trs.length; i++) {
//         let tr = trs[i];
//         let order = {
//             product: {
//                 id: $(tr).find("input[name='id']").val(),
//                 name: $(tr).find("input[name='name']").val(),
//                 count: $(tr).find("input[name='count']").val(),
//                 tare_id: $(tr).find("select[name='tare']").val(),
//                 price: $(tr).find("input[name='price']").val(),
//                 user_id: $(tr).find("select[name='user']").val(),
//                 is_bought: $(tr).find("input[name='is_bought']").prop("checked")
//             }
//         };
//         orders.push(order)
//     }
//     $.post("save_rows",
//         {
//             csrfmiddlewaretoken: csrftoken,
//             session_id: session_id,
//             orders: JSON.stringify(orders)
//         },
//         function (data, status) {
//         })
// }

function addUser() {
    let users = $("#users tbody");
    let lastRow = $("#users tbody tr:last");
    let lastRowClone = $(lastRow).clone();
    $(lastRowClone[0].cells[0]).find("input").val("");

    let newUserName = $(lastRow).find("input[name='name']").val();
    // let newUserName = $("#modal-settings input[name='newName']");
    $.post("add_user",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
            name: newUserName
        },
        function (data, status) {
            $(lastRow).remove();

            console.log(data);
            $(users).append(`
              <tr class="text-center">
                <td class="form-group">
                  <input type="hidden" name="id" value="${data.id}">
                  <input class="form-control"
                         type="text"
                         value="${newUserName}"
                         name="name"
                         autocomplete="off">
                </td>
                <td class="form-group del-elem d-flex justify-content-center flex-column">
                  <i class="fa fa-times" onclick="delUser(this)" style="color:red;cursor:pointer;"></i>
                </td>
              </tr>
`);
            users.append(lastRowClone);

            // $("select[name='user']").append(`<option value="${data.id}">${newUserName}</option>`)
            // $(newUserName).val('');
        });


}

function delUser(_this) {
    let tr = $(_this).parents("tr");
    let id = $(tr).find("input[name='id']").val();

    $.post("del_user",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
            id: id
        },
        function (data, status) {
            $(tr).remove();
            $(`select[name='user'] option[value=${id}]`).remove();

        })
}

function saveUser(_this) {

    let tr = $(_this).parents("tr");
    let user = {
        id: $(tr).find("input[name='id']").val(),
        name: $(tr).find("input[name='name']").val(),
    };

    let users = [user];
    $.post("save_users",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
            users: JSON.stringify(users)
        },
        function (data, status) {
            $(`select[name='user'] option[value=${user.id}]`).html(user.name);
        })
}


function getCalculateData() {
    let users = $("select[name='user']:not(:last)");
    for (let i = 0; i < users.length; i++) {
        if ($(users[i]).val() === "None") {
            alert("Не все значения 'кто' проставлены, рассчёт невозможен");
            return
        }
    }
    $.post("get_calculate",
        {
            csrfmiddlewaretoken: CSRFTOKEN,
            session_id: SESSION_ID,
        },
        function (data, status) {
            let modelBody = $("#modal-calculation .modal-body");
            modelBody.empty();
            for (let i = 0; i < data.result.length; i++)
                modelBody.append(`<div>${data.result[i]}</div>`);
            $('#modal-calculation').modal('show');
        });

}

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }