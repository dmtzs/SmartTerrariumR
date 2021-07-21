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

		if (rangoTempResAgua== "") {
			
			ipcRenderer.send("alertaForm");
		}
	});
});
