document.addEventListener("DOMContentLoaded", function() {
    let currentQuestionIndex = 0;
    let questionsJson = document.getElementById('content').getAttribute('data-questions');
    questionsJson = questionsJson.replace(/[\x00-\x1F\x7F-\x9F]/g, "");
    questionsJson = questionsJson.replace(/&nbsp;/g, " ");
    questionsJson = questionsJson.replace(/\s+/g, ' ').trim();
    let questions = JSON.parse(questionsJson);
    const content = document.getElementById('content');
    const btn = document.getElementById('revealBtn');
    
function displayQuestion() {
    if (currentQuestionIndex < questions.length) {
        const question = questions[currentQuestionIndex].fields.question_text;
        const answer = questions[currentQuestionIndex].fields.answer_text;
        content.innerHTML = `<div class='question'>Question: ${question}</div><div class='answer' style='display: none;'>Answer: ${answer}</div>`;
    } else {
        content.innerHTML = `<div class='message'>"No more questions."</div>`;
        btn.style.display = "none";
    }
}

displayQuestion();

btn.addEventListener("click", function() {
    const answerElement = content.querySelector('.answer');
    if (btn.textContent === "Reveal Answer") {
        answerElement.style.display = "block";
        btn.textContent = "Next Question";
    } else {
        currentQuestionIndex++;
        displayQuestion();
    }
});
});