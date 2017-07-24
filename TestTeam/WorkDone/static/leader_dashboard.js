wd_token = ""
function get_work(work_id) {
    var ret = null
    $.ajax({
        type: "GET",
        url: "/workdone/getWorkById/",
        dataType: "json",
        contentType: "application/json",
        async: false,
        data: { id: work_id, token: '516c7e36e65af02a87cff3f2874b4de154e46c5b' },
        success: function (data) {
            console.log(data)
            ret = data.data
        }
    })
    return ret
}

function add_tab(user, work_info) {
    var status_type
    if (work_info.Status == "pending") {
        status_type = "warning"
    }
    else if (work_info.Status == "delay") {
        status_type = "danger"
    }
    else {
        status_type = "info"
    }
    var tab = '<tr class="' + status_type + '">\
                    <td>'+ user + '</td>\
                    <td>'+ work_info.summary + '</td>\
                    <td>'+ work_info.StartDate + '</td>\
                    <td>'+ work_info.EstimateDate + '</td>\
                    <td>'+ work_info.Notes + '</td>\
                    <td>'+ work_info.Reason + '</td>\
                    <td>'+ work_info.Status + '</td>\
                </tr>'
    $("#dl_table").append(tab);
}

function add_user(user, works) {
    var pending = works["pending"]
    var delay = works["delay"]
    var ongoing = works["ongoing"]
    for (var id in pending) {
        work_info = get_work(pending[id])
        add_tab(user, work_info)
    }
    for (var id in delay) {
        work_info = get_work(delay[id])
        add_tab(user, work_info)
    }
    for (var id in ongoing) {
        work_info = get_work(ongoing[id])
        add_tab(user, work_info)
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}

$(function () {
    wd_token = getCookie("wd_token")
    if (wd_token == "") {
        window.location.href = "/";
    }
    $.ajax({
        type: "GET",
        url: "/workdone/QueryIssueList_V2/",
        dataType: "json",
        contentType: "application/json",
        // async: false,
        data: { token: wd_token },
        success: function (body) {
            // console.log(body);
            if (body.error_code == 0) {
                for (var user in body.data) {
                    add_user(user, body.data[user])
                }
            }
        }
    })

    $('#wd_exit').click(function () {
        clearCookie("wd_token")
        console.log("clearCookie");
    })
})