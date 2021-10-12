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

//teclado en pantalla
$(function () {
	$("#virtual-keyboard button").on("click", function () {
		if ($(this).attr("data") == "DEL") {
			board_text = $("textarea.board").text();
			board_text = board_text.substring(0, board_text.length - 1);
			$("textarea.board").text(board_text);
		} else {
			$("textarea.board").text(
				$("textarea.board").text() + $(this).attr("data")
			);
		}
	});
});
