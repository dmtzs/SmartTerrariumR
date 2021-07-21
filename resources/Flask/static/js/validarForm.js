function validarFormulario() {
    let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
    let rangoTempTerrario= document.getElementById("TempTerrario").value;
    let rangoHumedad= document.getElementById("Humedad").value;
    let flotante= /^\d*(\.\d{1})?\d{0,1}$/;

    if (rangoTempResAgua== "") {
        return false;
    }
}