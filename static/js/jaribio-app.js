requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendors'
    },
    waitSeconds: 0
});

requirejs(['accounts','ajax_api', 'commons', 'image_loader'], function(account,ajax_api){
    account.init();
    console.log("JQuery version :", $().jquery);
});