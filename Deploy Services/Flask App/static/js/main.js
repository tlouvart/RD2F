$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result_test').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result_test_0').text('');
        $('#result_test_1').text('');
        $('#result_test_2').text('');
        $('#result_test_0').hide();
        $('#result_test_1').hide();
        $('#result_test_2').hide();
        readURL(this);
    });

    // Predict
    var i=0;
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        


        // Show loading animation
        $(this).hide();
        $('.loader').show();
    
        i++;
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
                
                $('.custom_add_tr').append(`
                <tr id="thr_`+i+`">
                  <td>`+i+`</td>
                  <td id="result_test_0_`+i+`"><span> </span></td>
                  <td><span> </span></td>
                  <td id="result_test_1_`+i+`"><span> </span></td>
                  <td id="result_test_2_`+i+`"><span> </span></td>

                </tr>
                
                `).attr('id',i).val(i);
                
                
                $('#result_test_0_'+i).fadeIn(600) ;
                $('#result_test_1_'+i).fadeIn(600);
                $('#result_test_2_'+i).fadeIn(600);                            
                $('#result_test_0_'+i).text(data[0]);
                $('#result_test_1_'+i).text(data[1]);               
                $('#result_test_2_'+i).text(data[2]);           
                console.log('Succes');
            },
        });
    });

});