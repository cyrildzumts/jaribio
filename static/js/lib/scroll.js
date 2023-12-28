define([], function(){
    'use strict';
    let scrollLeft;
    let scrollRight;
    let windowsWidth;
    const SCROLL_BEHAVIOR = "smooth";
    const EASE = 0.05;
    var scroll_tools = {
        init : function(){
            let self = this;
            scrollLeft = document.querySelectorAll('.js-scroll-left');
            scrollRight = document.querySelectorAll('.js-scroll-right');
            let scrollables = document.querySelectorAll('.scroll');
            if(scrollables){
                scrollables.forEach(function(el, index, list){
                    if(el.scrollWidth <= el.clientWidth){
                        let scrollbar = el.parentElement.querySelector('.scroll-bar');
                        if(scrollbar){
                            scrollbar.style.display = 'none';
                        }
                    }
                });
            }
            if (scrollRight){
                scrollRight.forEach((element, index, list)=>{
                    element.addEventListener('click', (event)=>{
                        let scrollElement = element.parentElement.parentElement.querySelector('.scroll');
                        if(scrollElement.scrollWidth > scrollElement.clientWidth){
                            let item = scrollElement.children[0];
                            let visibleItems = scrollElement.clientWidth / item.clientWidth;
                            scrollElement.scroll({top:0, left: (scrollElement.scrollLeft + (item.clientWidth * visibleItems)), behavior:SCROLL_BEHAVIOR});
                        }
                    });
                });
            }
            if (scrollLeft){
                scrollLeft.forEach((element, index, list)=>{
                    element.addEventListener('click', (event)=>{
                        let scrollElement = element.parentElement.parentElement.querySelector('.scroll');
                        if(scrollElement.scrollWidth > scrollElement.clientWidth){
                            let item = scrollElement.children[0];
                            let visibleItems = scrollElement.clientWidth / item.clientWidth;
                            scrollElement.scroll({top:0, left: (scrollElement.scrollLeft - (item.clientWidth * visibleItems)), behavior:SCROLL_BEHAVIOR});
                        }
                    });
                });
            }
        },
        animate: function(){

        },

        setTransform : function(el, transform){
            el.style.transform = transform;
        },
        lerp : function(start, end, t){
            return start *(1-t) + end *t;
        }
    };
    return scroll_tools;
});