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
		var bande= 0;

		try {
			rangoTempResAgua= parseFloat(rangoTempResAgua);
			rangoTempTerrario= parseFloat(rangoTempTerrario);
			rangoHumedad= parseFloat(rangoHumedad);
			bande= 1;
		} catch (error) {
			bande= 0;
		}

		if (rangoTempResAgua== null || rangoTempResAgua== "" || rangoTempResAgua.length < 5 || rangoTempResAgua.length > 5 || bande=== 0) {
			ipcRenderer.send("alertaForm");
		}
		if (rangoTempTerrario== null || rangoTempTerrario== "" || rangoTempTerrario.length < 5 || rangoTempTerrario.length > 5 || bande=== 0) {
			ipcRenderer.send("alertaForm");
		}
		if (rangoHumedad== null || rangoHumedad== "" || rangoHumedad.length < 5 || rangoHumedad.length > 5 || bande=== 0) {
			ipcRenderer.send("alertaForm");
		}
	});
});
