$(function () {
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
});