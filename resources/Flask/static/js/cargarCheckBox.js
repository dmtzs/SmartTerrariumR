$(function () {
    var initialMode = '{{ pushed }}'

    if (initialMode === "0"){
      localStorage.input = false
    }
    if (initialMode === "1"){
      localStorage.input = true
    }
    var test = localStorage.input === 'true'? true: false;
    
    $('#modoOperacion').prop('checked', test || false);
    localStorage.input = $('#modoOperacion').is(':checked');
    var modoSwitch = false;
    if ($('#modoOperacion').is(":checked")){
      modoSwitch = true;
    }
    $("#modoOperacion").on('click', function(){
      $("#modoOperacion").prop('disabled', true);
    })
    //envia el estado de la checkbox de modo al backend
    $.ajax({
      type:'POST',
      url:'/',
      data:{ modoOperacion:modoSwitch },
      complete: function(){
        $("#modoOperacion").prop('disabled', false);
        $("#submitButton").prop('disabled', false);
      }
    })

    setTimeout(removeLoader, 10);
    function removeLoader(){
        $( "#loader" ).fadeOut(500, function() {
          // fadeOut complete. Remove the loading div
          $( "#loader" ).hide(); //makes page more lightweight 
      });  
    }
  });