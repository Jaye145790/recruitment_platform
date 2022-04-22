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
			toastr["error"]("网络连接失败");
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
				$("#filelist").append(result[index]).append('</br>')
			})
		},
	})
}

function interviewee() {
	var formdata = {
	    "name": $("#name").val(),
	    "gender": $("#gender").val(),
	    "school": $("#school").val(),
		"major": $("#major").val(),
		"education": $("#education").val(),
		"graduated": $("#graduated").val(),
		"experience": $("#experience").val(),
		"e_level": $("#e_level").val(),
		"resume": $("#resume").val(),
		"interview": $("#interview").val(),
		"dept": $("#dept").val(),
		"hire": $("#hire").val(),
	}
	$.ajax({
	    url: "/upload",
	    data: JSON.stringify(formdata),
	    type: "POST",
	    dataType: "json",
	    contentType: "application/json",
	    success: function(result) {
	        if (result.result == "OK") {
	            toastr["success"]("注册成功")
	        } else if (result.result == "NO") {
	            toastr["error"](result.msg)
	        }
	    },
	    error: function() {
	        toastr["error"]("网络连接失败");
	    }
	})
}