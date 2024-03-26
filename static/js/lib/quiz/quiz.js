define(['ajax_api', 'tag_api', 'quiz/step', 'quiz/question','quiz/answer' ],function(Ajax, TagApi, QuizStep, Question,Answer){
    const QUIZ_GAME_CONTAINER = "quiz-game-container";
    const ANSWERS_GAME_CONTAINER = "answers-game-container";
    const START_QUIZ_BTN = "start-quiz-btn";
    const NEXT_QUESTION_BTN = "next-question-btn";
    const NEXT_STEP_BTN = "next-step-btn";
    const COLLECT_RESULT_BTN = "collect-result-btn";
    const FETCH_QUIZ_URL = "/api/fetch-quiz-data/";
    const FETCH_QUESTION_ANSWERS_URL = "/api/fetch-question-data/";
    const FETCH_COLLECT_RESULT_URL = "/api/fetch-collect-result/";
    const TIMER_ID = "timer";
    const BASE_TIMEOUT_MS = 1000; 
    const TIMER_TIMEOUT_MS = 15; 
    class Quiz {
        constructor(){
            this.players = [];
            this.currentStep = null;
            this.currentStepIndex = 0;
            this.steps = [];
            this.questions = [];
            this.currentQuestion = null;
            this.start_btn = null;
            this.next_btn = null;
            this.next_step_btn = null;
            this.collect_btn = null;
            this.container = null;
            this.quiz_uuid = null;
            this.quiz_data = null;
            this.quiz_started = false;
            this.is_ready = false;
            this.iterations = TIMER_TIMEOUT_MS;
            this.timeout = null;
            this.timer_tag = null;
        }

        init(){
            let self = this;
            this.start_btn = document.getElementById(START_QUIZ_BTN);
            this.next_btn = document.getElementById(NEXT_QUESTION_BTN);
            this.next_step_btn = document.getElementById(NEXT_STEP_BTN);
            this.collect_btn = document.getElementById(COLLECT_RESULT_BTN);
            this.container = document.getElementById(QUIZ_GAME_CONTAINER);
            this.answers_container = document.getElementById(ANSWERS_GAME_CONTAINER);
            this.timer_tag = document.getElementById(TIMER_ID);
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
            this.next_btn.addEventListener('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                if(self.quiz_started){
                    self.onNextBtnClicked(event);
                }
            });
            this.next_step_btn.addEventListener('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                if(self.quiz_started){
                    self.onNextStepBtnClicked(event);
                }
            });
            this.collect_btn.addEventListener('click', function(event){
                event.preventDefault();
                event.stopPropagation();
                if(self.quiz_started){
                    self.onNextBtnClicked(event);
                }
            });
            
            console.info("Quiz Initialized");
        }

        monitorQuestion(){
            this.timer_tag.innerText = `${this.iterations}s`;
            if(this.iterations-- > -1){
                this.timeout = setTimeout(this.monitorQuestion.bind(this), BASE_TIMEOUT_MS);
            }else{
                this.onQuestionTimeout();
            }
        }

        removeAllChildren(container){
            if(!container){
                return;
            }
            while(container.firstChild){
                container.removeChild(container.firstChild);
            }
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

        onQuestionTimeout(){
            clearTimeout(this.timeout);
            this.start_btn.classList.add("hidden");
            this.next_btn.classList.toggle("hidden", this.currentStep.isLastQuestion());
            this.next_btn.disabled = this.currentStep.isLastQuestion();
            let has_next_step = this.currentStepIndex < this.steps.length;
            let go_next = this.currentStep.isLastQuestion() && has_next_step;
            this.next_step_btn.classList.toggle('hidden', !go_next);
            this.iterations = TIMER_TIMEOUT_MS;
            this.timer_tag.innerText = `${this.iterations}s`;
            this.timer_tag.classList.add('hidden');
        }

        onNextStepBtnClicked(event){
            if(this.currentStepIndex < this.steps.length){
                
            }
            this.next_step_btn.classList.add('hidden');
            this.currentStepIndex ++;
            this.currentStep = this.steps[this.currentStepIndex];
            this.currentQuestion = this.currentStep.currentQuestion();
            if(this.currentQuestion){
                this.renderCurrentQuestion();
            }else{
                console.warn("CurrentQuestion is null");
            }

        }


        onNextBtnClicked(event){
            this.next_btn.classList.add("hidden");
            this.next_btn.disabled = true;
            this.currentStep.nextQuestion();
            this.currentQuestion = this.currentStep.currentQuestion();
            if(this.currentQuestion){
                this.renderCurrentQuestion();
            }else{
                console.warn("CurrentQuestion is null");
            }

        }

        renderCurrentQuestion(){
            this.removeAllChildren(this.container);
            this.container.appendChild(this.currentQuestion.renderQuestion());
            this.container.classList.toggle('hidden', !this.currentQuestion);
            this.fetch_question_data(this.currentQuestion);
        }

        onQuizDataFetched(response){
            let self = this;
            console.info("Quiz Data fetched : ", response);
            response.questions.forEach(q => {
                self.questions.push(new Question(q));
            });
            response.quizsteps.forEach(qs => {
                let q_ids = qs.questions.split(',').map((x)=> parseInt(x));
                let questions = self.questions.filter((q) => q_ids.includes(q.id));
                let quizStep = new QuizStep(qs);
                quizStep.setQuestions(questions);
                self.steps.push(quizStep);
                
            });
            this.currentStep = this.steps[0];
            this.currentQuestion = this.currentStep.currentQuestion();
            this.quiz_data = response.quiz;
            this.renderCurrentQuestion()
            
        }

        onQuestionDataFetched(response, question){
            let self = this;
            console.info("Question Data fetched : ", response, question);
            this.removeAllChildren(this.answers_container);
            let answers = response.answers.map((a) => new Answer(a));
            question.setAnswers(answers);
            answers.forEach((a)=>{
                a.setOnClicked(question.onAnswerClicked.bind(question));
            });
            self.answers_container.appendChild(question.renderAnswers());
            this.answers_container.classList.toggle('hidden', !response.success);
            this.timer_tag.classList.remove('hidden');
            this.monitorQuestion();
        }

        renderAnswers(){

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

        fetch_question_data(question){
            let self = this;
            let url = `${FETCH_QUESTION_ANSWERS_URL}${question.getQuestionUuid()}/`;
            let options = {
                type: 'GET',
                dataType: 'json',
                url : url,
            }

            Ajax.ajax(options).then(function(response){
                if(response.success){
                    self.onQuestionDataFetched(response, question);
                }
            }, function(error){
                console.error(error);
            });
        }

        
        onQuizStarted(){

        }

        startQuiz(){
            console.log("Starting Quiz ...");
            this.fetch_quiz_data();
            this.start_btn.classList.add("hidden");
            this.start_btn.disabled = true;
        }

        stopQuiz(){
            this.next_btn.classList.add("hidden");
            this.next_btn.disabled = true;
            console.log("Stopping Quiz ...");
        }
    };

    return Quiz;
});
