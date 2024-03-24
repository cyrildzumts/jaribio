define(['tag_api'],function(tag_api) {
    'use strict';
    let filter_instance;

    function clean_form_before_submit(form){
        let filter_inputs = $('.filter-input', form);
        filter_inputs.each(function(){
            this.disabled = this.value == "";
        });
        $('.no-submit', form).each(function(){
            this.disabled = true;
        });
        let valid_inputs = filter_inputs.filter(function(){
            return this.value != "";
        });
        return valid_inputs.length == 0;
    }
    
    function filter_singular_init(field_id, chips_class){
        let input = document.getElementById(field_id);
        if(!input){
            return;
        }
        let selected_chips = document.querySelectorAll(chips_class);
        let values = ""
        selected_chips.forEach(function(element, index){
            if(index < selected_chips.length - 1){
                values += element.dataset.value + ",";
            }else{
                values += element.dataset.value;
            }
        });
        input.value = values;
    }
    
    function initialize_filters(){
        filter_singular_init('order-status-input', '.order-status-chips.chips-selected');
        filter_singular_init('order-payment-option-input', '.order-payment-option-chips.chips-selected');
    }
    
    
    function integer_field_filter(element){
        let values = "";
        let input_target = document.getElementById(element.dataset.target);
        if(!input_target){
            return;
        }
        let filter_type = element.dataset.type;
        let container = document.getElementById(input_target.dataset.container);
        if (filter_type == "selection"){
            element.classList.toggle('chips-selected', !element.classList.contains('chips-selected'));
            let selected_chips = container.querySelectorAll('.chips-selected');
            selected_chips.forEach(function(el, index){
                if(index < selected_chips.length - 1){
                    values += el.dataset.value + ",";
                }else{
                    values += el.dataset.value;
                }
            });
        }else if(filter_type == "range-start" || filter_type == "range-end"){
            let start="";
            let end="";
            if(filter_type == 'range-start'){
                start = element.value;
                end = document.getElementById(element.dataset.rangeNext).value;
            }else if(filter_type == 'range-end'){
                end = element.value;
                start = document.getElementById(element.dataset.rangeNext).value;
            }
            if(start.length || end.length){
                values = start + '-' + end;
            }
    
        }else if (filter_type == "value"){
            values = element.value;
        }
        input_target.value = values;
    
    }
    
    function install_integer_filter(){
        $('.js-list-filter').on('click', function(){
            integer_field_filter(this);
        });
        $('.js-range-filter,.js-value-filter').on('keyup change', function(){
            integer_field_filter(this);
        });
    }
    var ListFilter = (function(){
        function ListFilter(){

        };

        ListFilter.prototype.init = function(){
            let self = this;
            $('.js-filter-btn').on('click', function(event){
                var ctx = $('#' + this.dataset.context);
                var input_name = this.dataset['input-name'];
                var container = $('#' + this.dataset.container);
                var filter_field = this.dataset["filter-field"];
                var value_list = [];
                $("input:checked[name=\"" + input_name + "\"]", ctx).each(function(){
                    value_list.push(this.dataset.value);
                });
                self.filter(container, filter_field, value_list);
            });
        
            $('.js-filter-reset-btn').on('click', function(event){
                var ctx = $('#' + this.dataset.context);
                var container = $('#' + this.dataset.container);
                self.reset_filter(ctx, container);
            });
        };

        ListFilter.prototype.filter = function(ctx, filter_field, value_list){
            if(!ctx || !filter_field || !value_list || value_list.length == 0){
                console.log("Filter called with missing argumtent");
                return;
            }
            $(".filterable", ctx).each(function(index, element){
                let filter_value = this.dataset[filter_field];
                $(this).toggle(value_list.includes(filter_value));
            });
        };

        ListFilter.prototype.reset_filter = function(ctx, container){
            if(!ctx || !container){
                console.log(" Reset Filter called with missing context");
                return;
            }
            $("input:checkbox", ctx).each(function(){
                this.checked = false;
            });
            $(".filterable", container).each(function(index, element){
                $(this).show();
            });
        };

        return ListFilter;
    })();
    let list_filter = {
        init : function(){
            $('.js-list-filter').on('keyup', function(event){
                event.stopPropagation();
                let input = event.target;
                let value = input.value.trim().toLowerCase();
                let fields = input.dataset.fields.split(' ');
                let target = document.getElementById(input.dataset.target);
                let node;
                let collection = target.children;
                let included = false;
                for(let index = 0; index < collection.length; index++){
                    node = collection[index];
                    for(let f of fields){
                        included = node.dataset[f].toLowerCase().includes(value);
                        if(included) break;
                    }
                    node.classList.toggle('hidden', !included); 
                }
            });
            filter_instance = new ListFilter();
            filter_instance.init();
            let filter_form = $('#filter-form');
            initialize_filters();
            install_integer_filter();
            filter_form.on('submit', function(event){
                $('input[name="csrfmiddlewaretoken"]').prop('disabled', true);
                let reload = clean_form_before_submit(this);
                if(reload){
                    event.stopPropagation();
                    event.preventDefault();
                    window.location.search = "";
                    window.location = location.pathname;
                }
            });
            $('.js-pagination').on('click', function(event){
                
                if(filter_form.length != 0){
                    event.preventDefault();
                    event.stopPropagation();
                    
                    let page = $(event.target).data('page');
                    let input = tag_api.create_tag({'element': 'input', 'options': {'cls': 'filter-input', 'name': 'page', 'value': page,'type':'text','id':'page'}});
                    filter_form.append(input)
                    filter_form.submit();
                }
            });
        }
    };
    return list_filter;
});