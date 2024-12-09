from django.urls import path
from .views import UserRegistrationView, ParticipantScoresAPIView, ParticipantsScoresAPIView, SetScoreView, GetCriterios, GetPart, ParticipantsAdd

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('participant_scores/<int:participant_id>/', ParticipantScoresAPIView.as_view(), name='participant_scores'),
    path('participants_scores/', ParticipantsScoresAPIView.as_view(), name='participants_scores'),
    path('add-participant/', ParticipantsAdd.as_view(), name='add-participant'),
    path('set-score/', SetScoreView.as_view(), name='Set-score'),
    path('get-part/', GetPart.as_view(), name='Get-Part'),
    path('get-criterios/', GetCriterios.as_view(), name='Get-Criterios'),
]