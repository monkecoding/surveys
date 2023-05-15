from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Form, Question, FormResponse, AnswerOption
from core.serializers import FormSerializer, QuestionSerializer, FormResponseSerializer, QuestionResponseSerializer, \
    AnswerOptionSerializer


class FormViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class FormRetrieveViewSet(mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        q = Q(form__user=self.request.user)
        if form_id := self.kwargs.get("form_id"):
            q &= Q(form_id=form_id)
        return qs.filter(q)


class AnswerOptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        q = Q(question__form__user=self.request.user)
        if question_id := self.kwargs.get("question_id"):
            q &= Q(question_id=question_id)
        return qs.filter(q)


class FormResponseViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    queryset = FormResponse.objects.all()
    serializer_class = FormResponseSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        form_data = request.data
        question_response_data = form_data.pop("question_responses", [])
        serializer = self.get_serializer(data=form_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        form_response = serializer.instance

        question_responses = []
        for question_response_data in question_response_data:
            question_response_serializer = QuestionResponseSerializer(
                data=question_response_data, context={'form': serializer.instance.form}
            )
            question_response_serializer.is_valid(raise_exception=True)
            question_response_serializer.validated_data["form_response_id"] = form_response.id
            question_response = question_response_serializer.save()
            question_responses.append(question_response)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
