data_arr = {}
// wd_token = "516c7e36e65af02a87cff3f2874b4de154e46c5b"
wd_token = ""
wd_work_id = ""

function updateModal(id) {
	var data = data_arr[id];
	$("#update_work-summary").val(data.summary)
	$("#update_work-startdate").val(data.StartDate)
	$("#update_work-estimatedate").val(data.EstimateDate)
	$("#update_work-notes").val(data.Notes)
	$("#update_work-reasons").val(data.Reason)
	$("#update_work-status").attr("disabled", false)
	$("#update_work-notes").attr("disabled", false)
	$("#update_work-reasons").attr("disabled", false)
	wd_work_id = id
	var status = data.Status
	var op = ""
	switch (data.Status) {
		case "todo":
			op = '<option>todo</option>\
					<option>ongoing</option>\
					<option>pending</option>'
			break;
		case "ongoing":
			op = '<option>ongoing</option>\
					<option>pending</option>\
					<option>done</option>'
			break;
		case "pending":
			var s = data.EstimateDate;
			s = s.replace(/-/g, "/");
			// console.log(s)
			var d1 = new Date(s)
			var d2 = new Date();
			if (d1 <= d2) {
				// console.log(">")
				op = '<option>pending</option>\
					<option>delay</option>\
					<option>done</option>'
			} else {
				// console.log("<")
				op = '<option>pending</option>\
					<option>ongoing</option>\
					<option>done</option>'
			}
			break;
		case "delay":
			op = '<option>delay</option>\
					<option>pending</option>\
					<option>done</option>'
			break;
		case "done":
			op = '<option>done</option>'
			$("#update_work-status").attr("disabled", true)
			$("#update_work-notes").attr("disabled", true)
			$("#update_work-reasons").attr("disabled", true)
			break;
	}

	$("#update_work-status").empty()
	$("#update_work-status").append(op);

}

function update(id) {
	var data = data_arr[id];
	$("#update_work-summary").val(data.summary)
	$("#update_work-startdate").val(data.StartDate)
	$("#update_work-estimatedate").val(data.EstimateDate)
}

function add_reason_label(reasons) {
	var labels = "";
	// console.log(reasons)
	if (reasons != null) {
		reasons_arr = reasons.split(",")
		// console.log(reasons_arr)
		for (var cc in reasons_arr) {
			labels += '<span class="label label-primary">' + reasons_arr[cc] + '</span> '
		}
	}
	return labels
}

function add_tab_in_panel(data) {
	console.log(data)
	data_arr[data.id] = data;
	var tab = '\
			<table id="work' + data.id + '" class="table table-striped table-bordered table-condensed" contenteditable="true">\
				<tbody>\
					<tr>\
						<td>\
							<p>'+ data.summary + '</p>\
							<p>StartTime：'+ data.StartDate + '</p>\
							<p>EstimateDate：'+ data.EstimateDate + '</p>\
							<p>Reasons: '+ add_reason_label(data.Reason) + '</p>\
							<button id="work_btn'+ data.id + '" class="btn btn-info btn-xs" type="button " data-toggle="modal" data-target="#UpdateWorkModal" onclick="updateModal(' + data.id + ')">Update</button>\
						</td>\
					</tr>\
				</tbody>\
			</table>'

	// switch (data.Status) {
	// 	case "todo":
	// 		$("#panel-todo").append(tab);
	// 		break;
	// 	case "ongoing":
	// 		$("#panel-ongoing").append(tab);
	// 		break;
	// 	case "pending":
	// 		$("#panel-pending").append(tab);
	// 		break;
	// 	case "delay":
	// 		$("#panel-delay").append(tab);
	// 		break;
	// 	case "done":
	// 		$("#panel-done").append(tab);
	// 		break;
	// }
	//一行搞定，傻逼了写这么多
	$("#panel-" + data.Status).append(tab)
}

function addWork(work_id) {
	var x = 5;
	$.ajax({
		type: "GET",
		url: "/workdone/getWorkById/",
		dataType: "json",
		contentType: "application/json",
		data: { id: work_id, token: wd_token },
		success: function (data) {
			add_tab_in_panel(data.data)
		}
	})
}

$(function () {
	wd_token = getCookie("wd_token")
	if (wd_token == "") {
		window.location.href = "/";
	}

	$.ajax({
		type: "GET",
		url: "/workdone/getWorkList/",
		dataType: "json",
		contentType: "application/json",
		data: { token: wd_token },
		success: function (body) {
			// console.log(data);
			if (body.error_code == 0) {
				for (var work_id in body.data.works) {
					addWork(body.data.works[work_id]);
				}
				ret = 0;
			} else {
				ret = 1;
			}
		}
	})

	$('#save-btn').click(function () {
		var work_summary = $("#work-summary").val();
		var work_startdate = $('#work_startdate_pl').datetimepicker('getFormattedDate')
		var work_estimatedate = $('#work_estimatedate_pl').datetimepicker('getFormattedDate')
		console.log(work_summary);
		console.log(work_startdate);
		console.log(work_estimatedate);

		$.ajax({
			type: "POST",
			url: "/workdone/CreateWork/",
			contentType: "application/json",
			data: JSON.stringify({
				"token": wd_token,
				"summary": work_summary,
				"StartDate": work_startdate,
				"EstimateDate": work_estimatedate
			}),
			success: function (data) {
				console.log(data);
			}
		})

		$('#NewWorkModal').modal('hide')
		window.location.href = "";
	})

	$('#update_save-btn').click(function () {
		console.log("ok")
		var status = $("#update_work-status").val()
		var notes = $("#update_work-notes").val()
		var reasons = $("#update_work-reasons").val()

		$.ajax({
			type: "POST",
			url: "/workdone/UpdateWork/",
			contentType: "application/json",
			data: JSON.stringify({
				"token": wd_token,
				"work_id": wd_work_id,
				"status": status,
				"Notes": notes,
				"Reasons": reasons
			}),
			success: function (data) {
				console.log(data);
			}
		})

		$('#UpdateWorkModal').modal('hide')
		window.location.href = "";
	})

	$('#wd_exit').click(function () {
		clearCookie("wd_token")
		console.log("clearCookie");
	})
})


//设置cookie
function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
	var expires = "expires=" + d.toUTCString();
	document.cookie = cname + "=" + cvalue + "; " + expires;
}
//获取cookie
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
//清除cookie
function clearCookie(name) {
	setCookie(name, "", -1);
}
function checkCookie() {
	var user = getCookie("username");
	if (user != "") {
		alert("Welcome again " + user);
	} else {
		user = prompt("Please enter your name:", "");
		if (user != "" && user != null) {
			setCookie("username", user, 365);
		}
	}
}
