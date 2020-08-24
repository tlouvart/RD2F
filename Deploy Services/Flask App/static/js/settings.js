$(document).ready(function () {



$('#default-settings').click(function () {
        $.ajax({
                    type: 'POST',
                    url: '/settings/default',
        
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: true,
                    success: function (data) {
                         location.reload(true);                       
                    },
                });   
});


$('#edit-btn,#edit-btn1,#edit-btn2').click(function () {
        console.log("able");
        $(this).parent().siblings( "input" ).prop("disabled", false);
        $(this).parent().siblings( "select" ).prop("disabled", false);        
}); 
$('#save-chg,#save-chg1,#save-chg2').click(function () {
        console.log('disable edit');
        var server_path_new = $("#input-path").val();

        $(this).parent().siblings( "input" ).prop("disabled", true);
        $(this).parent().siblings( "select" ).prop("disabled", true);

        $.ajax({
                    type: 'POST',
                    url: '/settings',
        
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: true,
                    data: server_path_new,
                    success: function (data) {
                        $('#col-md-5').load(document.URL +  '#col-md-5');
                    },
                });
                
        isSiteOnline(server_path,function(found){
            if(found) {
                $('#server-status').attr('class', "input-group-text server-status-on");
                $('#server-status').text("ON");  
                console.log('Server running');
                }
            else {
                $('#server-status').attr('class', "input-group-text server-status-off");
                $('#server-status').text("OFF");
                
                // site is offline (or favicon not found, or server is too slow)
            }
        })   
});










function isSiteOnline(url,callback) {
    // try to load favicon
    var timer = setTimeout(function(){
        // timeout after 5 seconds
        callback(false);
    },5000)

    var img = document.createElement("img");
    img.onload = function() {
        clearTimeout(timer);
        callback(true);
    }

    img.onerror = function() {
        clearTimeout(timer);
        callback(false);
    }

    img.src = url +"/favicon.ico";
}


isSiteOnline(server_path,function(found){
    if(found) {
        $('#server-status').attr('class', "input-group-text server-status-on");
        $('#server-status').text("ON");  
        console.log('Server running');
        }
    else {
        $('#server-status').attr('class', "input-group-text server-status-off");
        $('#server-status').text("OFF");  
        // site is offline (or favicon not found, or server is too slow)
    }
})





});