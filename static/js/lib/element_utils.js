
define([], function() {
    'use strict';
    var element_factory = {
        create_input : function(option){
            let input = document.createElement('input');
            if(option.cls.length){
                option.cls.split(' ').forEach(cls =>{
                    input.classList.add(cls);
                });
            }
            input.id = option.id;
            input.type = option.type;
            input.value = option.value;
            input.name = option.name;
            if(option.hasOwnProperty('checked')){
                input.checked = option.checked;
            }
            return input;
        },
        create_label : function(option){
            let label = document.createElement('label');
            label.htmlFor = option.input_id;
            label.innerText = option.value;
            return label;
        },
        create_option : function(option){
            let select_option = document.createElement('option');
            select_option.value = option.value;
            select_option.selected = option.selected;

            return select_option;
        },
        create_select : function(option){
            let select = document.createElement('select');
            select.name = option.name;
            select.id = option.id;
            select.multiple = option.multiple;
            option.options.forEach(opt => {
                select.appendChild(opt);
            });
            return select;
        },
        create_li : function(option){
            let li = document.createElement('li');
            if(option.cls.length){
                option.cls.split(' ').forEach(cls =>{
                    li.classList.add(cls);
                });
            }
            if(option.hasOwnProperty('child')){
                li.appendChild(option.child);
            }
            return li;
        },
        create_ul : function(option){
            let ul = document.createElement('ul');
            if(option.cls.length){
                option.cls.split(' ').forEach(cls =>{
                    ul.classList.add(cls);
                });
            }
            if(option.hasOwnProperty('children')){
                option.children.forEach(child =>{
                    ul.appendChild(child);
                });
            }
            return ul;
        },
        create_element : function(option){
            let el = document.createElement(option.element);
            if(option.cls.length){
                option.cls.split(' ').forEach(cls =>{
                    el.classList.add(cls);
                });
            }
            if(option.hasOwnProperty('children')){
                option.children.forEach(child =>{
                    el.appendChild(child);
                });
            }
            return el;
        },
        
        init : function(){
            console.log("Element Utils ready");
        }

    };
    return element_factory;
    
});
