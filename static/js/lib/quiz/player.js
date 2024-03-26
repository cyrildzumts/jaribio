define(['ajax_api','tag_api'], function(Ajax,TagApi){
    class Player {
        constructor(user){
            this.user = user;
            this.score = 0;

        }

        getScore(){
            return this.score;
        }

        setScore(score){
            this.score = score;
        }

        getUser(){
            return this.user;
        }

        getSelectedAnswer(){
            // TODO
        }

        render(){
            let name = TagApi.create_tag({
                'element': 'span',
                'options': {
                    'innerText': this.user.username,
                    'cls': 'margin-r'
                }
            });
            let score = TagApi.create_tag({
                'element': 'span',
                'options': {
                    'innerText': `Score : ${this.score}`,
                }
            });
            let div = TagApi.create_tag({
                'element': 'div',
                'options': {
                    'children': [name, score]
                }
            });
            return div;
        }
    }

    return Player;
});