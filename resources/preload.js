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

		if (rangoTempResAgua== null || rangoTempResAgua== "" || rangoTempResAgua < 15.55 || rangoTempResAgua > 35) {
			ipcRenderer.send("alertaForm");
		}
		else if (rangoTempTerrario== null || rangoTempTerrario== "" || rangoTempTerrario < 15.55 || rangoTempTerrario > 35) {
			ipcRenderer.send("alertaForm");
		}
		else if (rangoHumedad== null || rangoHumedad== "" || rangoHumedad < 15.55 || rangoHumedad > 35) {
			ipcRenderer.send("alertaForm");
		}
	});
});
