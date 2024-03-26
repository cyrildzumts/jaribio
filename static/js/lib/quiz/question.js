define(['ajax_api','tag_api'], function(Ajax,TagApi){
    const ANSWERS_CLS = "question-grid container answers";
    const ANSWERS_ID = "answers";
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
            
        }

        renderQuestion(){
            let content = TagApi.create_tag({
                'element': 'p',
                'options': {
                    'innerText': this.content,
                    'cls': 'title-case bold large'
                }
            });
            let div_inner = TagApi.create_tag({
                'element': 'div',
                'options': {
                    'cls': 'margin-b',
                    'children': [content]
                }
            });
            
            let div = TagApi.create_tag({
                'element': 'div',
                'options': {
                    'id':'question',
                    'cls': 'question-box',
                    'children': [div_inner]
                }
            });
            return div;
        }

        renderAnswers(){
            //let answers_tag = this.answers.map((a) => a.render());
            let ul = TagApi.create_tag({
                'element': 'ul',
                'options': {
                    'id': ANSWERS_ID,
                    'cls': ANSWERS_CLS,
                    'children': this.answers.map((a) => a.render())
                }
            });

            return ul;
        }
    }

    return Question;
});