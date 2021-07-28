window.addEventListener("DOMContentLoaded", () => {
	var { ipcRenderer } = require("electron");
	document.getElementById("close-btn").addEventListener("click", () => {
		// alert("WWWWWW");

		ipcRenderer.send("window-close");
	});

	document.getElementById("Enviar").addEventListener("click", () => {
		var rangoTempResAgua= document.getElementById("TempAguaReserva").value;
		var rangoTempTerrario= document.getElementById("TempTerrario").value;
		var rangoHumedad= document.getElementById("Humedad").value;

		//Validar en caso de que sea vacio, es decir, "". Ya que ahora si se deja vacío salta la alerta de error.

		if (rangoTempResAgua < 15.55 || rangoTempResAgua > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else if (rangoTempTerrario < 15.55 || rangoTempTerrario > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else if (rangoHumedad < 15.55 || rangoHumedad > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else {
			ipcRenderer.send("alertaFormSuccess");
		}
	});
});
