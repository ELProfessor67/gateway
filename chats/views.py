from django.shortcuts import render,HttpResponse
from .models import Questions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import json


data =  Questions.objects.all().values()

questions = [item['question'] for item in data]
answers = [item['answer'] for item in data]

print(questions)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Train classifier
classifier = LinearSVC()
classifier.fit(X, questions)


simple_responses = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! What can I help you with?",
    "hey": "Hey! How can I assist you?",
    "good morning": "Good morning! How can I help you?",
    "good afternoon": "Good afternoon! What can I do for you?",
    "good evening": "Good evening! How can I assist you?"
}


def get_answer(question):
    # Convert question to lower case to handle case insensitivity
    question = question.lower()

    # Check for simple responses
    if question in simple_responses:
        return simple_responses[question]

    # Proceed with machine learning model for other questions
    question_vec = vectorizer.transform([question])
    predicted_question = classifier.predict(question_vec)[0]
    
    for item in data:
        if item['question'] == predicted_question:
            return item['answer']
    
    return "Sorry, I don't have an answer for that question."

# Create your views here.
def customerService(request):
    questions = Questions.objects.all()
    return render(request,"customer-service/chat.html",{"questions": questions})


def getAnswer(request):
    question = request.GET.get("question")
    answer = get_answer(question)

   
    if answer is not None:
        
        answer = answer.replace(r"\n","<br/>")
        
        return HttpResponse(answer)
    else:
        return HttpResponse("Please Send Your query on customer support email.")

