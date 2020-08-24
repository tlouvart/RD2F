$(document).ready(function () {

    $('.custom-select').change(function () {

        var selectedCamera = $('.custom-select').val();
        console.log(selectedCamera)
    
    

        // Enable
    
        $('#btn-enable-s').click(function () {
            
            $('#btn-enable-s').toggleClass("active");
            $('#btn-disable-s').removeClass("active");
            $('#btn-disable-s').text('Stop System');
            $('#btn-enable-s').text("Monitoring Enable");
            
            if ($('#btn-enable-s').hasClass("active")) {
                // Show loading animation
               $('.loader').show()
            
                // Make prediction by calling api /predict
                function predict() {$.ajax({
                    type: 'POST',
                    url: '/dashboard/enable',
        
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: true,
                    data: selectedCamera,
                    success: function (data) {
                        // Get and display the result
                        $('.loader').hide();
                        console.log("Enabled")
                        $('#table-list-entry').load(document.URL +  ' #table-list-entry');
                        $('#act_cam').attr('src', '/static/last_image_to_test/' + data.name);                   
                        $('.loader').show()
                    },
                });
                setTimeout(predict, 30000);
                }
                predict();
                
                };
    
        });
    
        $('#btn-disable-s').click(function () {
           
            $('#btn-enable-s').removeClass("active");
            $('#btn-disable-s').toggleClass("active");
            $('#btn-disable-s').text('System Stopped');
            $('btn-enable-s').text("Enable Monitoring");
            
            if ($('#btn-disable-s').hasClass("active")) {
                // Show loading animation
                $('.loader').hide();
            
                // Make prediction by calling api /predict
                $.ajax({
                    type: 'POST',
                    url: '/dashboard/disable',
        
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: true,
                    success: function (data) {
                        // Get and display the result
                        console.log("Disable")
                        location.reload(true);                    
                    },
                });
                };  
        });


    });


});