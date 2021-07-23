$(function () {
	$("#rellenar-bebedero").on("click", function () {
		$("#rellenar-bebedero").toggleClass("pressed");
		if ($("#rellenar-bebedero").hasClass("pressed")) {
			$("#rellenar-bebedero").text("Detener llenado");
		} else {
			$("#rellenar-bebedero").text("Rellenar bebedero");
		}
	});

	$("#humedecer").on("click", function () {
		console.log("humedecer");
	});
});
