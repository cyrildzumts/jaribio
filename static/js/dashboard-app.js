requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendor'
    }
});

requirejs(['accounts','ajax_api','commons', 'image_loader', 'dashboard'], function(accounts, ajax_api){
    accounts.init();
    console.log("JQuery version :", $().jquery);
});