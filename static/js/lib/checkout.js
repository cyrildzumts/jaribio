define([
'ajax_api'
], function(ajax_api) {
    'use strict';
    var ADDRESS_FIELDS = [ 
            'user', 'city', 'firstname', 'lastname', 'country', 
            'postal_code','phone_number', 'address_extra', 'street',
            'house_number', 'is_active'
        ];

    var ADDRESS_FIELDS_REQUIRED = [ 
        'user', 'city', 'firstname', 'lastname', 'country', 
        'postal_code','phone_number', 'street'
 
    ];
    var LI_PO_PREFIX = '#p-option-';
    var LI_PM_PREFIX = '#p-method-';
    var INPOUT_PM_PREFIX = '#pm-';
    var PAYMENT_METHOD_CONTAINER = "#payment-method ul";
    var SHIP_STANDARD = 0;
    var SHIP_EXPRESS  = 1
    var SHIP_IN_STORE = 2
    var SHIP_IN_STORE_POG = 3
    var SHIP_IN_STORE_LBV = 4
    var SHIPPING_ADDRESS_CONTAINER = "address-container";
    var api_address_url = '/api/create-address/';
    var SHIP_IN_HOUSE = [SHIP_STANDARD, SHIP_EXPRESS];
    var SHIP_IN_STORE = [SHIP_IN_STORE, SHIP_IN_STORE_LBV, SHIP_IN_STORE_POG];
    var address = {
        id : "",
        name : "",
        email : "",
        city : "",
        postal_code: "",
        street : "",
        house_number : "",
        phone_number : "",
        country : ""
    };
    var step = {
        index : 1,
        valid : false,
        tab : null
    };
    var shipmode_tab = 1;
    var address_tab = 2;
    var payment_tab = 3;
    var verification_tab = 4;
    var confirmation_tab = 5
    var steps_order = [shipmode_tab, address_tab, payment_tab, verification_tab, confirmation_tab]
    var tabs = null;

    var PAY_AT_DELIVERY = 0;
    var PAY_AT_ORDER = 1;
    var PAY_WITH_PAY = 2;
    var PAY_BEFORE_DELIVERY = 3;

    var PAYMENT_OPTIONS = [PAY_AT_DELIVERY, PAY_AT_ORDER, PAY_WITH_PAY, PAY_BEFORE_DELIVERY];

    var ORDER_PAYMENT_CASH = 0;
    var ORDER_PAYMENT_PAY = 1;
    var ORDER_PAYMENT_MOBILE = 2;

    var PAYMENT_METHODS = [ORDER_PAYMENT_CASH, ORDER_PAYMENT_MOBILE, ORDER_PAYMENT_PAY];



    var PAYMENT_OPTION_METHODS_MAPPING = new Map();
    PAYMENT_OPTION_METHODS_MAPPING.set(PAY_AT_DELIVERY, [ORDER_PAYMENT_CASH]);
    PAYMENT_OPTION_METHODS_MAPPING.set(PAY_AT_ORDER, [ORDER_PAYMENT_PAY, ORDER_PAYMENT_MOBILE]);
    PAYMENT_OPTION_METHODS_MAPPING.set(PAY_BEFORE_DELIVERY, [ORDER_PAYMENT_CASH, ORDER_PAYMENT_MOBILE, ORDER_PAYMENT_PAY]);

    var Checkout = function(tabs_comp){
        tabs = tabs_comp;
        this.address = {};
        this.payment_option = -1;
        this.payment_method = -1;
        this.currentTab = 1;
        this.shipping_price = 0;
        this.items_count = 0;
        this.steps = [];
        this.current_step = {};
        this.address_required = true;
        this.address_available = false;
        this.ship_mode = -1;
        this.ship_mode_valid = false;
        this.payment_option_is_valid = false;
        this.payment_method_is_valid = false;
        this.address_is_valid = false;
        this.shipping_price = 0;
        this.sub_total = 0;
        this.total = 0;
        this.form_is_valid = false;
        this.form_selector = "checkout-form";
        this.form = null;
        
    };
    
    Checkout.prototype.init = function(){
        var self = this;
        this.form = document.getElementById(this.form_selector);
        if(!this.form){
            return;
        }
        var addr = document.getElementById('address');

        $('.js-input-payment-option').on('change', function(event){
            self.payment_option = this.value;
            self.payment_method = -1;
            self.payment_method_is_valid = false;
             tabs.toggle_checked(payment_tab, false);
            self.update_payment_method();
            self.validate_pament_options();
        });
        $('.js-input-payment-method').on('change', function(event){
            self.payment_method = $(this).data('mode');
            self.validate_pament_method();
        });
        $('.js-add-address').on('click', function(){
            $('#new-address, #checkout-address').toggleClass('hidden');
            
            if(addr){
                addr.toggleAttribute('disabled');
            }
            
        });
        $('.js-create-address').on('click', function(){
            self.create_address();
        });
        $('.js-input-ship-mode').on('change', function(event){
            self.ship_mode_changed(this);
        });
        //this.validate_address();
        self.update_payment_method();
        tabs.init();
        
        $('input.js-input-ship-mode').prop('checked', false);
        $('.js-send').prop('disabled', true);
        this.form.addEventListener('submit', function(event){
            event.stopPropagation();
            if(!self.is_form_valid()){
                event.preventDefault();
                return false;
            }
            return true;
        });

    };

    Checkout.prototype.update_send_btn = function(){
        $('.js-send').prop('disabled', !this.is_form_valid());
        $('.js-send').toggleClass('disabled', !this.is_form_valid());
    };

    Checkout.prototype.is_form_valid = function(){
        return this.ship_mode_valid && this.address_is_valid && this.payment_option_is_valid && this.payment_method_is_valid;
    };

    Checkout.prototype.validate_address = function(){
        var toggle = false;
        var address_input = $('#address').get();
        var inputs_container = $('#new-address').get();
        if(address_input){
            toggle = true;
            this.address_is_valid = true;
        }else if(inputs_container){
            var inputs = $("input", inputs_container);
            toggle = true;
            var i;
            for(i in inputs){
                if(i.value == ""){
                    toggle = false;
                    break;
                }
            }
        }
        this.address_is_valid = toggle;
        tabs.toggle_checked(address_tab, toggle);
        this.update_send_btn();
    };
    Checkout.prototype.validate_pament_options = function(){
       var is_valid = PAYMENT_OPTIONS.includes(parseInt(this.payment_option));
       if(!is_valid){
           console.log("Payment Option is invalid");
       }
       //tabs.toggle_checked(payment_tab, is_valid);
       this.payment_option_is_valid = is_valid;
       this.update_send_btn();

    };

    Checkout.prototype.validate_pament_method = function(){
       var methods = PAYMENT_OPTION_METHODS_MAPPING.get(parseInt(this.payment_option));
       var is_valid = methods && methods.includes(parseInt(this.payment_method));
       if(!is_valid){
           console.log("Payment Method is invalid");
       }
        tabs.toggle_checked(payment_tab, is_valid);
        this.payment_method_is_valid = is_valid;
        this.update_send_btn();
        return is_valid;
     };

    Checkout.prototype.create_address = function(){
        var self = this;
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]');
        var container = $('#new-address');
        var address_inputs = $('input', container);
        var available_fields = [];
        var data = {
            'csrfmiddlewaretoken' : csrfmiddlewaretoken.val()
        };
        address_inputs.each(function(){
            if(this.value){
                available_fields.push(this.name);
            }
            data[this.name] = this.value;
        });
        var missing_fields = ADDRESS_FIELDS_REQUIRED.filter(field => !available_fields.includes(field));
        if(missing_fields.length > 0){
            missing_fields.forEach(field =>{
                $(`input[name="${field}"]`, container).addClass('warn');
            });
            return;
        }else{
            address_inputs.removeClass('warn');
        }
        var option = {
            type:'POST',
            dataType: 'json',
            url : api_address_url,
            data : data
        }
        var add_promise = ajax_api.ajax(option).then(function(response){
            if(response.status){
                address_inputs.each(function(){
                    this.disabled = 'disabled';
                });
                var input = $('<input>', {name : 'address', type :'hidden', value : response.id});
                input.appendTo(container);
                this.address_is_valid = true;
                tabs.toggle_checked(address_tab, true);
                $('.js-add-address, .js-create-address').addClass('disabled').prop('disabled', 'disabled');
                this.update_send_btn();
            }else{
                console.log("address not created. Error : %s", response.error);
            }
            
        }, function(reason){
            console.error(reason);
        });
    }

    Checkout.prototype.update_payment_method = function(){
        //this.payment_option = parseInt($('.js-input-payment-option').val());
        var methods = PAYMENT_OPTION_METHODS_MAPPING.get(parseInt(this.payment_option));
        var li_list = $(PAYMENT_METHOD_CONTAINER + " li");
        li_list.hide();
        $('input', li_list).each(function(){
            this.checked = false;
        });
        if(methods){
            methods.forEach(function(value, index){
                $(LI_PM_PREFIX + value, PAYMENT_METHOD_CONTAINER).show();
            });
        }
        this.update_send_btn();
        
    };
    Checkout.prototype.validate_shipmode = function(){
        var shipmde_container = $('#step-' + shipmode_tab);
        var $selectec_ship_mode = $('.js-input-ship-mode:checked')
        var $input = $("input[type='radio']:checked", shipmde_container);
        tabs.toggle_checked(shipmode_tab, is_valid);
        return is_valid;
    };

    Checkout.prototype.ship_mode_changed = function(el){
        this.ship_mode = parseInt($(el).data('mode'));
        this.ship_mode_valid = SHIP_IN_HOUSE.includes(this.ship_mode) || SHIP_IN_STORE.includes(this.ship_mode);
        //var shipping_price_el = $('.js-shipping-price');
        //var grand_total_el = $('.js-grand-total');
        //var total_el = $('.js-final-price');
        this.sub_total = parseInt($('.js-final-price').text());
        this.shipping_price = parseInt($(el).data('price'));
        //total += shipping_price;
        this.total = this.sub_total + this.shipping_price;
        $('.js-shipping-price').text(this.shipping_price);
        $('.js-grand-total').text(this.total);
        this.address_required = SHIP_IN_HOUSE.includes(this.ship_mode);
        $('.js-add-address').toggle(this.address_required);
        $('#address-container').toggle(this.address_required);
        $('.js-no-address-required').toggleClass('hidden', this.address_required);
        tabs.toggle_checked(shipmode_tab, true);
        this.validate_address();
        this.update_send_btn();
    };
    
    return Checkout;
    
});