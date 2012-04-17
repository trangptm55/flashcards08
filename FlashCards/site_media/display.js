//var cmd5 = '3***4***5***6***7***8***9***10***11***12***13***14***15***16***17***18***19***20***21***22***23***24***25***26***27***28***29***30***31***32***33***34***35***36***37***38***39***40';
//var cmd6 = '3***4***5***6***7***8***9***10***11***12***13***14***15***16***17***18***19***20***21***22***23***24***25***26***27***28***29***30***31***32***33***34***35***36***37***38***39***40';
var cmd5 = document.getElementById('hiddenprompt').value
var cmd6 = document.getElementById('hiddenanswer').value

// split the encoded list of cards into encoded a-b-a-b pairs
var each = cmd5.split('***');
var each2 = cmd6.split('***');

function Question(num, question, answer) {
    this.num = num;
    this.question = question;
    this.answer = answer;
}

var FCQuestions = new Array();
for (var i = 0; i < each.length; i++) {
    FCQuestions.push(new Question(i, each[i], each2[i]));
}

var FC = new FlashCards(FCQuestions);
var MC = new MultipleChoice(FCQuestions);
var M = new Match(FCQuestions);

// FLASH CARDS
function FlashCards(questions) {
    this.questions = questions;
    this.flipped = 0;
    this.current = 0;
    this.cardCount = questions.length - 1;

    // Initialize flash cards
    //  - Clear content and load first flash card.
    this.init = function () {
        this.flipped = 0;
        this.current = 0;
        this.questions.sort(randOrd);

        // Mark table as currently on Flash Cards
        var table = FCGid('contenttable');
        table.cellSpacing = 0;
        table.className = 'flashcards';

        // Clear content
        var rows = table.getElementsByTagName('tr').length;
        for (i = 0; i < rows; i++)
            table.deleteRow(0);

        // Insert flash card HTML
        var tr = table.insertRow(-1);
        var td = tr.insertCell(-1);
        td.colSpan = 3;
        td.className = 'main';
        td.innerHTML = '<span id="question"></span><br/><br/><span id="answer" style="color:rgb(0,170,0)"></span>';
        tr = table.insertRow(-1);
        td = tr.insertCell(-1);
        td.innerHTML = '<a href="javascript:FC.next(-1);void(0)" id="prev">&laquo; Prev</a><a id="answerbutton" href="javascript:FC.flip();void(0)"></a><a href="javascript:FC.next(1);void(0)" id="next">Next &raquo;</a>';

        // Load first flash card
        this.next(0);
    };

    // Flip card
    // Toggle show/hide answer
    this.flip = function () {
        FCFadeDown('answer', 100);
        FCFadeDown('answerbutton', 100);

        if (this.flipped) {
            var x = setTimeout("FCGid('answer').innerHTML='&nbsp;'; FCGid('answerbutton').innerHTML='Show Answer'; FCFadeUp('answer',100); FCFadeUp('answerbutton',100);", 101);
        }
        else {
            var x = setTimeout("FCGid('answer').innerHTML=FC.questions[" + this.current + "].answer; FCGid('answerbutton').innerHTML='Hide Answer'; FCFadeUp('answer',100); FCFadeUp('answerbutton',100);", 101);
        }
        this.flipped = !this.flipped;
        ;
    };

    // Next card
    // Load next flashcard
    this.next = function (dir) {
        var i = this.current;
        if (dir == 1) i++;
        else if (dir == -1) i--;

        if (this.questions[i].question) {
            this.current = i;
            if (this.current <= 0) {
                this.current = 0;
                FCOpac('prev', 50);
            }
            else FCOpac('prev', 100);

            // next phase
            if (this.current + 1 >= this.questions.length) {
                FCGid('next').href = 'javascript:FC.done();void(0)';
            }

            else {
                FCGid('next').href = 'javascript:FC.next(1);void(0)';
            }

            FCFadeDown('question', 100);
            var x = setTimeout("FCGid('question').innerHTML=FC.questions[" + this.current + "].question; FCFadeUp('question',101);", 101);
            this.flipped = 1;
            FC.flip();
        }
    }

    // Done
    // Finished with Flash Cards, show link to Matching
    this.done = function () {
        FCFadeDown('question', 100);
        var link = 'Flashcards Complete!<br/><br/><a href="javascript:FCLoadNew(2);void(0)">Go to Step 2: Matching &raquo</a>';
        var x = setTimeout("FCGid('question').innerHTML='" + link + "'; FCFadeUp('question',100);", 101);
        FCGid('next').href = 'javascript:FCLoadNew(2);void(0)';
        FCGid('answer').innerHTML = '&nbsp;';
    }
}


// MATCHING
function Match(questions) {
    this.questions = questions;
    this.flipped = 0;
    this.matchInc = 5;
    this.matchStart = 0;

    // Initialize Matching
    //  - Clear content and load first problem.
    this.init = function () {
        var tr, td, a;
        this.flipped = 0;

        // Mark table as currently on Matching
        var table = FCGid('contenttable');
        table.cellSpacing = 0;
        table.className = 'matching';

        // Clear Content
        var rows = table.getElementsByTagName('tr').length;
        for (var i = 0; i < rows; i++) table.deleteRow(0);

        // Load new matching HTML
        tr = table.insertRow(-1);
        td = tr.insertCell(-1);
        td.style.fontSize = '8pt';
        td.style.fontWeight = 'bold';
        td.style.paddingLeft = '30px';
        td.id = 'scorel';
        td.innerHTML = 'Can you match each question with the correct answer?';

        td = tr.insertCell(1);
        td.className = 'bold';
        td.colSpan = 2;
        td.id = 'score';
        td.style.paddingLeft = '20px';
        td.innerHTML = '<a href="javascript:M.startCheck();void(0)">Done? Check your answers</a>';

        // Get and randomize the next slice of answers
        this.questionSlice = this.questions.slice(this.matchStart, this.matchStart + this.matchInc);
        this.questionSlice.sort(randOrd);

        // print the questions and answers
        for (var i = 0; i < this.questionSlice.length; ++i) {
            var question1 = this.questions[this.matchStart + i];
            var question2 = this.questionSlice[i];
            tr = table.insertRow(-1);

            // Question
            td = tr.insertCell(-1);
            td.id = 'tdq' + i;
            td.className = 'q';
            td.innerHTML = question1.question;
            td.setAttribute("question", question1.num);

            // Movement buttons
            td = tr.insertCell(-1);
            td.id = 'tdm' + i;
            td.className = 'm';
            td.innerHTML = '<a href="javascript:M.move(' + i + ',-1);void(0)"><img src="/static/i/up_8.png"/></a> <a href="javascript:M.move(' + i + ',1);void(0)"><img src="/static/i/down_8.png"/></a>';

            // Answer
            td = tr.insertCell(-1);
            td.id = 'tda' + i;
            td.className = 'a';
            td.innerHTML = question2.answer;
            td.setAttribute("answer", question2.num);

            // Try to prevent the random answer from being correct
            if ((i) && (question1.num == question2.num)) this.swap(i, (i - 1));
        }
    }

    // Move an answer one up or down.
    // Wrap around if at bottom/top.
    this.move = function (n, dir) {
        if (!this.flipped) {
            var newn;
            if (dir == -1) newn = n - 1;
            else if (dir == 1) newn = n + 1;

            if (!FCGid('tda' + newn)) {
                if (dir == 1) newn = this.matchStart;
                else if (dir == -1) newn = this.matchStart + this.matchInc - 1;
            }

            // fade both down
            FCFadeDown('tda' + newn, 150);
            FCFadeDown('tda' + n, 150);

            // switch answers and fade up
            var a = setTimeout("M.swap(" + newn + "," + n + ")", 151);
        }
    }

    // Swap two answers
    this.swap = function (a, b) {
        var tmpAnswer = FCGid('tda' + a).innerHTML;
        FCGid('tda' + a).innerHTML = FCGid('tda' + b).innerHTML;
        FCGid('tda' + b).innerHTML = tmpAnswer;

        var tmpAnswerNum = FCGid('tda' + a).getAttribute("answer");
        FCGid('tda' + a).setAttribute("answer", FCGid('tda' + b).getAttribute("answer"));
        FCGid('tda' + b).setAttribute("answer", tmpAnswerNum);

        // fade both up
        FCFadeUp('tda' + a, 150);
        FCFadeUp('tda' + b, 150);
    }

    // Initiate checking score
    this.startCheck = function () {
        this.flipped = 1;
        for (var i = 0; i < this.questionSlice.length; i++) {
            setTimeout("FCFadeDown('tda" + i + "',75);", i * 150);
            setTimeout("M.checkScore(" + i + ");FCFadeUp('tda" + i + "',75);", (i * 150) + 76);
        }
        i++;
        setTimeout("M.totalScore();", i * 150);
    }

    // Mark each answer as correct/incorrect
    this.checkScore = function (i) {
        // correct
        var answer = FCGid('tda' + i).getAttribute("answer");
        var question = FCGid('tdq' + i).getAttribute("question");

        FCGid('tda' + i).style.fontWeight = 'bold';
        if (question == answer) {
            FCGid('tda' + i).style.color = 'rgb(0,128,0)';
        }
        else {
            FCGid('tda' + i).style.color = 'rgb(170,0,0)';
        }
    }

    // Calculate and show total score
    // If all correct, load next question. If wrong, redo.
    this.totalScore = function () {
        var wrong = 0;
        for (var i = 0; i < this.questionSlice.length; i++) {
            var answer = FCGid('tda' + i).getAttribute("answer");
            var question = FCGid('tdq' + i).getAttribute("question");
            if (question != answer) wrong++;
        }

        // wrong, redo
        if (wrong) {
            FCGid('score').innerHTML = '<a href="javascript:FCLoadNew(2);void(0)">Reset and try again</a>';
            FCGid('scorel').innerHTML = '<b style="color:rgb(170,0,0)">You missed ' + wrong + ' out of ' + this.questionSlice.length + '</b>';
        }

        // right
        else {
            // next set of matching
            if (this.matchStart + this.matchInc < each.length) {
                FCGid('scorel').innerHTML = '<b>100% Correct!</b>';
                FCGid('score').innerHTML = 'Loading next matching group';
                this.matchStart += this.matchInc;
                setTimeout("FCLoadNew(2)", 500);
            }

            // go to next step
            else {
                FCGid('scorel').innerHTML = '<b>100% Correct!</b>';
                FCGid('score').innerHTML = '<a href="javascript:FCLoadNew(3);void(0)">Go to Step 3: Multiple Choice &raquo;</a>';
                this.matchStart = 0;
            }
        }
    }
}


// MULTI CHOICE
function MultipleChoice(questions) {
    this.questions = questions;
    this.redo = new Array();
    this.current = 0;
    this.choices = new Array();

    // Initialize Multiple Choice
    //  - Clear content and load first question.
    this.init = function () {
        // Shuffle questions
        this.questions.sort(randOrd);

        this.current = 0;
        this.redo = new Array();

        // Mark table as currently on Multiple Choice
        var table = FCGid('contenttable');
        table.cellSpacing = 0;
        table.className = 'multi';

        // Clear content
        var rows = table.getElementsByTagName('tr').length;
        for (i = 0; i < rows; i++) table.deleteRow(0);

        // Load multiple choice HTML
        var tr = table.insertRow(-1);
        var td = tr.insertCell(-1);
        td.id = 'question';

        var tr = table.insertRow(-1);
        var td = tr.insertCell(-1);
        td.id = 'answers';

        var tr = table.insertRow(-1);
        var td = tr.insertCell(-1);
        td.id = 'status';
        td.innerHTML = '&nbsp;';

        // Load first multiple choice question
        this.loadQuestion();
    }

    // Next multiple choice
    // Switch to next question
    this.next = function () {
        var i = this.current;
        i++;
        if (this.questions[i]) {
            this.current = i;
            FCFadeDown('question', 100);
            FCFadeDown('answers', 100);
            FCFadeDown('status', 100);
            var x = setTimeout("MC.loadQuestion(); FCFadeUp('question',100); FCFadeUp('answers',100); FCFadeUp('status',100);", 101);
        }
        else this.done();
    }

    // Load question
    // Inserts question HTML
    this.loadQuestion = function () {
        FCGid('question').innerHTML = this.questions[this.current].question;

        // get right answer
        var correctAnswer = this.questions[this.current];

        var tmpQuestions = this.questions.slice(0); // Make a copy of the array
        tmpQuestions.sort(randOrd);

        // Add correct answer and 3 wrong answers to possible choices
        this.choices = new Array(correctAnswer);
        for (var i in tmpQuestions) {
            var question = tmpQuestions[i];
            if (question.num != correctAnswer.num)
                this.choices.push(question);
            if (this.choices.length >= 4)
                break;
        }

        // Then randomize the choices
        this.choices.sort(randOrd);

        // Write answers
        FCGid('answers').innerHTML = '';
        for (var i = 0; i < this.choices.length; ++i) {
            choice = this.choices[i];
            letter = String.fromCharCode(i + 97);
            FCGid('answers').innerHTML += letter + ') <a href="javascript:MC.submitAnswer(' + choice.num + ');void(0)" id="ans' + choice.num + '">' + choice.answer + '</a><br/>';
        }

        // Make mark space
        FCGid('status').innerHTML = '&nbsp;';
    }

    // Submit answer
    // Mark correct and move to next question if answer is correct,
    // else, mark incorrect, and add question back to end of questions
    this.submitAnswer = function (guess) {
        ans = FCGid('ans' + guess);

        // If the guess is correct
        if (guess == this.questions[this.current].num) {
            // Mark it as correct
            FCFadeDown('status', 100);
            ans.href = 'javascript:MC.next();void(0)';
            setTimeout("FCGid('status').style.color='rgb(0,0,0)';FCGid('status').innerHTML='Correct! Get ready...';    FCGid('ans" + guess + "').innerHTML+=' - Correct!'; FCGid('ans" + guess + "').style.color='rgb(0,170,0)'; FCFadeUp('status',100); ", 101);

            setTimeout('MC.next()', 500);

            // Fade wrong answers
            for (var i in this.choices) {
                var guessNum = this.choices[i].num;
                if ((guessNum != guess) && (FCGid('ans' + guessNum))) FCGid('ans' + guessNum).style.color = 'rgb(170,170,170)';
            }
        }

        // If wrong
        else {
            // Add question to back of list
            if (this.redo[this.current] != 1) {
                this.questions.push(this.questions[this.current])
                this.redo[this.current] = 1;
            }

            // Mark as incorrect
            FCFadeDown('ans' + guess, 100);
            FCFadeDown('status', 100);
            setTimeout("FCGid('ans" + guess + "').style.textDecoration='line-through'; FCGid('ans" + guess + "').style.color='rgb(213,0,0)'; FCGid('status').style.color='rgb(170,0,0)'; FCGid('status').innerHTML='Incorrect, try again.'; FCFadeUp('ans" + guess + "',100); FCFadeUp('status',100)", 101);
        }
    }

    // Done
    // Finished with Multiple Choice
    this.done = function () {
        FCFadeDown('question', 100);
        FCFadeDown('answers', 100);
        FCFadeDown('status', 100);
        var link = '<center>Multiple Choice Complete!</center>';
        var x = setTimeout("FCGid('question').innerHTML='" + link + "'; FCGid('status').innerHTML='&nbsp;'; FCGid('answers').innerHTML='&nbsp;'; FCFadeUp('question',100);", 101);
    }
}


// GENERAL
// fade in new content
function FCLoadNew(game) {
    var task;
    if (game == 1) task = 'FC.init';
    else if (game == 2) task = 'M.init';
    else if (game == 3) task = 'MC.init';

    FCFadeDown('contenttable', 150);
    var x = setTimeout(task + "();FCFadeUp('contenttable',150);", 151);

    var tabs = FCGid('itemtabs').getElementsByTagName('a');
    for (i = 0; i < tabs.length; i++) tabs[i].className = '';

    game--;
    tabs[game].className = 'itemtab';
}

// fade object's opac
function FCFadeDown(id, time) {
    var inc = time / 5;
    var a = setTimeout("FCOpac('" + id + "',80)", inc);
    var b = setTimeout("FCOpac('" + id + "',60)", inc * 2);
    var c = setTimeout("FCOpac('" + id + "',40)", inc * 3);
    var d = setTimeout("FCOpac('" + id + "',20)", inc * 4);
    var e = setTimeout("FCOpac('" + id + "',0)", inc * 5);
}

function FCFadeDownHalf(id, time) {
    var inc = time / 5;
    var a = setTimeout("FCOpac('" + id + "',90)", inc);
    var b = setTimeout("FCOpac('" + id + "',75)", inc * 2);
    var c = setTimeout("FCOpac('" + id + "',50)", inc * 3);
    var d = setTimeout("FCOpac('" + id + "',45)", inc * 4);
    var e = setTimeout("FCOpac('" + id + "',30);FCGid('" + id + "').style.color='rgb(0,0,0)'", inc * 5);
}

function FCFadeUp(id, time) {
    var inc = time / 5;
    var a = setTimeout("FCOpac('" + id + "',20)", inc);
    var b = setTimeout("FCOpac('" + id + "',40)", inc * 2);
    var c = setTimeout("FCOpac('" + id + "',60)", inc * 3);
    var d = setTimeout("FCOpac('" + id + "',70)", inc * 4);
    var e = setTimeout("FCOpac('" + id + "',100)", inc * 5);
}

// GENERIC
function FCGid(i) {
    return document.getElementById(i);
}
function FCOpac(id, n) {
    FCGid(id).style.filter = 'alpha(opacity=' + n + ')';
    FCGid(id).style.opacity = n / 100;
}
function randOrd() {
    return(Math.round(Math.random()) - 0.5);
}

document.write(
    '<link rel="stylesheet" href="/static/embed.css" type="text/css"/>' +
        '<div id="studybulb">' +
        '<span id="itemtabs">' +
        '    <a href="javascript:FCLoadNew(1);void(0)" style="border-left-width:1px">1. Flashcards</a>' +
        '    <a href="javascript:FCLoadNew(2);void(0)">2. Matching</a>' +
        '    <a href="javascript:FCLoadNew(3);void(0)">3. Multiple Choice</a>' +
        '</span>' +
        '<table id="contenttable" cellspacing="0"><tr><td></td></tr></table>' +
        '</div>'
);

FCLoadNew(1);