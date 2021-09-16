requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendor'
    }
});

requirejs(['ajax_api', 'components_api','commons', 'image_loader'], function(ajax_api, Component){
    console.log("LyshopApp loaded ...");

    Component.initComponent();
    
    console.log("JQuery version :", $().jquery);
});