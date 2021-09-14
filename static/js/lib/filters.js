
var order_status_container;
var order_payment_option_container;
var order_status = [];
var filter_form;

function clean_form_before_submit(form){
    $('.filter-input', form).each(function(){
        this.disabled = this.value == "";
    });
    $('.no-submit', form).each(function(){
        this.disabled = true;
    });
}

function filter_singular_init(field_id, chips_class){
    var input = $(field_id);
    var selected_chips = $(chips_class);
    var values = ""
    selected_chips.each(function(index, element){
        var chips = $(this);
        if(index < selected_chips.length - 1){
            values += chips.data('value') + ",";
        }else{
            values += chips.data('value');
        }
    });
    input.val(values);
}

function initialize_filters(){
    filter_singular_init('#order-status-input', '.order-status-chips.chips-selected');
    filter_singular_init('#order-payment-option-input', '.order-payment-option-chips.chips-selected');
}


function integer_field_filter(element){
    var values = "";
    var input_target = $('#' + element.data('target'));
    var filter_type = element.data('type');
    var parent = element.parent();
    if (filter_type == "selection"){
        element.toggleClass('chips-selected', !element.hasClass('chips-selected'));
        var selected_chips = $('.chips-selected', parent);
        selected_chips.each(function(index, element){
            var chips = $(this);
            if(index < selected_chips.length - 1){
                values += chips.data('value') + ",";
            }else{
                values += chips.data('value');
            }
        });
        

    }else if(filter_type == "range-start" || filter_type == "range-end"){
        var start;
        var end;
        if(filter_type == 'range-start'){
            start = element.val();
            end = $('#' + element.data('range-next')).val();
        }else if(filter_type == 'range-end'){
            end = element.val();
            start = $('#' + element.data('range-next')).val();
        }
        if(start != "" || end != ""){
            values = start + '-' + end;
        }

    }else if (filter_type == "value"){
        values = element.val();
    }
    input_target.val(values);

}

function install_integer_filter(){
    $('.js-list-filter').on('click', function(){
        integer_field_filter($(this));
    });
    $('.js-range-filter,.js-value-filter').on('keyup change', function(){
        integer_field_filter($(this));
    });
    /*
    $('.js-value-filter').on('keyup,change', function(){
        integer_field_filter($(this));
    });
    */
}

function toggle_order_status(element){
    var value = element.data('value');
    var added = false;
    var status_input = $('#order-status-input');
    var current_value = status_input.val();
    var values = ""
    element.toggleClass('chips-selected', !element.hasClass('chips-selected'));
    var selected_chips = $('.order-status-chips.chips-selected');
    selected_chips.each(function(index, element){
        var chips = $(this);
        if(index < selected_chips.length - 1){
            values += chips.data('value') + ",";
        }else{
            values += chips.data('value');
        }
        added = true;
    });
    status_input.val(values);
    return added;
}

function toggle_playment_option(element){
    var value = element.data('value');
    var added = false;
    var input = $('#order-payment-option-input');
    var current_value = input.val();
    var values = ""
    element.toggleClass('chips-selected', !element.hasClass('chips-selected'));
    var selected_chips = $('.order-payment-option-chips.chips-selected');
    selected_chips.each(function(index, element){
        var chips = $(this);
        if(index < selected_chips.length - 1){
            values += chips.data('value') + ",";
        }else{
            values += chips.data('value');
        }
        added = true;
    });
    input.val(values);
    return added;
}


function toggle_amount_option(element){
    var input = $('#amount-filter');
    var filter_action = element.data('value');
    var added = false;
    if(input.val() == filter_action){
        //element.removeClass('chips-selected').siblings().removeClass('chips-selected');
        input.val('');
    }else{
        input.val(filter_action);
        added = true;
        //element.addClass('chips-selected').siblings().removeClass('chips-selected');
    }
    $(".amount-filter-chips .chips").removeClass('chips-selected');
    return added;
}

function toggle_date_filter(element){
    var input = $('#filter-action');
    var filter_action = element.data('filter-action');
    if(input.val() == filter_action){
        element.removeClass('chips-selected').siblings().removeClass('chips-selected');;
        input.val('');
    }else{
        input.val(filter_action);
        element.addClass('chips-selected').siblings().removeClass('chips-selected');
    }
}

$(document).ready(function(){
    filter_form = $('#filter-form');
    $('#filter-form').on('submit', function(event){
        $('input[name="csrfmiddlewaretoken"]').prop('disabled', true);
        clean_form_before_submit(this);
    });
    $('.js-pagination').on('click', function(event){
        
        if(filter_form.length != 0){
            event.preventDefault();
            event.stopPropagation();
            
            var page = $(event.target).data('page');
            var input = $('<input />', {
                name : 'page',
                value : page
            });
            input.appendTo(filter_form);
            filter_form.submit();
        }
        

    });

    $("#amount-filter-input").on('keyup', function(event){
        var input = $(this);
        $(input.data('update')).text(input.val());
        $("#" + input.data('target')).val(input.val());
    });
    initialize_filters();
    install_integer_filter();
});