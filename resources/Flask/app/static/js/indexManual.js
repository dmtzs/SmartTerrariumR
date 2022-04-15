$(function () {
	$("#rellenar-bebedero").on("click", function () {
		$("#loader").show();

		$(".disable_inputs").prop("disabled", true);

		$("#rellenar-bebedero").toggleClass("pressed");

		if ($("#rellenar-bebedero").hasClass("pressed")) {
			$("#rellenar-bebedero").text("Detener llenado");
			value = 1;
		} else {
			$("#rellenar-bebedero").text("Rellenar bebedero");
			value = 0;
		}

		$.ajax({
			type: "POST",
			url: "/indexevents",
			data: { rellenar: value },
			complete: function (response) {
				if (response.responseText != "error") {
					if ($("#rellenar-bebedero").hasClass("pressed")) {
						$("#rellenar-bebedero").prop("disabled", false);
					} else {
						$(".disable_inputs").prop("disabled", false);
					}
					$("#loader").hide();
					console.log(response.responseText);
				} else {
					window.location.replace("http://127.0.0.1:5000/error500");
				}
			},
		});
	});

	$("#humedecer").on("click", function () {
		$("#loader").show();
		$(".disable_inputs").prop("disabled", true);
		$("#humedecer").toggleClass("pressed");
		$("#humedecer").text("Humedeciendo");

		value = 1;
		
		$.ajax({
			type: "POST",
			url: "/indexevents",
			data: { humedecer: value },
			complete: function (response) {
				if (response.responseText != "error") {
					
					$("#humedecer").prop("disabled", false);
					setTimeout(function(){callAjax();}, 8000);

					function callAjax() {
						$.ajax({
							type: "POST",
							url: "/indexevents",
							data: { humedecer: value },
							complete: function (response) {
								if (response.responseText != "error") {
									$(".disable_inputs").prop("disabled", false);
									$("#humedecer").text("Humedecer");
									$("#humedecer").toggleClass("pressed");
									$("#loader").hide();
									console.log(response.responseText);
								} else {
									window.location.replace("http://127.0.0.1:5000/error500");
								}
							},
						});
					}
					
					console.log(response.responseText);
				} else {
					window.location.replace("http://127.0.0.1:5000/error500");
				}
			},
		});

	});
});
