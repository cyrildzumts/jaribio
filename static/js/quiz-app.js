requirejs.config({
    baseUrl :'/static/js/lib',
    paths:{
        vendor: '../vendors'
    },
    waitSeconds: 0
});

requirejs(['accounts','quiz/quiz', 'commons', 'image_loader'], function(account, Quiz){
    account.init();
    let quiz = new Quiz();
    quiz.init();
    console.log("JQuery version :", $().jquery);
});