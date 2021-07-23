$("#close-btn").on("click", function () {
	$.ajax({
		type: "POST",
		url: "/closeApp",
		data: { closeMsg: "closeAll" },
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
