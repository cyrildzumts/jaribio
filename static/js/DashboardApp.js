requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendor'
    }
});

requirejs(['attributes_api', 'ajax_api', 'components_api', 'accounts','price_calculator', 'commons', 'image_loader', 'dashboard'], function(AttributeManager ,ajax_api, Component, accounts, calculator){
    console.log("DashboardApp loaded ...");
    var attr_manager = new AttributeManager();
    attr_manager.init();
    Component.initComponent();
    calculator.init();
    console.log("JQuery version :", $().jquery);
});