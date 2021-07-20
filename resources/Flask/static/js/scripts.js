$("#close-btn").on("click", function () {
	$.ajax({
		type: "POST",
		url: "/closeApp",
		data: { closeMsg: "closeAll" },
	});
});
