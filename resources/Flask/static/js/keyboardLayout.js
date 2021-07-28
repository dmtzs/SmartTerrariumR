$(function () {
	var keyboard = {
		layout: [
			// alphanumeric keyboard type
			// text displayed on keyboard button, keyboard value, keycode, column span, new row
			[
				[
					["1", "1", 49, 0, true],
					["2", "2", 50, 0, false],
					["3", "3", 51, 0, false],
					["Borrar", "8", 8, 3, false],
					["4", "4", 52, 0, true],
					["5", "5", 53, 0, false],
					["6", "6", 54, 0, false],
					["Cancelar", "27", 27, 3, false],
					["7", "7", 55, 0, true],
					["8", "8", 56, 0, false],
					["9", "9", 57, 0, false],
					["Enter", "13", 13, 3, false],
					["0", "0", 48, 0, true],
					[".", ".", 190, 0, false],
				],
			],
		],
	};
	$("input.jQKeyboard").initKeypad({ keyboardLayout: keyboard });
});
