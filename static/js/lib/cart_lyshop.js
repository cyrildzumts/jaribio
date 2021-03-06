
define(['ajax_api', 'lang', 'accounts'], function(ajax_api, Locale, accounts) {
    'use strict';
    
    //accounts.init();
    var user = {};
    var customer = - 1;
    // accounts.set_callback(function(obj){
    //     user = obj;
    //     customer = user.user_id;
    // });

    function Cart(){
        this.user = "";
        this.items = [];
        this.total = 0;
        this.customer = {};
        this.csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        this.cart_container = null;
        this.add_to_cart_form = null;
    }

    Cart.prototype.init = function(){
        if(!this.csrfmiddlewaretoken || !this.csrfmiddlewaretoken.value){
            console.warn("no csrf_token found");
            return;
        }
        this.cart_container = document.getElementById('cart');
        this.cart_container = document.getElementById('add-cart-form');
        if(!(this.cart == null || this.add_to_cart_form == null)){
            return;
        }
        var self = this;
        this.customer = document.querySelector('#cart-customer');
        if(this.customer){
            customer = this.customer.value;
        }
        $('.js-cart-update-item-quantity,.js-cart-delete-item').on('click', function(){
            var item = $(this);
            var obj = {};
            obj['action'] = item.data('action');
            obj['target'] = $('#' + item.data('target'));
            obj['update'] = $('#' + item.data('update'));
            obj['parent'] = $('#' + item.data('parent'));
            obj['cart_total'] = $('.js-cart-total');
            obj['cart_quantity'] = $('.js-cart-quantity');
            obj['item_uuid'] = item.data('item');
            self.update_product(obj);
        });

        $('#add-cart-form').submit(function(event){
            event.stopPropagation();
            event.preventDefault();
            var variant = $('#variant').val();
            var is_valid = variant.length > 0;
            $('.js-selection-required').toggleClass('hidden', is_valid);
            if(is_valid){
                self.add($(this).serialize(), $('#product-name', this).val());
            }
        });
        $('.js-cart-item-quantity').on('keypress', function(e){
            if(e.which != 13){
                return;
            }
            var item = $(this);
            self.update_product_quantity(item.data('item'), item.val(), item);
        });
        $('.js-attr-select').on('click', function(event){
            var element = $(this);
            var input = $('#' + element.data('target'));
            var was_selected = element.hasClass('chips-selected');
            
            element.toggleClass('chips-selected', !was_selected).siblings().removeClass('chips-selected');
            if(!was_selected){
                input.val(element.data('value'));
                $('.js-selection-required').toggleClass('hidden', !was_selected);
            }else{
                input.val('');
            }
            
        });
        $('.js-add-coupon').on('click', self.addCoupon.bind(this));
        $(".js-remove-coupon").on('click', self.removeCoupon);
    }

    Cart.prototype.set_user = function(obj){
        user = obj;
        customer = user.user_id;
    }

    Cart.prototype.add = function(formData, product_name){
        var self = this;
        if(!formData){
            return;
        }
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/api/add-to-cart/',
            data : formData
        }
        
        ajax_api.ajax(option).then(function(response){
            self.update_badge(response.quantity);
            notify({level:response.success? 'info': 'error', content: response.message});
        }, function(reason){
            console.error(reason);
            notify({level:'warn', content:'product could not be added'});
        });
    }

    Cart.prototype.remove = function(product){
        if(!this.csrfmiddlewaretoken || !this.csrfmiddlewaretoken.value){
            console.warning("Cart add oporation not allowed: csrf_token missing");
            return;
        }
        console.log("Removing product from cart");
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/cart/ajax_cart_item_delete/' + product.product_uuid + '/',
            data : {'csrfmiddlewaretoken': this.csrfmiddlewaretoken.value, 'item_uuid': product.product_uuid}
        }
        ajax_api(option).then(function(response){
            self.update_badge(response.quantity);
            notify({level:response.success? 'info': 'error', content: response.error});
        }, function(reason){
            console.error(reason);
            notify({level:'warn', content:'product could not be removed'});
        });
    }

    Cart.prototype.putInWishlist = function(product_uuid){
        if(!this.csrfmiddlewaretoken || !this.csrfmiddlewaretoken.value){
            console.warning("csrf_token missing");
            return;
        }
    }

    Cart.prototype.clear = function(){
        if(!this.csrfmiddlewaretoken || !this.csrfmiddlewaretoken.value){
            console.warning("csrf_token missing");
            return;
        }
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/api/clear-cart/',
            data : {'csrfmiddlewaretoken': this.csrfmiddlewaretoken.value}
        }
        ajax_api(option).then(function(response){
            self.update_badge(0);
            notify({level:response.success? 'info': 'error', content: response.error});
        }, function(reason){
            console.error(reason);
            notify({level:'warn', content:'your cart could ne be cleared'});
        });
    }

    Cart.prototype.addCoupon = function(){
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        var coupon = $('#coupon').val();
        if(coupon.length == 0 || csrfmiddlewaretoken.length == 0){
            console.error("invalid coupon");
            return;
        }
        this.isValidCoupon(coupon, function(response){
            $("#coupon-error").toggle(!response.valid);
            if(response.status && response.valid){
                
                var option = {
                    type:'POST',
                    method: 'POST',
                    dataType: 'json',
                    url : '/api/add-to-coupon/',
                    data : {coupon : coupon, csrfmiddlewaretoken : csrfmiddlewaretoken}
                }
                ajax_api.ajax(option).then(function(response){
                    if(response.added){
                        $(".original-price").text(response.subtotal);
                        $(".final-price").text(response.total);
                        $(".js-cart-reduction").text(response.reduction);
                        $(".js-add-coupon").hide().siblings(".js-remove-coupon").show();
                        $("#coupon").prop('disabled', true).toggleClass('disabled');
                        notify({level:'info', content:'coupon added'});
                    }else{
                        notify({level:'info', content:'coupon could not be added'});
                    }
                    
                }, function(reason){
                    notify({level:'info', content:'coupon could not be added'});
                    console.error("Error on adding Coupon \"%s\" to user cart", coupon);
                    console.error(reason);
                });
            }else if(response.status && !response.valid){
                setTimeout(()=>{
                    $("#coupon-error").fadeOut(600);
                }, 5000);
                console.log("invalid coupon : %s", coupon);
            }
            
        });
    }
    

    Cart.prototype.removeCoupon = function(){
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        if(!csrfmiddlewaretoken){
            console.warning("Cart remove oporation not allowed: csrf_token missing");
            return;
        }
        var coupon = $('#coupon');
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/api/remove-coupon/',
            data : {coupon: coupon.val(), csrfmiddlewaretoken : csrfmiddlewaretoken}
        }
        ajax_api.ajax(option).then(
            function(response){
                var data = response;
                if(response.removed){
                    coupon.prop('disabled', false).removeClass('disabled', false).val('');
                    $(".original-price").text(response.subtotal);
                    $(".final-price").text(response.total);
                    $(".js-cart-reduction").text(response.reduction);
                    $(".js-add-coupon").show().siblings(".js-remove-coupon").hide();
                    notify({level:'info', content:'coupon removed'});
                }else{
                    notify({level:'warn', content:'Coupon not removed'});
                }
                //document.location.reload();
            }, 
            function(error){
                notify({level:'warn', content:'error on checking the coupon'});
            });

    }

    Cart.prototype.isValidCoupon = function(coupon, callback){
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        if(!csrfmiddlewaretoken){
            console.warning("Cart add oporation not allowed: csrf_token missing");
            return;
        }
        console.log("Verifying coupon ", coupon);
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/api/verify-coupon/',
            data : {coupon : coupon, csrfmiddlewaretoken : csrfmiddlewaretoken}
        }
        ajax_api.ajax(option).then(
            function(response){
                if(typeof callback == "function"){
                    callback(response);
                }
            }, 
            function(error){
                if(typeof callback == "function"){
                    callback(error);
                }
            });
    }

    Cart.prototype.update_product = function(to_update){
        var self = this;
        var data = {
            "csrfmiddlewaretoken"   : this.csrfmiddlewaretoken.value,
            //"quantity"              : to_update['quantity'],
            "action"                :  to_update['action'],
            "item"                  : to_update['item_uuid'],
            "customer"              : customer
        };
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            //url : '/cart/ajax-cart-item/' + data['item'] + '/' + data['action'] + '/',
            url : '/api/update-cart-item/',
            data : data
        }
        ajax_api.ajax(option).then(function(response){
            self.update_badge(response.count);
            if(!response.success){
                notify({level:'error', content:response.error});
                return;
            }
            if(response.count == 0){
                document.location.reload();
                return ;
            }
            if(response['removed']){
                to_update.parent.fadeOut('slow').remove()
            }else{
                to_update.target.val(response['item_quantity']);
                to_update.update.html(response['item_total']);
            }
            $(".original-price").text(response.subtotal);
            $(".final-price").text(response.total);
            $(".js-cart-quantity").text(response.count);
            $(".js-cart-reduction").text(response.reduction);
            notify({level:'info', content:'cart updated'});
            //to_update.cart_total.html(response['cart_total']);
            //to_update.cart_quantity.html(response['count']);            
            
        }, function(reason){
            console.error(reason);
        });
    }

    Cart.prototype.update_product_quantity = function(item_uuid, quantity, target){
        var data = {};
        data['csrfmiddlewaretoken'] = this.csrfmiddlewaretoken.value;
        data['quantity'] = quantity;
        data['action'] = 'update';
        data['item_uuid'] = item_uuid;
        data['customer'] = customer;
    
        var option = {
            type:'POST',
            method: 'POST',
            dataType: 'json',
            url : '/cart/ajax-cart-item-update/',
            data : data
        }
        ajax_api.ajax_lang(option).then(function(response){
            if(response['item_quantity'] == 0){
                $('#' + target.data('parent')).fadeOut('slow').remove();
            }else{
                target.val(response['item_quantity']);
                $('#' + target.data('total')).html(response['item_total']);
            }
    
            $(".original-price").text(response.subtotal);
            $(".final-price").text(response.total);
            $(".js-cart-quantity").text(response.count);
            $(".js-cart-reduction").text(response.reduction);
            this.update_badge(response.count);
            notify({level:'info', content:'cart updated'});
            
        }, function(reason){
    
            console.error(reason);
            target.val(reason.responseJSON['item_quantity']);
            notify({level:'warn', content:'cart could not be updated'});
        });
    }

    Cart.prototype.update_badge = function(quantity){
        $('.cart .js-cart-count').text(quantity);
    }

    return Cart;
});