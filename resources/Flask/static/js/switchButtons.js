//check operation mode
$(function () {
	if (initialMode === "0") {
		localStorage.input = false;
	}
	if (initialMode === "1") {
		localStorage.input = true;
	}

	var test = localStorage.input === "true" ? true : false;
	$("#modoOperacion").prop("checked", test || false);

	$("#modoOperacion").on("change", function (e) {
		$("#modoOperacion").prop("disabled", true);
		localStorage.input = $(this).is(":checked");
		var modoSwitch = false;
		if ($("#modoOperacion").is(":checked")) {
			modoSwitch = true;
		}
		e.preventDefault();
		//envia el estado de la checkbox de modo al backend
		$.ajax({
			type: "POST",
			url: "/indexevents",
			data: { modoOperacion: modoSwitch },
		});
		window.location.reload();
	});
});

//check day light mode
$(function () {
	if (lightMode === "0") {
		localStorage.input = false;
	}
	if (lightMode === "1") {
		localStorage.input = true;
	}

	var test = localStorage.input === "true" ? true : false;
	$("#day-night").prop("checked", test || false);

	$("#day-night").on("change", function (e) {
		$("#day-night").prop("disabled", true);
		localStorage.input = $(this).is(":checked");
		var modolight = false;
		if ($("#day-night").is(":checked")) {
			modolight = true;
		}
		e.preventDefault();
		//envia el estado de la checkbox de modo al backend
		$.ajax({
			type: "POST",
			url: "/indexevents",
			data: { lighMode: modolight },
			complete: function (response) {
				if (response.responseText != "error") {
					$("#day-night").prop("disabled", false);
					$("#loader").hide();
				} else {
					window.location.replace("http://127.0.0.1:5000/error500");
				}
			},
		});
	});
});

//loader
$(function () {
	setTimeout(removeLoader, 10);
	function removeLoader() {
		$("#loader").fadeOut(500, function () {
			// fadeOut complete. Remove the loading div
			$("#loader").hide(); //makes page more lightweight
		});
	}
});
