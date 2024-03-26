define(['ajax_api','tag_api'], function(Ajax,TagApi){
    class Question {
        constructor(question){
            this.id = question.id;
            this.content = question.content;
            this.explanation = question.explanation;
            this.answer_count = question.answer_count;
            this.question_type = question.question_type;
            this.question_uuid = question.question_uuid;
            this.quiz = question.quiz;
            this.answers = [];

        }

        getId(){
            return this.id;
        }

        setAnswers(answers){
            this.answers = answers;
        }

        getAnswers(){
            return this.answers;
        }

        getContent(){
            return this.content;
        }

        getExplanation(){
            return this.explanation;
        }

        getAnswerCount(){
            return this.answer_count;
        }

        getQuestionType(){
            return this.question_type;
        }

        getQuestionUuid(){
            return this.question_uuid;
        }

        render(){
            let content = TagApi.create_tag({
                'element': 'span',
                'options': {
                    'innerText': this.content,
                    'cls': ''
                }
            });
            
            let div = TagApi.create_tag({
                'element': 'div',
                'options': {
                    'cls': 'flex',
                    'children': [content]
                }
            });
            return div;
        }
    }

    return Question;
});