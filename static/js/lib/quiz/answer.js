define(['ajax_api','tag_api'], function(Ajax,TagApi){
    class Answer {
        constructor(answer){
            this.id = answer.id;
            this.question = answer.question;
            this.content = answer.content;
            this.answer_uuid = answer.answer_uuid;
            this.quiz = answer.question.quiz;
            this.selected = false;
            this.onclick = null;
            this.tag = null;
        }

        setOnClicked(callback){
            this.onclick = callback;
        }

        getContent(){
            return this.content;
        }

        getQuestion(){
            return this.question;
        }

        getAnswerUuid(){
            return this.answer_uuid;
        }

        getQuiz(){
            return this.quiz;
        }

        render(){
            let self = this;
            let content = TagApi.create_tag({
                'element': 'div',
                'options': {
                    'innerText': this.content,
                    'cls': 'answer'
                }
            });
            
            let div = TagApi.create_tag({
                'element': 'li',
                'options': {
                    'cls': 'answer-wrapper',
                    'data-answer': this.answer_uuid,
                    'data-value': this.content,
                    'children': [content]
                }
            });
            div.addEventListener('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                //self.selected = true;
                self.onclick(self);
            });
            this.tag = {
                'div': div,
                'content': content
            };
            return div;
        }
    }

    return Answer;
});