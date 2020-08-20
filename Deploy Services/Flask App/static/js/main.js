$(document).ready(function () {
    // Init
    //$('.image-section').hide();
    $('.loader').hide();
    $('#result_test').hide();

    // Upload Preview
    
   function readURL(input) {
      if (input.files && input.files[0]) {
            var reader = new FileReader();
    
            reader.onload = function(e) {
                $('#act_cam').attr('src', e.target.result);
                }
            reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}
    
    
    $("#imageUpload").change(function () {
        $('.image-section').show();   
        readURL(this);
    });
    
    

    // Predict

    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        


        // Show loading animation
        //$(this).hide();
        $('.loader').show();
    

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                
                /*
                $('.custom_add_tr').append(`
                <tr id="thr_`+i+`">
                  <td>`+i+`</td>
                  <td id="result_test_0_`+i+`"><span> </span></td>
                  <td id="result_test_1_`+i+`"><span> </span></td>
                  <td id="result_test_2_`+i+`"><span> </span></td>
                  <td><span> </span></td>
                </tr>
                
                `).attr('id',i).val(i);
                */
                
                $('#current_test_0').fadeIn(600) ;
                $('#current_test_1').fadeIn(600);
                $('#current_test_2').fadeIn(600);                            
                $('#current_test_0').text(data[0]);
                $('#current_test_1').text(data[1]);               
                $('#current_test_2').text(data[2]);           
                console.log('Succes');
                location.reload(true);
            },
        });

    });

});