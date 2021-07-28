function validarFormulario() {
    let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
	let rangoTempTerrario= document.getElementById("TempTerrario").value;
	let rangoHumedad= document.getElementById("Humedad").value;

    if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoTempResAgua > 50) {
        return false;
    }
    else if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoTempTerrario > 50) {
        return false;
    }
    else if ((rangoTempResAgua < 15.55) && (rangoTempResAgua != "") || rangoHumedad > 50) {
        return false;
    }
}