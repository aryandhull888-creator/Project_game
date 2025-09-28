from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def check_guess(guess, answer):
    """Checks a guess and returns a list of colors (grey, orange, green)."""
    result = ['grey'] * 5
    answer_list = list(answer)
    guess_list = list(guess)


    for i in range(5):
        if guess_list[i] == answer_list[i]:
            result[i] = 'green'
            answer_list[i] = None 
            guess_list[i] = None 

    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in answer_list:
            result[i] = 'orange'
            answer_list[answer_list.index(guess_list[i])] = None 

    return result

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request, 'game/register.html', {'form': form})


# game/views.py (add these below the register view)
from django.contrib.auth.decorators import login_required
from .models import Word, GameSession
from django.utils import timezone
from django.http import Http404

@login_required
def home(request):
    # A simple home page view
    return render(request, 'game/home.html')

@login_required
def start_game(request):
    today = timezone.now().date()
    games_today = GameSession.objects.filter(player=request.user, start_time__date=today).count()

    if games_today >= 3:
        messages.warning(request, 'You have already played your 3 games for today. Please come back tomorrow!')
        return redirect('home')

    # Find a new random word the user hasn't played today
    words_played_today_ids = GameSession.objects.filter(player=request.user, start_time__date=today).values_list('word_to_guess_id', flat=True)
    word_to_guess = Word.objects.exclude(id__in=words_played_today_ids).order_by('?').first()

    if not word_to_guess:
        # This happens if user has played all words in the database
        messages.error(request, 'Wow, you have played all the available words!')
        return redirect('home')

    new_game = GameSession.objects.create(player=request.user, word_to_guess=word_to_guess)
    return redirect('game-play', session_id=new_game.id)

@login_required
def game_play(request, session_id):
    try:
        game_session = GameSession.objects.get(id=session_id, player=request.user)
    except GameSession.DoesNotExist:
        raise Http404("Game session not found or you do not have permission to view it.")

    if request.method == 'POST':
        if game_session.is_finished:
            return redirect('game-play', session_id=session_id)

        guess = request.POST.get('guess', '').upper()
        if len(guess) == 5:
            current_guesses_count = sum([1 for g in [game_session.guess1, game_session.guess2, game_session.guess3, game_session.guess4, game_session.guess5] if g])
            if current_guesses_count < 5:
                setattr(game_session, f'guess{current_guesses_count + 1}', guess)

            if guess == game_session.word_to_guess.text:
                game_session.is_won = True
                game_session.is_finished = True
                messages.success(request, 'Congratulations! You guessed the word correctly!')
            elif current_guesses_count == 4: 
                game_session.is_finished = True
                messages.info(request, f'Better luck next time! The word was {game_session.word_to_guess.text}.')

            game_session.save()
        else:
            messages.error(request, 'Your guess must be 5 letters long.')

        return redirect('game-play', session_id=session_id)

    guesses_with_feedback = []
    all_guesses = [game_session.guess1, game_session.guess2, game_session.guess3, game_session.guess4, game_session.guess5]
    for g in all_guesses:
        if g:
            feedback = check_guess(g, game_session.word_to_guess.text)
            guesses_with_feedback.append(list(zip(g, feedback)))

    # This is the corrected code
    remaining_guesses_count = 5 - len(guesses_with_feedback)

    context = {
        'game_session': game_session,
        'guesses_with_feedback': guesses_with_feedback,
        'remaining_guesses_range': range(remaining_guesses_count) # Add this line
    }
    return render(request, 'game/game_board.html', context)