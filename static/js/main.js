function getStatus(){
    var data = $.ajax({
        type: "GET",
        url: '/get_internet_status/',
        async: false
    }).complete(function(){
        setTimeout(function(){getStatus();}, 1000);
    }).responseText;
    console.log(data);
    $('#internet_status').html(data);
}

$(function() {
    getStatus();
    $('#dont_connect').click(function() {
        window.location.href = '/go_to_step/4/';
    });
});
