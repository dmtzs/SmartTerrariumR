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

		let aux1= toString(rangoTempResAgua);
		let aux2= toString(rangoTempTerrario);
		let aux3= toString(rangoHumedad);

		if (rangoTempResAgua < 15.55 || rangoTempResAgua > 50) {
			return false;
		}
		else if (rangoTempTerrario < 15.55 || rangoTempTerrario > 50) {
			return false;
		}
		else if (rangoHumedad < 15.55 || rangoHumedad > 50) {
			return false;
		}
		else if (!aux1.includes(".")) {
			return false;
		}
		else if (!aux2.includes(".")) {
			return false;
		}
		else if (!aux3.includes(".")) {
			return false;
		}
	});
});
