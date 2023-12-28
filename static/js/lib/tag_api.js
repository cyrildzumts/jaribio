
define([], function() {
    'use strict';
    var element_factory = {
        create_tag : function(option){
            let element = document.createElement(option.element);
            if(!option.hasOwnProperty('options')){
                return element;
            }
            let options = option.options;
            for(const [key, value] of Object.entries(options)){
                if((key == 'cls') && value.length){
                    value.split(' ').forEach(cls =>{
                        element.classList.add(cls);
                    });
                }else if(key == 'children'){
                    value.forEach(child =>{
                        element.appendChild(child);
                    });
                    
                }else if(key == 'child'){
                    element.appendChild(value);
                }else if(key.startsWith('data-')){
                    element.setAttribute(key, value);
                }else{
                    element[key] = value;
                }
            }
            return element;
        }
    };
    return element_factory;
    
});
