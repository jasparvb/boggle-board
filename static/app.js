class Boggle {
    constructor() {
        this.msg = $('.message');
        this.score = 0;
        this.currentTime = 59;
        this.correctWords = [];
        this.gameTimer = setInterval(this.countDown.bind(this), 1000);
        $('#submit-form').on("submit", this.checkWord.bind(this));
    }


    async checkWord(e) {
        e.preventDefault()
        //Get word from input field
        console.log("start game");
        let word = $('#word').val().toUpperCase();
        if(word) {
            const response = await axios.get('/check-word', {
                params: {word: word}
            });
            this.handleResponse(response, word);
    
            //Clear input form
            $('#submit-form').trigger("reset");
        }
    }

    handleResponse(res, word) {
        
        if(res.data.result === 'ok' && this.correctWords.includes(word)) {
            this.msg.text("You already guessed that word!");
        }
        else if(res.data.result === 'ok' ) {
            this.correctWords.push(word);
            this.score += word.length;
            $('.score').text(this.score);
            this.msg.text(`Congrats! "${word}" is a word on the board. You scored ${word.length} ${word.length == 1 ? 'point' : 'points'}`);
        }
        else if(res.data.result === 'not-word') {
            this.msg.text(`"${word}" isn't even a word!`);
        }
        else if(res.data.result === 'not-on-board') {
            this.msg.text(`"${word}" is a word, but it's not on the board.`);
        }
    }

    countDown() {
        //countDown() runs every second
        $('.time').text(this.currentTime);
        //stops countdown when reaches 0
        if(this.currentTime === 0) {
            clearInterval(this.gameTimer);
            this.gameOver();
        }
        this.currentTime--;
    }
    
    async gameOver() {
        //disable input field
        $('#word').prop("disabled", true);
        //post score to server to see if made new high score (responds with true or false)
        const response = await axios.post('/post-score', {score: this.score});

        if(response.data){
            this.msg.html(`Game Over! You made a new high score of ${this.score}`);
            $('.high-score').text(this.score);
        }
        else this.msg.html('Game Over!');
    }
}

let boggleGame = new Boggle();