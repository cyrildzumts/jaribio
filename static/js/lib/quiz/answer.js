define(['ajax_api','tag_api'], function(Ajax,TagApi){
    class Answer {
        constructor(answer){
            this.question = answer.question;
            this.content = answer.content;
            this.answer_uuid = answer.answer_uuid;
            this.quiz = answer.question.quiz;
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
            return div;
        }
    }

    return Answer;
});