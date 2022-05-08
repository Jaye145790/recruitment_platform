function upload() {
	var formdata = new FormData($("#uploadform")[0]);
	$.ajax({
		url: "/upload_btn",
		type: "POST",
		data: formdata,
		processData: false,
		contentType: false,
		cache: false,
		success: function(data) {
			toastr["success"](data);
			get_list()
		},
		error: function() {
			toastr["error"]("请选择上传文件");
		}
	});
}

function get_list() {
	$("#filelist").empty();
	$.ajax({
		url: "/get_list",
		type: "get",
		success: function(result) {
			$.each(result, function(index) {
				// 显示主页简历信息
				$("#filelist").append(result[index]).append('</br>')
			})
		},
	})
}

// 提交简历信息
function interviewee() {
	var formdata = {
	    "name": $("#name").val(),
	    "gender": $("#gender").val(),
	    "school": $("#school").val(),
		"major": $("#major").val(),
		"education": $("#education").val(),
		"graduated": $("#graduated").val(),
		"experience": $("#experience").val(),
		"level": $("#level").val(),
		"resume": $("#resume").val(),
		"interview": $("#interview").val(),
		"hire": $("#hire").val()
	}
	$.ajax({
	    url: "/upload",
	    data: JSON.stringify(formdata),
	    type: "POST",
	    dataType: "json",
	    contentType: "application/json",
	    success: function(result) {
	        if (result.result == "OK") {
	            // toastr["success"]("简历信息上传")
	        } else if (result.result == "NO") {
	            // toastr["error"](result.msg)
	        }
	    },
	    error: function() {
	        toastr["error"]("网络连接失败");
	    }
	})
}