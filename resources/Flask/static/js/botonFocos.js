$("#botonFocos").on("click", function (e) {
	$("#botonFocos").prop("disabled", true);
	$("#loader").show();
	if ($("#botonFocos").hasClass("on")) {
		$("#botonFocos").removeClass("on");
		statusFocos = 0;
	} else {
		$("#botonFocos").addClass("on");
		statusFocos = 1;
	}

	statusFocos = $.ajax({
		type: "POST",
		url: "/indexevents",
		data: { lightStatus: statusFocos },
		complete: function (response) {
			if (response.responseText != "error") {
				$("#botonFocos").prop("disabled", false);
				$("#loader").hide();
			} else {
				window.location.replace("http://127.0.0.1:5000/error500");
			}
		},
	});
});
