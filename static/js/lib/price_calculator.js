define(function() {
    'use strict';

    var DEFAULT_PERCENT = 50;
    var PERCENT_STEP = 10;
    var MAX_PERCENT = 100;
    var MINUM_PERCENT = 20;
    var EURO_TO_XAF = 655.95;
    var DEFAULT_SHIP_IT_PRICE = 13;
    var CURRENT_PERCENT;
    var SHIP_IT_PRICE;
    var PERCENT_LIST = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    return {
        init : function(){
            var current = document.querySelector('input#current-percent');
            var ship_it = document.querySelector('input#ship-it');
            if(current){
                CURRENT_PERCENT = current.value;
            }else{
                CURRENT_PERCENT = DEFAULT_PERCENT;
            }
            if(ship_it){
                SHIP_IT_PRICE = ship_it.value;
            }else{
                SHIP_IT_PRICE = DEFAULT_SHIP_IT_PRICE;
            }
            var self = this;
            $('#percent,#ship-it,#calc-price,#currency').on('keyup change', this.updateCalculator.bind(this));
            $('#ship-it,#start_price, #end_price,#currency').on('keyup change', this.update_price_table.bind(this));
        },
        calculate : function(price, ship_it, percent){
            if(typeof price != "number"){
                return -1;
            } 
            let t_price = price + ship_it;
            return (t_price * (1 + percent/100));
        },

        calculate_with_percent : function(price, percent){
            if(typeof price != "number"){
                return -1;
            } 
            let t_price = price + SHIP_IT_PRICE;
            return (t_price * (1 + percent/100));
        },

        toXAF : function(price, ship_it, percent){
            let total = this.calculate(price, ship_it, percent);
            return total > 0 ? total * EURO_TO_XAF : total;
        },
        update_price_table : function(){
            var self = this;
            var ship_it = parseFloat(document.querySelector('#ship-it').value);
            var start_price = parseFloat(document.querySelector('#start_price').value);
            var end_price = parseFloat(document.querySelector('#end_price').value);
            var currency = parseFloat(document.querySelector('#currency').value);
            if(!ship_it || !start_price || !end_price || !currency ){
                return;
            }
            var prices_list = [];
            var tbody = document.querySelector('#price-table tbody');
            document.querySelectorAll('#price-table tbody tr').forEach((e) =>{e.remove()});
            for(let p = start_price; p <= end_price; p++){
                var entry = [];
                entry.push(p);
                entry.push(p + ship_it);
                PERCENT_LIST.forEach((v)=>{
                    entry.push(Math.ceil(self.toXAF(p, ship_it, v)));
                });
                prices_list.push(entry);
            }
            prices_list.forEach((r)=>{
                self.insertRow(r, tbody);
            });
        },

        calculateTable : function(start_price, end_price, ship_it_price){

            
        },
        insertRow : function(row, tbody){
            //var tbody = document.querySelector('#price-table tbody');
            var tr = document.createElement('tr');
            row.forEach((p)=>{
                var td = document.createElement('td');
                td.innerText = p;
                tr.appendChild(td);

            });
            tbody.appendChild(tr);
        },

        updateCalculator : function(){
            var self = this;
            var percent = parseFloat(document.querySelector('#percent').value);
            var ship_it = parseFloat(document.querySelector('#ship-it').value);
            var price = parseFloat(document.querySelector('#calc-price').value);
            var currency = parseFloat(document.querySelector('#currency').value);
            if(!percent || !ship_it || !price || !currency ){
                return;
            }
            var selling_price = document.querySelector('input#calc-selling-price');
            var selling_price_xaf = document.querySelector('input#calc-selling-price-xaf');
            var min_selling_price_xaf = document.querySelector('input#calc-min-selling-price-xaf');
            let total = this.calculate(price, ship_it, percent);
            let total_xaf = Math.floor(total * currency);
            selling_price.value = total;
            selling_price_xaf.value = total_xaf;
            min_selling_price_xaf.value = Math.ceil((price + ship_it) * EURO_TO_XAF);

            var tbody = document.querySelector('#simple-price-table tbody');
            document.querySelectorAll('#simple-price-table tbody tr').forEach((e) =>{e.remove()});
            var entries = [];
            PERCENT_LIST.forEach((v)=>{
                entries.push(Math.ceil(self.toXAF(price, ship_it, v)));
            });
            self.insertRow(entries, tbody);
        }

    };
    
});