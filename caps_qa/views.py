from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, UserProfile
from .forms import SignUpForm, UserProfileForm
from django.shortcuts import get_object_or_404

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})

@login_required
def home(request):
    question = Question.objects.order_by('?').first()
    
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        Answer.objects.create(question=question, text=answer_text, user=request.user)
        return redirect('home')
    
    return render(request, 'home.html', {'question': question})