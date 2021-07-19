$(document).ready(function () {
    $('#dismiss').on('click', function () {
        $('#sidebar').removeClass('active');
    });
    //boton para abrir la sidebar
    $("#sidebarCollapse").on("click", function () {
        $("#sidebar").toggleClass("active");
        $(this).toggleClass("active");
    });

    $("#boton_inicio").on("click", function () {
        window.location.reload();
    });

    //almacena el modo de operacion
    $(function(){
        var test = localStorage.input === 'true'? true: false;
        $('#modoOperacion').prop('checked', test || false);
    });
    $('#modoOperacion').on("change", function(e){
        localStorage.input = $(this).is(':checked');
        var modoSwitch = false;
        if ($('#modoOperacion').is(":checked")){
        modoSwitch = true;
        }
        e.preventDefault();
        //envia el estado de la checkbox de modo al backend
        $.ajax({
        type:'POST',
        url:'/',
        data:{ modoOperacion:modoSwitch }
        })
        window.location.reload();
    })
    });