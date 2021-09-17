define(['ajax_api','element_utils'], function(ajax_api, element_utils) {
    'use strict';
    var fileUpload;
    var productManager;
    let quizManager;
    let quizstepManager;
    let questionManager;
    var messages;
    var notification_wrapper;
    var fadeDelay = 5000; // 5s
    var AVAILABILITY_ON_DEMAND = 1;
    
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

    function notify(message){
        if( typeof notification_wrapper === 'undefined' || typeof messages === 'undefined'){
            console.warn("Notify call for message %s. But There is no messages container", message);
            return;
        }
        let li = $('<li />', {
            "class" : message.level,
        });
        let div = $('<div />', {
            "class" : "notification flex"
        });
        div.append($('<i />', {
            "class" : "fas fa-info-circle icon"
        })).append($('<span />', {
            'text': message.content
        })).appendTo(li);
        li.appendTo(messages);
        //let top = notification_wrapper.offset().top - $(window).scrollTop();
        notification_wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            messages.empty();
        });
    }

    function notify_init(wrapper, message_container){
    
        if(typeof wrapper === 'undefined'){
            return;
        }

        if(typeof message_container === 'undefined' || $('li', message_container).length == 0){
            return;
        }

        wrapper.fadeIn().delay(fadeDelay).fadeOut('slow', function () {
            message_container.empty();
        });
    }

    function input_check_max_limit(input){
        var $input = $(input);
        var max_len = parseInt($input.data('max-length'));
        var len = $input.val().length;
        var target = $($input.data('target'));
        var max_len_reached = len > max_len;
        $input.toggleClass("warning", max_len_reached);
        target.toggleClass("danger", max_len_reached).text(len);
    }

    function track_action(track_element){
        let csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        let url = '/api/track-actions/';
        let action = parseInt(track_element.dataset.action);
        let options = {
            url : url,
            type: 'POST',
            data : {'action': action, 'csrfmiddlewaretoken': csrfmiddlewaretoken.value},
            dataType : 'json',
            async:false,
            cache : false,

        };
        ajax_api.ajax(options).then(function(response){
            
        }, function(reason){
            console.error(reason);
        });
    }


    var ListFilter = (function(){
        function ListFilter(){
            this.init();
            console.log("ListFilter instance created");
        };

        ListFilter.prototype.init = function(){
            console.log("ListFilter instance initializing");
            var self;
            $('.js-list-filter').on('keyup', function(event){
                event.stopPropagation();
                var value = this.value.trim().toLowerCase();
                var fieldname = $(this).data('field');
                var target = $("#" + $(this).data('target'));
                
                target.children().filter(function(){
                    self = $(this)
                    self.toggle(self.data(fieldname).toLowerCase().includes(value));
                });
            });

            console.log("ListFilter instance initialized");
        };

        ListFilter.prototype.filter = function(ctx, filter_field, value_list){
            if(!ctx || !filter_field || !value_list || value_list.length == 0){
                console.log("Filter called with missing argumtent");
                return;
            }
            console.log("Filtering started");
            $(".filterable", ctx).each(function(index, element){
                let filter_value = this.getAttribute(filter_field);
                console.log(" Filter Field = \"%s\" - Filter Value = \"%s\" - Value List = [\"%s\"]", filter_field ,filter_value, value_list)
                $(this).toggle(value_list.includes(filter_value));
            });
            console.log("Listfilter : filter run with success");
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
            console.log("Listfilter : reset run with success");
        };

        return ListFilter;
    })();

    function clear_uploaded_files(){
        var files_container = document.querySelector('.file-list');
        var input_files = document.querySelector('#files');
        input_files.value = null;
        while(files_container.firstChild){
            files_container.removeChild(files_container.firstChild);
        }
        $('.js-uploaded-files-clear').hide();
    }
    function show_preview(files) {
        var files_container = document.querySelector('.file-list');
        var li;
        var img;
        while(files_container.firstChild){
            files_container.removeChild(files_container.firstChild);
        }
        console.log("files : ", files);
        var f;
        for(var i = 0; i < files.length; i++){
            f = files[i];
            li = document.createElement('li');
            img = document.createElement('img');
            img.src = URL.createObjectURL(f);
            img.height = 60;
            files_container.appendChild(li);
            img.onload = function(){
                URL.revokeObjectURL(img.src);
            };
            li.classList.add('file-entry');
            li.appendChild(img);
            const info = document.createElement('span');
            info.innerHTML = f.name + " : " + f.size + ' bytes';
            li.appendChild(info);
        }
    }

    function onDragInit(){
        var droppedFiles;
        var dragarea = document.querySelector('.drag-area');
        if(!dragarea){
            console.log("no drag-area could be found");
            return;
        }
        var $form = $('#' + dragarea.dataset.form);
        $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
            e.preventDefault();
            e.stopPropagation();
        }).on('dragover dragenter', function(){
            dragarea.classList.add('on-drag');
        }).on('dragleave dragend drop', function(){
            dragarea.classList.remove('on-drag');
        }).on('drop', function(e){
            droppedFiles = e.originalEvent.dataTransfer.files;
            var input_files = document.querySelector('#files');
            console.log("Droped file : ", droppedFiles);
            console.log("Input file : ", input_files.files);
            input_files.files = droppedFiles;
            console.log("Input file 2 : ", input_files.files);
            show_preview(droppedFiles);
            $('.js-uploaded-files-clear').show();
            console.log("Files dropped : %s", droppedFiles.length);

        });
        $('.js-uploaded-files-clear').on('click', clear_uploaded_files);
    }

    function onDropHandler(event){
        event.preventDefault();
        var files = [];
        event.dataTransfer = event.originalEvent.dataTransfer;
        if(event.dataTransfer.items){
            var items = event.dataTransfer.items;
            for(var i = 0; i < items.length; i++){
                if(items[i].kind === 'file'){
                    var file = items[i].getAsFile();
                    fileUpload.addFile(file);
                }
            }
        }else{
            var files = event.dataTransfer.files;
            //fileUpload.setFiles(files);
            for(var i = 0; i < files.length; i++){
                //var file = files[i]
                fileUpload.addFile(files[i]);
            }
        }
        $('.drag-area').removeClass('on-drag');
    }


    function onDragOverHandler(event){
        event.preventDefault();
    }

    function onDragStartHandler(event) {
        $('.drag-area').addClass('on-drag');
        
    }
    function onDragEndHandler(event) {
        $('.drag-area').removeClass('on-drag');
        
    }

    function uploadFiles(form, files) {
        var formData = new FormData(form);
        files.forEach(function(file, index){
            formData.append("file_" + index, file, file.name);
        });
        $(form).serializeArray().forEach(function(input, index){
            formData.append(input.name, input.value);
        });
        var options = {
            url : $(form).attr('action'),
            type: 'POST',
            enctype : 'multipart/form-data',
            data : formData,
            processData : false,
            cache : false,
            contentType : false
        };
        ajax_api.ajax_lang(options, false).then(function(response){

        }, function(reason){

        });
        
    }

    var QuizManager = (function(){
        function QuizManager() {
            this.images = null;
            this.form = undefined;
            this.formData = undefined;
            this.input_file = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.quiz_container = undefined;
            this.quiz_link = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
        };
        QuizManager.prototype.init = function(){
            var self = this;
            this.form = document.querySelector('#quiz-form') || document.querySelector('#quiz-update-form');
            if(this.form == null ){
                console.warn("No quiz form found");
                return;
            }
            this.drag_area = document.querySelector('.drag-area');
            if(!this.drag_area){
                console.warn("No drag-area on quiz form found");
                return;
            }
            this.input_file = document.querySelector('#files');
            if(!this.input_file){
                console.warn("No image input on quiz form found");
                return;
            }
            this.quiz_container = document.querySelector('#created-producted-link');
            this.quiz_link = document.querySelector('#created-producted-link a');
            this.files_container = document.querySelector('.file-list');

            $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                self.drag_area.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                self.drag_area.classList.remove('on-drag');
            }).on('drop', function(e){
                self.images = e.originalEvent.dataTransfer.files;
                self.input_file.files = self.images;
                self.onImagesChanged();
                self.imagesPreview();

            });
            $('#files').on('change', function(e){
                self.images = self.input_file.files;
                self.onImagesChanged();
                self.imagesPreview();
            });
            $('.js-uploaded-files-clear').on('click', this.clearImages.bind(this));
            this.validators = [];
            
            $(this.form).on('submit', function(e){
                e.preventDefault();
                e.stopPropagation();
                self.formData = new FormData(self.form);
                self.upload();
            });

            console.log("QuizManager initialized");

        };

        QuizManager.prototype.imagesPreview = function(){
            let li;
            let img;
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            let f;
            for(let i = 0; i < this.images.length; i++){
                f = this.images[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                this.files_container.appendChild(li);
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                li.appendChild(info);
            }
            $('.js-uploaded-files-clear').show();
        };

        QuizManager.prototype.clearImages = function(){
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            this.images = null;
            this.input_file.files = null;
            let li = document.createElement('li');
            let span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            this.files_container.appendChild(li);
            this.onImagesChanged();
        };

        QuizManager.prototype.clear = function(){
            document.querySelector('#max_question').value = "";
            document.querySelector('#title').value = "";
            
            document.querySelector('#description').value = "";
            document.querySelector('#description-counter').innerText = '0';
            this.input_file.files = null;
            this.images = null;
            this.quiz_link.href = '';
            this.quiz_link.innerText = '';
            this.quiz_container.style.display = 'none';
            this.onImagesChanged();
        }

        QuizManager.prototype.is_update_form = function(){
            return this.form != null ? this.form.id == 'quiz-update-form' : false;
        }

        QuizManager.prototype.onImagesChanged = function(){
            this.drag_area.classList.toggle('active', this.images && (this.images.length > 0));
        };

        QuizManager.prototype.onUploadResponse = function(data){
            if(!data.success){
                
                return;
            }
            this.clear();
            this.quiz_link.href = data.url;
            this.quiz_link.innerText = data.url_text + " : " + data.name;
            this.quiz_container.style.display = 'flex';
        };

        QuizManager.prototype.upload = function(){
            let self = this;
            let form_is_valid = this.validate();
            if(!form_is_valid){
                console.log("Quiz form is invalid");
                return;
            }

            let url = this.is_update_form() ? '/api/update-quiz/' + this.form.dataset.quiz + '/' : '/api/create-quiz/';

            let options = {
                url : url,
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                dataType : 'json',
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                let msg = {
                    content : response.message,
                    level : response.created
                }
                notify(msg);
                self.onUploadResponse(response);
                self.clearImages();
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                self.clearImages();
            });
        };

        
        QuizManager.prototype.validate = function(){
            let title = document.querySelector('#title');
            let max_questions = document.querySelector('#max_questions');
            let description = document.querySelector('#description');
            let c_type = document.querySelector('.js-input-quiz-type:checked');
            
            let is_valid = true;

            if(max_questions == null || title == null || description == null){
                is_valid = false;
            }
            if(max_questions.value == ""){
                max_questions.classList.add('warn');
                is_valid = false;
            }else{
                max_questions.classList.remove('warn');
            }
            if(title.value == ""){
                title.classList.add('warn');
                is_valid = false;
            }else{
                title.classList.remove('warn');
            }
            if(description.value == ""){
                description.classList.add('warn');
                is_valid = false;
            }else{
                description.classList.remove('warn');
            }
            if(c_type == null){
                is_valid = false;
            }
            /*
            if((this.images == null || this.images.length == 0) && !this.is_update_form()){
                return false;
            }*/
            return is_valid;
        };

        return QuizManager;

    })();


    var QuestionManager = (function(){
        function QuestionManager() {
            this.images = null;
            this.form = undefined;
            this.formData = undefined;
            this.input_file = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.quiz_container = undefined;
            this.quiz_link = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
            this.answer_formset_total_form = "form-TOTAL_FORMS";
            this.answer_formset_initial_form = "form-INITIAL_FORMS";
        };
        QuestionManager.prototype.init = function(){
            var self = this;
            this.form = document.querySelector('#question-form') || document.querySelector('#question-update-form');
            if(this.form == null ){
                console.warn("No Question form found");
                return;
            }
            this.drag_area = document.querySelector('.drag-area');
            if(!this.drag_area){
                console.warn("No drag-area on quiz form found");
                return;
            }
            this.input_file = document.querySelector('#files');
            if(!this.input_file){
                console.warn("No image input on quiz form found");
                return;
            }
            this.quiz_container = document.querySelector('#created-producted-link');
            this.quiz_link = document.querySelector('#created-producted-link a');
            this.files_container = document.querySelector('.file-list');

            $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                self.drag_area.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                self.drag_area.classList.remove('on-drag');
            }).on('drop', function(e){
                self.images = e.originalEvent.dataTransfer.files;
                self.input_file.files = self.images;
                self.onImagesChanged();
                self.imagesPreview();

            });
            $('#files').on('change', function(e){
                self.images = self.input_file.files;
                self.onImagesChanged();
                self.imagesPreview();
            });
            $('.js-uploaded-files-clear').on('click', this.clearImages.bind(this));
            this.validators = [];
            
            $(this.form).on('submit', function(e){
                e.preventDefault();
                e.stopPropagation();
                self.formData = new FormData(self.form);
                self.upload();
            });
            $('.js-add-answer').on('click', function(event){
                self.add_response();
            });
            $('.js-clear-answers').on('click', function(){
                self.remove_responses();
            });

            console.log("QuestionManager initialized");

        };

        QuestionManager.prototype.imagesPreview = function(){
            let li;
            let img;
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            let f;
            for(let i = 0; i < this.images.length; i++){
                f = this.images[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                this.files_container.appendChild(li);
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                li.appendChild(info);
            }
            $('.js-uploaded-files-clear').show();
        };

        QuestionManager.prototype.clearImages = function(){
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            this.images = null;
            this.input_file.files = null;
            let li = document.createElement('li');
            let span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            this.files_container.appendChild(li);
            this.onImagesChanged();
        };

        QuestionManager.prototype.clear = function(){
            document.querySelector('#content').value = "";
            document.querySelector('#answer_count').value = "";
            document.querySelector('#score').value = "";
            document.querySelector('#explanation').value = "";
            document.querySelector('#description-counter').innerText = '0';
            this.input_file.files = null;
            this.images = null;
            this.quiz_link.href = '';
            this.quiz_link.innerText = '';
            this.quiz_container.style.display = 'none';
            this.onImagesChanged();
        }

        QuestionManager.prototype.is_update_form = function(){
            return this.form != null ? this.form.id == 'question-update-form' : false;
        }

        QuestionManager.prototype.onImagesChanged = function(){
            this.drag_area.classList.toggle('active', this.images && (this.images.length > 0));
        };

        QuestionManager.prototype.onUploadResponse = function(data){
            if(!data.success){
                
                return;
            }
            this.clear();
            this.quiz_link.href = data.url;
            this.quiz_link.innerText = data.url_text + " : " + data.name;
            this.quiz_container.style.display = 'flex';
        };

        QuestionManager.prototype.upload = function(){
            let self = this;
            let form_is_valid = this.validate();
            if(!form_is_valid){
                console.log("Quiz form is invalid");
                return;
            }

            let url = this.is_update_form() ? '/api/quizzes/' + this.form.dataset.quiz + '/update-question/' + this.form.dataset.question + '/' : '/api/quizzes/' + this.form.dataset.quiz + '/create-question/';

            let options = {
                url : url,
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                dataType : 'json',
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                let msg = {
                    content : response.message,
                    level : response.created
                }
                notify(msg);
                self.onUploadResponse(response);
                self.clearImages();
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                self.clearImages();
            });
        };


        QuestionManager.prototype.add_response = function(){
            element_utils.init();
            let answer_count = 4;
            let quiz = document.querySelector('#quiz');
            let answers_container = document.querySelector('#answers');
            //var options = [];
            for(let i = 0; i < answer_count; i++){
                let form_prefix = "form-" + i;
                let content_input = element_utils.create_input({'cls':'answer-content','name':form_prefix + '-' + 'content','value':'', 'type': 'text', 'id': form_prefix + '-' + 'content'});
                let is_correct_input = element_utils.create_input({'cls':'answer-is-correct','name': form_prefix + '-' + 'is_correct','value':'','type':'checkbox', 'id': form_prefix + '-' + 'is_correct'});
                let label = element_utils.create_label({'input_id':form_prefix + '-' + 'is_correct','value': 'Is correct'});
                //let delete_icon = element_utils.create_element({'element': 'i', 'cls': 'fas fa-trash icon'});
                //let span_icon= element_utils.create_element({'element': 'span', 'cls': 'padding-h','children':[delete_icon]});
                let span_iscorrect = element_utils.create_element({'element': 'span', 'cls': 'padding-h', 'children': [label,is_correct_input]});
                let div  = element_utils.create_element({'element': 'div', 'cls': 'flex flex-left', 'children':[content_input,span_iscorrect]});
                let li = element_utils.create_li({'cls':'', 'child': div});
                answers_container.appendChild(li);
            }
            let form_management_total_input = element_utils.create_input({'name': this.answer_formset_total_form, 'value': answer_count, 'type': 'hidden', 'id': this.answer_formset_total_form});
            let form_management_initial_input = element_utils.create_input({'name': this.answer_formset_total_form, 'value': 0, 'type': 'hidden', 'id': this.answer_formset_initial_form});
            this.form.appendChild(form_management_initial_input);
            this.form.appendChild(form_management_total_input)
            
        };

        QuestionManager.prototype.remove_responses = function(){
            let answers_container = document.querySelector('#answers');
            while(answers_container.firstChild){
                answers_container.removeChild(answers_container.firstChild);
            }
            this.form.removeChild(document.querySelector('#' + this.answer_formset_total_form));
            this.form.removeChild(document.querySelector('#' + this.answer_formset_initial_form));
            
        };
        
        QuestionManager.prototype.validate = function(){
            let content = document.querySelector('#content');
            let score = document.querySelector('#score');
            let answer_count = document.querySelector('#answer_count');
            let explanation = document.querySelector('#explanation');
            let c_type = document.querySelector('.js-input-question-type:checked');
            
            let is_valid = true;

            if(content == null || score == null || answer_count == null || explanation == null){
                is_valid = false;
            }
            if(content.value == ""){
                content.classList.add('warn');
                is_valid = false;
            }else{
                content.classList.remove('warn');
            }
            if(score.value == ""){
                score.classList.add('warn');
                is_valid = false;
            }else{
                score.classList.remove('warn');
            }
            if(answer_count.value == ""){
                answer_count.classList.add('warn');
                is_valid = false;
            }else{
                answer_count.classList.remove('warn');
            }
            if(c_type == null){
                is_valid = false;
            }
            /*
            if((this.images == null || this.images.length == 0) && !this.is_update_form()){
                return false;
            }*/
            return is_valid;
        };

        return QuestionManager;

    })();
    


    var QuizStepManager = (function(){
        function QuizStepManager() {
            this.form = undefined;
            this.formData = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.quiz_container = undefined;
            this.quiz_link = undefined;
            this.selected_questions = [];
        };
        QuizStepManager.prototype.init = function(){
            var self = this;
            this.form = document.querySelector('#quizstep-form') || document.querySelector('#quizstep-update-form');
            if(this.form == null ){
                console.warn("No QuizStep form found");
                return;
            }
            this.questions_input = document.querySelector('#questions');
            this.quiz_container = document.querySelector('#created-producted-link');
            this.quiz_link = document.querySelector('#created-producted-link a');
            this.validators = [];
            $('.js-qs-question-select').on('change', function(event){
                let value = "";
                if(this.checked){
                    self.selected_questions.push(this);
                }else{
                    self.selected_questions.splice(self.selected_questions.indexOf(this), 1);
                }
                self.selected_questions.forEach(function(input, index){
                    if(index < self.selected_questions.length -1){
                        value+= input.value + ',';
                    }else{
                        value +=input.value;
                    }
                });
                self.questions_input.value = value;
            });
            $('.js-clear-selected-questions').on('click', function(){
                $('.js-qs-question-select').prop('checked', false);
                self.questions_input.value = "";
                self.selected_questions.splice(0, self.selected_questions.length);
            });
            $(this.form).on('submit', function(e){
                e.preventDefault();
                e.stopPropagation();
                self.formData = new FormData(self.form);
                self.upload();
            });

            console.log("QuizStepManager initialized");

        };

        QuizStepManager.prototype.clear = function(){
            document.querySelector('#title').value = "";
            document.querySelector('#rank').value = "";
            this.quiz_link.href = '';
            this.quiz_link.innerText = '';
            this.quiz_container.style.display = 'none';
        }

        QuizStepManager.prototype.is_update_form = function(){
            return this.form != null ? this.form.id == 'question-update-form' : false;
        }

        QuizStepManager.prototype.onUploadResponse = function(data){
            if(!data.success){
                
                return;
            }
            this.clear();
            this.quiz_link.href = data.url;
            this.quiz_link.innerText = data.message;
            this.quiz_container.style.display = 'flex';
        };

        QuizStepManager.prototype.upload = function(){
            let self = this;
            let form_is_valid = this.validate();
            if(!form_is_valid){
                console.log("Quiz form is invalid");
                return;
            }

            let url = this.is_update_form() ? '/api/quizzes/' + this.form.dataset.quiz + '/update-quizstep/' + this.form.dataset.quizstep + '/' : '/api/quizzes/' + this.form.dataset.quiz + '/create-quizstep/';

            let options = {
                url : url,
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                dataType : 'json',
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                let msg = {
                    content : response.message,
                    level : response.success
                }
                notify(msg);
                self.onUploadResponse(response);
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
            });
        };

        
        QuizStepManager.prototype.validate = function(){
            let title = document.querySelector('#title');
            let rank = document.querySelector('#rank');
            let c_type = document.querySelector('.js-input-score-type:checked');
            
            let is_valid = true;

            if(title == null || rank == null){
                is_valid = false;
            }
            if(title.value == ""){
                title.classList.add('warn');
                is_valid = false;
            }else{
                title.classList.remove('warn');
            }
            if(rank.value == ""){
                rank.classList.add('warn');
                is_valid = false;
            }else{
                rank.classList.remove('warn');
            }
            if(c_type == null){
                is_valid = false;
            }
            /*
            if((this.images == null || this.images.length == 0) && !this.is_update_form()){
                return false;
            }*/
            return is_valid;
        };

        return QuizStepManager;

    })();

    var ProductManager = (function(){
        function ProductManager() {
            this.images = null;
            this.form = undefined;
            this.formData = undefined;
            this.input_file = undefined;
            this.drag_area = undefined;
            this.files_container = undefined;
            this.send_btn = undefined;
            this.clear_uploaded_files_btn = undefined;
            this.created_product_container = undefined;
            this.created_product_link = undefined;
            this.on_demand_url = undefined;
            this.supported_formats = ['jpg', 'jpeg', 'png', 'webp'];
        };
        ProductManager.prototype.init = function(){
            var self = this;
            this.form = document.querySelector('#product-upload-form') || document.querySelector('#product-update-form');
            if(this.form == null ){
                return;
            }
            this.drag_area = document.querySelector('.drag-area');
            if(!this.drag_area){
                return;
            }
            this.input_file = document.querySelector('#files');
            if(!this.input_file){
                return;
            }
            this.created_product_container = document.querySelector('#created-producted-link');
            this.created_product_link = document.querySelector('#created-producted-link a');
            this.files_container = document.querySelector('.file-list');
            this.on_demand_url = document.querySelector('#on-demand-url');
            $('.drag-area').on('drag dragstart dragend dragover dragenter drop', function(e){
                e.preventDefault();
                e.stopPropagation();
            }).on('dragover dragenter', function(){
                self.drag_area.classList.add('on-drag');
            }).on('dragleave dragend drop', function(){
                self.drag_area.classList.remove('on-drag');
            }).on('drop', function(e){
                self.images = e.originalEvent.dataTransfer.files;
                self.input_file.files = self.images;
                self.onImagesChanged();
                self.imagesPreview();

            });
            $('#files').on('change', function(e){
                self.images = self.input_file.files;
                self.onImagesChanged();
                self.imagesPreview();
            });
            $('.js-input-availability').on('change', function(e){
                try {
                    self.on_demand_url.classList.toggle('hidden', !(parseInt(this.value) == AVAILABILITY_ON_DEMAND));
                } catch (error) {
                    
                }
            });
            $('input.product-type-input').on('change', update_attrs_from_type);
            $('.js-uploaded-files-clear').on('click', this.clearImages.bind(this));
            this.validators = [this.validateAvailability, this.validateBrand, this.validateCategory, 
                                this.validateDescriptions, this.validateGender, this.validateName, 
                                this.validateProductType, this.validateVariants, this.validateImages];
            

            
            $(this.form).on('submit', function(e){
                e.preventDefault();
                e.stopPropagation();
                self.formData = new FormData(self.form);
                self.upload();
            });

            console.log("ProductManager initialized");

        };

        ProductManager.prototype.imagesPreview = function(){
            var li;
            var img;
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            var f;
            for(var i = 0; i < this.images.length; i++){
                f = this.images[i];
                li = document.createElement('li');
                img = document.createElement('img');
                img.src = URL.createObjectURL(f);
                img.height = 60;
                this.files_container.appendChild(li);
                img.onload = function(){
                    URL.revokeObjectURL(img.src);
                };
                li.classList.add('file-entry');
                li.appendChild(img);
                const info = document.createElement('span');
                info.innerHTML = f.name + " : " + Math.ceil(f.size/1024) + ' KB';
                li.appendChild(info);
            }
            $('.js-uploaded-files-clear').show();
        };

        ProductManager.prototype.clearImages = function(){
            while(this.files_container.firstChild){
                this.files_container.removeChild(this.files_container.firstChild);
            }
            this.images = null;
            this.input_file.files = null;
            var li = document.createElement('li');
            var span = document.createElement('span');
            span.innerText = "No images";
            li.appendChild(span);
            this.files_container.appendChild(li);
            this.onImagesChanged();
        };

        ProductManager.prototype.clear = function(){
            var inputs = [];
            var name = document.querySelector('#name');
            var display_name = document.querySelector('#display-name');
            var gender = document.querySelectorAll('#gender');
            var seller = document.querySelector('#sold-by');
            var availability = document.querySelectorAll('#availability');
            var attributes = document.querySelectorAll('#attributes');
            var price = document.querySelector('#price');
            var discount = document.querySelector('#promotion-price');
            var description = document.querySelector('#description');
            var short_description = document.querySelector('#short-description');
            short_description.value = "";
            description.value = "";
            price.value = "";
            discount.value = "";
            name.value = "";
            display_name.value = "";
            gender.selectedIndex = null;
            seller.selectedIndex = null;
            availability.selectedIndex = null;
            attributes.selectedIndex = null;
            this.input_file.files = null;
            this.images = null;
            this.created_product_link.href = '';
            this.created_product_link.innerText = '';
            this.created_product_container.style.display = 'none';
            this.onImagesChanged();
        }

        ProductManager.prototype.is_update_form = function(){
            return this.form != null ? this.form.id == 'product-update-form' : false;
        }

        ProductManager.prototype.validate = function(){
            // if(this.validators){
            //     return this.validators.every((f)=>f());
            // }
            return true;
        };

        ProductManager.prototype.validateName = function(){
            var name = document.querySelector('#name');
            var display_name = document.querySelector('#display-name');
            // if(!name || !display_name || !name.value.lenght || !display_name.value.length){
            //     console.log("name & display name errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateGender = function(){
            var gender = document.querySelector('#gender');
            // if(!gender  || !gender.value.length){
            //     console.log("error errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateAvailability = function(){
            var availability = document.querySelector('#availability');
            // if(!availability  || !availability.value.length){
            //     console.log("availability errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateCategory = function(){
            var category = document.querySelector('#category');
            // if(!category  || !category.value.length){
            //     console.log("category errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateBrand = function(){
            var brand = document.querySelector('#brand');
            // if(!brand  || !brand.value.length){
            //     console.log("brand errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateProductType = function(){
            var product_type = document.querySelector('#product-type');
            // if(!product_type  || !product_type.value.length){
            //     console.log("product type errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validatePrices = function(){
            var price = document.querySelector('#price');
            // if(!price  || !price.value.length){
            //     console.log("price errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateVariants = function(){
            var variants = document.querySelector('#variants');
            // if(!variants  || !variants.value.length){
            //     console.log(" variants errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.validateDescriptions = function(){
            var description = document.querySelector('#description');
            // if(!description  || !description.value.length){
            //     console.log(" description errors");
            //     return false;
            // }
            return true;
        };

        ProductManager.prototype.onImagesChanged = function(){
            this.drag_area.classList.toggle('active', this.images && (this.images.length > 0));
        };

        ProductManager.prototype.validateImages = function(){
            
            if(!this.images  || !this.input_file.files.length){
                console.log(" images errors");
                return false;
            }
            return true;
        };

        ProductManager.prototype.onUploadResponse = function(data){
            
            if(!data.success){
                return;
            }
            this.created_product_link.href = data.url;
            this.created_product_link.innerText = data.url_text + " : " + data.name;
            this.created_product_container.style.display = 'flex';
            if(!this.is_update_form()){
                self.clearImages();
                this.clear();
            }
        };

        ProductManager.prototype.upload = function(){
            let self = this;
            var form_is_valid = this.validate();
            if(!form_is_valid){
                console.log("Product form is invalid");
                return;
            }
            let url = this.is_update_form() ? '/api/update-product/' + this.form.dataset.product + '/' : '/api/create-product/';
            var options = {
                url : url,
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                dataType : 'json',
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                var msg = {
                    content : response.message,
                    level : response.success
                }
                notify(msg);
                self.onUploadResponse(response);
                
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                if(!self.is_update_form()){
                    self.clearImages();
                }
            });
        };

        return ProductManager;

    })();

    var FileUpload = (function(){
        function FileUpload(){
            this.files = [];
            this.form = undefined;
            this.formData = undefined;
            this.clean = true;
            this.drag_area = $('.drag-area');
            this.file_list_container = $('.file-list');
            this.file_entries = {};
            this.empty_element = $('.no-data', this.file_list_container);
            this.send_btn = $('.js-send-file-upload-btn');
            this.clear_btn = $('.js-file-list-clear-btn');
            //this.init();
        };

        FileUpload.prototype.init = function(){
            var that = this;
            this.clear_btn.on('click', this.clear.bind(this));

            $('.drag-area')
                .on('drop', onDropHandler)
                .on('dragover', onDragOverHandler)
                .on('dragenter', onDragStartHandler)
                .on('dragleave', onDragEndHandler)
            console.log("Fileupload initialized");
        };

        FileUpload.prototype.clear = function() {
            this.files = [];
            this.formData = undefined;
            this.form = undefined;
            this.clean = true;
            //$('.file-entry', this.file_list_container).remove();
            this.file_list_container.empty().append(this.empty_element);
            this.drag_area.removeClass('non-empty');
            this.send_btn.addClass('disabled').prop('disabled',true);
            this.clear_btn.addClass('hidden');
            console.log("[OK] cleared file list");
        };

        FileUpload.prototype.isClean = function() {
            return this.clean;
        };

        FileUpload.prototype.setForm = function(form){
            this.form = form;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.setFiles = function(files){
            this.files = files;
            this.clean = false;
            return this;
        };

        FileUpload.prototype.addFile = function(file){
            if(this.files.some(f => f.name == file.name)){
                console.warn("A file with the same name already exists.")
                return this;
            }
            var that = this;
            this.files.push(file);
            var li = $('<li />',{
                id:"file-" + that.files.length,
                'class' : 'file-entry',
                'title': file.name,
            });
            var entry_text = $('<span />', {
                text: file.name
            });
            var entry_remove_btn = $('<button />', {
                class: 'mat-button mat-button-text',
                type: 'button'
            }).append($('<i />', {
                class: 'fas fa-times icon'
            }));
            entry_remove_btn.on('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                that.removeFile([file.name]);
                li.remove();
            });
            li.append(entry_text, entry_remove_btn).appendTo(that.file_list_container);
            $('.no-data', that.file_list_container).remove();
            this.drag_area.addClass('non-empty');
            this.send_btn.removeClass('disabled').prop('disabled',false);
            this.clear_btn.removeClass('hidden');
            this.clean = false;
            return this;
        };

        FileUpload.prototype.removeFile = function(fileNames){
            console.log("removing files : %s", fileNames);
            var old_length = this.files.length;
            this.files = this.files.filter(f => !fileNames.includes(f.name));
            if(this.files.length != old_length && this.files.length < old_length){
                console.log("removed files : %s", fileNames);
                if(this.files.length == 0){
                    this.file_list_container.append(this.empty_element);
                    this.drag_area.removeClass('non-empty');
                    this.send_btn.addClass('disabled').prop('disabled',true);
                    this.clear_btn.addClass('hidden');
                }
                this.clean = false;
            }else{
                console.log("files : %s not removed", fileNames);
                
            }
            
            return this;
        };
        FileUpload.prototype.update = function(){
            if(this.isClean()){
                console.warn("FileUpload can not be updated. formData is already clean.");
                return;
            }
            if(!this.form || !this.files || this.files.length == 0){
                console.warn("FileUpload can not be updated. form or files are missing.");
                return;
            }
            this.formData = new FormData(this.form);
            var that = this;
            this.files.forEach(function(file, index){
                that.formData.append("file_" + index, file, file.name);
            });
            this.clean = true;
            /*
            $(form).serializeArray().forEach(function(input, index){
                formData.append(input.name, input.value);
            });
            */
        };

        FileUpload.prototype.canSend = function(){
            let formValid = typeof this.form != 'undefined';
            let filesValid = typeof this.files != 'undefined';

            return formValid && filesValid && this.files.length > 0;
        };

        FileUpload.prototype.getForm = function() {
            return this.form;
        };

        FileUpload.prototype.getFiles = function() {
            return this.files;
        }

        FileUpload.prototype.getFormDate = function() {
            return this.formData;
        }

        FileUpload.prototype.upload = function(){
            if(!this.canSend()){
                console.error("Files can not be sent. Please check your files form. Files or form are missing.");
                return;
            }
            if(typeof ajax_api.ajax_lang === 'undefined'){
                var errorMsg = "can not upload files. ajax funtion is not defined";
                console.error(errorMsg);
                throw new Error(errorMsg);
            }
            var that = this;
            var options = {
                url : $(this.form).attr('action'),
                type: 'POST',
                enctype : 'multipart/form-data',
                data : this.formData,
                processData : false,
                cache : false,
                contentType : false
            };
            ajax_api.ajax(options).then(function(response){
                console.info("Files have bean uploaded.");
                var msg = {
                    content : response.message,
                    level : response.status === 'OK'
                }
                notify(msg);
                fileUpload.clear();
                

            }, function(reason){
                console.error("Files could not be uploaded.");
                console.error(reason);
                fileUpload.clear();
            });

        };

        return FileUpload;
    })();

    function kiosk_update(event){
        document.getElementById('main-image').src = event.target.src;
        $(".kiosk-image").removeClass('active').filter(event.target).addClass("active");
    }

    function dateFormat(index, input){
        console.log(input);
        console.log("Date Value : %s", input.value);
    }

    function regroupe_attrs(attribute_list){
        var keySet = new Set();
        var attrs_map = {};
        attribute_list.forEach((o)=>{
            keySet.add(o.name);
        });
        keySet.forEach((name)=>{
            attrs_map[name] = attribute_list.filter(o => o.name == name).sort((first, second) =>{
                if (first.value < second.value) {
                    return -1
                }
                if(first.value > second.value){
                    return 1;
                }
                return 0;
            });
        });
        return attrs_map;
    }

    function update_attrs(attrs_mapping){
        var attributes_container = document.querySelector('#attributes-container');
        while(attributes_container.firstChild){
            attributes_container.removeChild(attributes_container.firstChild);
        }
        var i = 0;
        for(const [key,value] of Object.entries(attrs_mapping)){
            var div = document.createElement('div');
            var label = document.createElement('label');
            var select = document.createElement('select');
            var opt = document.createElement('option');
            opt.innerText = `Select a ${key}`;
            select.appendChild(opt);
            value.forEach((o)=>{
                opt = document.createElement('option');
                opt.value = o.id;
                opt.innerText = o.value;
                select.appendChild(opt);
            });
            select.name = 'attributes';
            select.id = select.name + "-" + i;
            select.multiple = true;
            label.htmlFor = select.id;
            label.innerText = key.toUpperCase();
            i++;
            div.appendChild(label);
            div.appendChild(select);
            div.classList.add('form-group');
            attributes_container.appendChild(div);
            
        }

    }

    function update_attrs_from_type(){
        var input = document.querySelector('input.product-type-input:checked');
        var option = {
            type:'GET',
            method: 'GET',
            dataType: 'json',
            url : '/api/attrs-from-type/' + input.dataset.typeUuid + '/'
        }
        ajax_api.ajax(option).then(function(response){
            var attributes = response.attributes;
            var attrs_mapping = regroupe_attrs(attributes);
            update_attrs(attrs_mapping);
        }, function(reason){
            console.error(reason);
        });
    }


    $(document).ready(function(){
        if(window){
            window.notify = notify;
        }
        notification_wrapper = $('#notifications-wrapper');
        messages = $('#messages', notification_wrapper);
        //onDragInit();
        notify_init(notification_wrapper, messages);
        var listfilter = new ListFilter();
        fileUpload = new FileUpload();
        quizManager = new QuizManager();
        questionManager = new QuestionManager();
        quizstepManager = new QuizStepManager();
        quizManager.init();
        questionManager.init();
        quizstepManager.init();
        
        $('.collapsible .toggle').on('click', function(event){
            var parent = $(this).parent();
            var target = $('.' + this.getAttribute('data-toggle'), parent);
            $('input', parent).val('');
            
            target.toggle();
        });
        $('.js-filter-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var input_name = this.getAttribute('data-input-name');
            var container = $('#' + this.getAttribute('data-container'));
            var filter_field = this.getAttribute("data-filter-field");
            var value_list = [];
            $("input:checked[name=\"" + input_name + "\"]", ctx).each(function(){
                console.log("adding value to filter : %s", this.getAttribute("data-value"));
                value_list.push(this.getAttribute("data-value"));
            });
            listfilter.filter(container, filter_field, value_list);
        });

        $('.js-filter-reset-btn').on('click', function(event){
            var ctx = $('#' + this.getAttribute('data-context'));
            var container = $('#' + this.getAttribute('data-container'));
            listfilter.reset_filter(ctx, container);
        });

        $('#file-upload-form').on('submit', function(event){
            console.log("submitting file-upload-form");
            event.preventDefault();
            event.stopPropagation();
            console.log(this);
            fileUpload.setForm(this);
            fileUpload.update();
            fileUpload.upload();
            //return false;
            
        });
        $('.js-select-image').on('click', kiosk_update);
        $('.js-select-image').first().click();
        $(".limited-input").on("keyup", function(event){
            event.stopPropagation();
            console.log("limited input keyup");
            input_check_max_limit(this);
        });
        $('.js-dialog-open').on('click', function(){
            var target = $('#' + $(this).data('target'));
            target.show();
        });

        
        $('.js-dialog-close').on('click', function(){
            var target = $("#" + $(this).data('target'));
            target.hide();
            //var parent = $(this).parents('.dialog').hide();
            $('input[type!="hidden"]', target).val('');
        });
        $('.js-reveal-btn, .js-revealable-hide').on('click', function(){
            var target = $($(this).data('target')).parent();
            $('.js-revealable', target).toggleClass('hidden');
        });
        $('.js-clear-input').on('click', function(){
            
            var target = $('#' + $(this).data('target'));
            console.log("Clearing inputs from ", target);
            $('input[type!=checkbox]', target).val('');
            $('input:checkbox', target).val('').prop('checked', '');
        });
        var selectable_list = $(".js-selectable");
        var activable_list = $(".js-activable");
        var select_all = $('.js-select-all');
        selectable_list.on('click', function(){
            var is_selected = selectable_list.is(function (el) {
                return this.checked;
            });
            
            var selected_all = selectable_list.is(function (el) {
                return !this.checked;
            });
            select_all.prop('checked', !selected_all);
            activable_list.prop('disabled', !is_selected);
        });

        select_all.on('click', function(){
            console.log("Select All clicked : %s", this.checked);
            selectable_list.prop('checked', this.checked);
            activable_list.prop('disabled', !this.checked);
        });

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
        
        $('.js-custom-input .input-value').on('click', function(event){
            $(this).toggle();
            $('.input-edit-wrapper', $(this).parent()).toggle();
        });
        
        /*
        $('.js-custom-input .js-edit').on('click', function(event){
            $(this).parent().toggle();
            $(this).siblings('input').toggle();
        });
        */
        
        $('.js-custom-input input').on('keyup change', function(event){
            var $el = $(this);
            $el.parent().siblings('.input-value').html($el.val());
        });
        
        $('.js-custom-input .js-edit-close').on('click', function(event){
            var $el = $(this).siblings('input');
            $el.parent().siblings('.input-value').html($el.val());
            $(this).parent().toggle();
        });
        $('.js-menu').on('click', function(){
            console.log("Menu clicked");
            $('.site-panel').css('left', 0);
            $('.js-menu-close').show();
            $(this).hide();
    
        });
        $('.js-menu-close').on('click', function(){
            var panel = $('.site-panel');
            var left = '-' + panel.css('width');
            panel.css('left', left );
            $('.js-menu').show();
            $(this).hide();
        });
        $('.js-action-abtest').on('click', function(e){
            track_action(this);
        });
        
        console.log("commons.js loaded");
        /*
        $('.js-revealable-hide').on('click', function(){
            console.log('hidding revealable inputs');
            var target = $($(this).data('target')).parent();
            $('.js-revealable', target).hide();
        });
        */
    });

});