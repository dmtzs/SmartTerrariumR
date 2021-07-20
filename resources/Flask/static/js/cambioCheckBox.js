$("#submitButton").on('click', function(){
    sendString = "strm";
    $("#submitButton").prop('disabled', true);
    $( "#loader" ).show();
    $.ajax({
      type:'POST',
      url:'/raspberry',
      data:{ jsonString:sendString },
      complete: function(response){
        console.log(response.responseText)
        if(response.responseText != "error"){
          document.getElementById("send_data").innerHTML = sendString
          document.getElementById("received_data").innerHTML = response.responseText
          $("#submitButton").prop('disabled', false);
          $( "#loader" ).hide();
        }else{
          window.location.replace('http://127.0.0.1:5000/error500')
        }
      }
    })
  })