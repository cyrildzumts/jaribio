define(['ajax_api','tag_api'], function(Ajax,TagApi){
    const ANSWERS_CLS = "question-grid container answers";
    const ANSWERS_ID = "answers";
    const ANSWER_UNIQUE_SELECTION = 0;
    const ANSWER_MULTIPLE_SELECTION = 1;
    const ANSWER_TYPE_BOOLEAN_SELECTION = 2;
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
                    'cls': 'question-box flex full',
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

        onMultipleSelection(answer){
            let self = this;
            answer.selected = !answer.selected;
            answer.tag.content.classList.toggle('selected');
        }

        onUniqueSelection(answer){
            let self = this;
            this.answers.forEach((a) =>{
                if(a != answer){
                    a.selected = false;
                    a.tag.content.classList.remove('selected');
                }
            });
            answer.selected = true;
            answer.tag.content.classList.add('selected');
        }

        onAnswerClicked(answer){
            if(this.question_type == ANSWER_MULTIPLE_SELECTION){
                this.onMultipleSelection(answer);
            }else if(this.question_type == ANSWER_UNIQUE_SELECTION){
                this.onUniqueSelection(answer);
            }else{
                
            }
        }
    }

    return Question;
});