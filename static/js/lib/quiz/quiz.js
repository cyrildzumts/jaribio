define(['ajax_api', 'tag_api' ],function(Ajax, TagApi){
    const QUIZ_GAME_CONTAINER = "quiz-game-container";
    const START_QUIZ_BTN = "start-quiz-btn";
    const FETCH_QUIZ_URL = "/api/fetch-quiz-data/";
    class Quiz {
        constructor(){
            this.players = [];
            this.currentStep = null;
            this.steps = [];
            this.currentQuestion = null;
            this.start_btn = null;
            this.container = null;
            this.quiz_uuid = null;
            this.quiz_started = false;
            this.is_ready = false;
        }

        init(){
            let self = this;
            this.start_btn = document.getElementById(START_QUIZ_BTN);
            this.container = document.getElementById(QUIZ_GAME_CONTAINER);
            this.quiz_uuid = this.start_btn.dataset.quiz;
            this.start_btn.addEventListener('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                self.quiz_started = !self.quiz_started;
                if(self.quiz_started){
                    self.startQuiz();
                }else{
                    self.stopQuiz();
                }

            });
        }

        addPlayer(player){
            this.players.push(player);
        }
        removePlayer(player){
            
        }

        getNextStep(){
            return null;
        }

        getNextQuestion(){

        }

        collectAllAnswers(){

        }

        computeScore(){

        }

        onQuizDataFetched(response){
            console.info("Quiz Data fetched : ", response);
        }

        fetch_quiz_data(){
            let self = this;
            let url = `${FETCH_QUIZ_URL}${self.quiz_uuid}/`;
            let options = {
                type: 'GET',
                dataType: 'json',
                url : url,
            }

            Ajax.ajax(options).then(function(response){
                if(response.success){
                    self.onQuizDataFetched(response)
                }
            }, function(error){
                console.error(error);
            });
        }

        onQuestionTimeout(){

        }
        onQuizStarted(){

        }

        startQuiz(){
            console.log("Starting Quiz ...");
            this.fetch_quiz_data();
        }

        stopQuiz(){
            console.log("Stopping Quiz ...");
        }
    };

    return Quiz;
});
