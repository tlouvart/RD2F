$(document).ready(function () {

    
    

    // Enable

    $('#btn-enable-s').click(function () {
        
        $('#btn-enable-s').toggleClass("active");
        $('#btn-disable-s').removeClass("active");
        $('#btn-disable-s').text('Stop System');

        
        if ($('#btn-enable-s').hasClass("active")) {
            // Show loading animation
           $('.loader').show()
        
            // Make prediction by calling api /predict
            var timeout = setInterval(function () {$.ajax({
                type: 'POST',
                url: '/dashboard/enable',
    
                contentType: false,
                cache: false,
                processData: false,
                async: true,
                success: function (data) {
                    // Get and display the result
                    $('.loader').hide();
                    console.log("Enabled")
                    $('#table-list-entry').load(document.URL +  ' #table-list-entry');
                    $('#act_cam').attr('src', '/static/last_image_to_test/'+data.name);
                    $('.loader').show()
                },
            });
    }, 30000);
    };

});

    $('#btn-disable-s').click(function () {
        
        $('#btn-enable-s').removeClass("active");
        $('#btn-disable-s').toggleClass("active");
        $('#btn-disable-s').text('System Stopped');
        
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