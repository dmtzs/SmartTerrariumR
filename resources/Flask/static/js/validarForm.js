function validarFormulario() {
    var rangoTempResAgua= document.getElementById("TempAguaReserva").value;
	var rangoTempTerrario= document.getElementById("TempTerrario").value;
	var rangoHumedad= document.getElementById("Humedad").value;

    if (rangoTempResAgua < 15.55 || rangoTempResAgua > 35) {
        return false;
    }
    else if (rangoTempTerrario < 15.55 || rangoTempTerrario > 35) {
        return false;
    }
    else if (rangoHumedad < 15.55 || rangoHumedad > 35) {
        return false;
    }
}