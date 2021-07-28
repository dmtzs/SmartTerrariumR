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

		if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoTempResAgua > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoTempTerrario > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoHumedad > 50) {
			ipcRenderer.send("alertaFormError");
		}
		else {
			ipcRenderer.send("alertaFormSuccess");
		}
	});
});
