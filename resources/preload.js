window.addEventListener("DOMContentLoaded", () => {
	var { ipcRenderer } = require("electron");
	document.getElementById("close-btn").addEventListener("click", () => {
		// alert("WWWWWW");

		ipcRenderer.send("window-close");
	});

	document.getElementById("Enviar").addEventListener("click", () => {
		let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
		let rangoTempTerrario= document.getElementById("TempTerrario").value;
		let rangoHumedad= document.getElementById("Humedad").value;

		if (rangoTempResAgua== null || rangoTempResAgua== "" || rangoTempResAgua.length < 5 || rangoTempResAgua.length > 5 || !Number.isNaN(rangoTempResAgua)) {
			ipcRenderer.send("alertaForm");
		}
		else if (rangoTempTerrario== null || rangoTempTerrario== "" || rangoTempTerrario.length < 5 || rangoTempTerrario.length > 5 || !Number.isNaN(rangoTempTerrario)) {
			ipcRenderer.send("alertaForm");
		}
		else if (rangoHumedad== null || rangoHumedad== "" || rangoHumedad.length < 5 || rangoHumedad.length > 5 || !Number.isNaN(rangoHumedad)) {
			ipcRenderer.send("alertaForm");
		}
	});
});
