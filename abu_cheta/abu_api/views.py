from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserRegistrationSerializer, SetScoreSerializer, ParticipantSerializer, CriteriosSerializer
from .models import Participant, Scores, Criterios, CustomUser
from rest_framework.exceptions import NotFound
from django.db import IntegrityError

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SetScoreView(APIView):
    def post(self, request):
        serializer = SetScoreSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                participant = Participant.objects.get(id=data["participant_id"])
                juri = CustomUser.objects.get(id=data["juri_id"])
                criterion = Criterios.objects.get(id=data["criterion_id"])

                score, created = Scores.objects.update_or_create(
                    participiant=participant,
                    juri_id=juri,
                    criterion_id=criterion,
                    stage=data["stage"],
                    defaults={"score": data["score"]}
                )

                return Response({
                    "score_id": score.id,
                    "updated": not created
                }, status=status.HTTP_200_OK)
            except (Participant.DoesNotExist, CustomUser.DoesNotExist, Criterios.DoesNotExist):
                return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ParticipantScoresAPIView(APIView):
    def get(self, request, *args, **kwargs):
        participant_id = kwargs.get('participant_id')  # Получаем id участника из URL
        stage = request.query_params.get('stage')  # Получаем стадию из query параметров

        if not stage:
            return Response({"error": "Stage is required"}, status=400)

        # Проверка на существование участника
        try:
            participant = Participant.objects.prefetch_related(
                'Participiant__criterion_id', 'Participiant__juri_id'
            ).get(id=participant_id)
        except Participant.DoesNotExist:
            raise NotFound(detail="Participant not found", code=404)

        # Получаем все оценки для участника по определенной стадии
        participant_scores = participant.Participiant.filter(stage=stage)
        
        # Собираем данные для ответа
        criteries_data = {}

        for score in participant_scores:
            criterion_name = score.criterion_id.criterion
            jury_name = score.juri_id.fullname

            # Если критерий еще не добавлен, инициализируем его
            if criterion_name not in criteries_data:
                criteries_data[criterion_name] = {"name": criterion_name, "scores": []}

            criteries_data[criterion_name]["scores"].append({
                "jury": jury_name,
                "score": int(score.score)
            })

        # Вычисляем общую сумму баллов
        total_score = sum(int(score.score) for score in participant_scores)

        # Формируем ответ
        response_data = {
            "participants": participant.full_name,
            "criteries": list(criteries_data.values()),
            "scoreSum": total_score,
        }

        return Response(response_data)

class ParticipantsScoresAPIView(APIView):
    def get(self, request, *args, **kwargs):
        stage = request.query_params.get('stage')
        if not stage:
            return Response({"error": "Stage is required"}, status=400)

        # Получение всех участников и их оценок для указанной стадии
        participants = Participant.objects.prefetch_related(
            'Participiant__criterion_id', 'Participiant__juri_id'
        ).all()

        response_data = []

        for participant in participants:
            participant_scores = participant.Participiant.filter(stage=stage)
            criteries_data = {}

            for score in participant_scores:
                criterion_name = score.criterion_id.criterion
                jury_name = score.juri_id.fullname

                # Если критерий еще не добавлен, инициализируем его
                if criterion_name not in criteries_data:
                    criteries_data[criterion_name] = {"name": criterion_name, "scores": []}

                criteries_data[criterion_name]["scores"].append({
                    "jury": jury_name,
                    "score": int(score.score)
                })

            # Вычисление общей суммы баллов
            total_score = sum(
                int(score.score) for score in participant_scores
            )

            response_data.append({
                "participants": participant.full_name,
                "criteries": list(criteries_data.values()),
                "scoreSum": total_score,
            })

        return Response(response_data)

class ParticipantsAdd(APIView):
    def post(self, request):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                # Создание нового участника
                Participant.objects.create(
                    full_name=data['full_name'],
                    place_of_study=data['place_of_study'],
                    teacher_full_name=data.get('teacher_full_name'),
                    teacher_phone=data.get('teacher_phone')
                )
                return Response({'Response': 'Participant created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # Обработка ошибок базы данных, например уникальных ограничений
                return Response({'error': 'Database integrity error', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Общая обработка ошибок
                return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Если данные невалидны
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPart(APIView):
    def get(self, request):
        if request.query_params.get('part_id', None):
            part_data = Participant.objects.get(id = request.query_params.get('part_id'))
            serializer = ParticipantSerializer(part_data)
            return Response(serializer.data)
        else:
            parts_data = Participant.objects.all()
            serializer = ParticipantSerializer(parts_data, many=True)
            return Response(serializer.data)
        
class GetCriterios(APIView):
    def get(self, request):
        criterios = Criterios.objects.filter(stage = request.query_params.get('stage'))
        serializer = CriteriosSerializer(criterios, many=True)
        return Response(serializer.data)
