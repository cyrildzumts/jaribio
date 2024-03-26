define(['ajax_api','tag_api'], function(Ajax,TagApi){
    class QuizStep {
        constructor(quizStep){
            this.title = quizStep.title;
            this.quiz = quizStep.quiz;
            this.rank = quizStep.rank;
            this.questions = quizStep.questions;
            this.is_played = quizStep.is_played;
            this.score_type = quizStep.score_type;
            this.current_question_index = 0;
            this.max_steps = this.questions.length;
        }

        getTitle(){
            return this.title;
        }

        getQuiz(){
            return this.quiz;
        }

        getRank(){
            return this.rank;
        }

        getQuestions(){
            return this.questions;
        }

        getMaxSteps(){
            return this.max_steps;
        }

        getScoreType(){
            return this.score_type;
        }

        currentQuestion(){
            return this.questions[this.current_question_index]; 
        }

        nextQuestion(){
            if(this.current_question_index < this.max_steps - 1){
                this.current_question_index++;
            } 
        }
        isLastQuestion(){
            return this.current_question_index == this.max_steps - 1;
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

    return QuizStep;
});