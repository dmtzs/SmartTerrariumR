function validarFormulario() {
    let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
	let rangoTempTerrario= document.getElementById("TempTerrario").value;
	let rangoHumedad= document.getElementById("Humedad").value;

    if (rangoTempResAgua < 15.55 || rangoTempResAgua > 50) {
        return false;
    }
    else if (rangoTempTerrario < 15.55 || rangoTempTerrario > 50) {
        return false;
    }
    else if (rangoHumedad < 15.55 || rangoHumedad > 50) {
        return false;
    }
}