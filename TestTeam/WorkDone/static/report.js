
wd_token = ""

$(function () {
    wd_token = getCookie("wd_token")
    if (wd_token == "") {
        window.location.href = "/";
    }


    $('#report_btn').click(function () {

        $.ajax({
            type: "GET",
            url: "/workdone/getWeeklyReport/",
            dataType: "json",
            contentType: "application/json",
            // async: false,
            data: {
                token: wd_token,
                // day: $('#InputDay').val()
                day: $('#InputDay').datetimepicker('getFormattedDate')
            },
            success: function (body) {
                // console.log(body);
                if (body.error_code == 0) {
                    var path = body.data.substring(10, )
                    console.log(path)
                    // var host = location.host
                    // console.log(host)
                    window.open(path)
                }
            }
        })
    })
    $('#wd_exit').click(function () {
        clearCookie("wd_token")
        console.log("clearCookie");
    })
    Date.prototype.Format = function (format) {
        var o = {
            "M+": this.getMonth() + 1, //month 
            "d+": this.getDate(), //day 
            "h+": this.getHours(), //hour 
            "m+": this.getMinutes(), //minute 
            "s+": this.getSeconds(), //second 
            "q+": Math.floor((this.getMonth() + 3) / 3), //quarter 
            "S": this.getMilliseconds() //millisecond 
        }

        if (/(y+)/.test(format)) {
            format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        }

        for (var k in o) {
            if (new RegExp("(" + k + ")").test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
            }
        }
        return format;

    }

    var date = new Date();
    var now = date.Format("yyyy-MM-dd");
    console.log(wd_token)
    $.ajax({
        type: "GET",
        url: "/workdone/getselfWeeklyReport/",
        dataType: "json",
        contentType: "application/json",
        data: {
            token: wd_token,
            day: now
        },
        success: function (body) {
            // console.log(body)
            // console.log(body.data.last_week)
            // console.log(body.data.next_week)
            var lastweek = body.data.last_week
            var nextweek = body.data.next_week
            var lastweek_str = ""
            var nextweek_str = ""
            lastweek.forEach(function (e) {
                var tmp = e[0] + "(" + e[1] + ")<br>"

                lastweek_str += tmp

            })
            lastweek_str = "<p>" + lastweek_str + "</p>"
            // console.log(lastweek_str)
            $("#panel_lastweek").append(lastweek_str)

            nextweek.forEach(function (e) {
                // var tmp = e[0] + "("+e[1]+")<br>"
                var tmp = e[0] + "<br>"
                nextweek_str += tmp

            })
            nextweek_str = "<p>" + nextweek_str + "</p>"
            // console.log(nextweek_str)
            $("#panel_thisweek").append(nextweek_str)
        }
    })
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
})