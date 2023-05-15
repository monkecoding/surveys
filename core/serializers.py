from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from core import utils
from core.models import Form, Question, AnswerOption, FormResponse, QuestionResponse


class UserConnectionSerializerMixin(serializers.ModelSerializer):
    def create(self, validated_data):
        (
            validated_data['ip'],
            validated_data['user_agent'],
        ) = utils.get_client_connection(self.context["request"])
        return super().create(validated_data)


class AnswerOptionSerializer(
    UserConnectionSerializerMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = AnswerOption
        fields = (
            'id',
            'text',
            'num',
            'question',
        )


class QuestionSerializer(
    UserConnectionSerializerMixin,
    serializers.ModelSerializer,
):
    answer_options = serializers.SerializerMethodField()

    @staticmethod
    def get_answer_options(question):
        serializer = AnswerOptionSerializer(
            instance=AnswerOption.objects.filter(question=question).order_by("num"), many=True
        )
        return serializer.data

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'num',
            'form',
            'type',
            'is_required',
            'is_multiple_allowed',
            'is_other_allowed',
            'answer_options',
        )


class FormSerializer(
    UserConnectionSerializerMixin,
    serializers.ModelSerializer,
):
    questions = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=CurrentUserDefault())

    @staticmethod
    def get_questions(form):
        serializer = QuestionSerializer(
            instance=Question.objects.filter(form=form).order_by("num"), many=True
        )
        return serializer.data

    class Meta:
        model = Form
        fields = (
            'id',
            'title',
            'user',
            'questions',
        )


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = (
            'id',
            'question',
            'answer_options',
            'free_input_text',
        )

    def validate(self, data):
        question = data.get("question")
        answer_options = data.get("answer_options")
        free_input_text = data.get("free_input_text")
        form = self.context['form']

        if form != question.form:
            raise serializers.ValidationError("Invalid question.")

        if answer_options:
            options_ids = {x.id for x in answer_options}
            if question.answeroption_set.filter(id__in=options_ids).count() != len(options_ids):
                raise serializers.ValidationError("Invalid answer options.")

        if question.is_required:
            if not answer_options and not free_input_text:
                raise serializers.ValidationError("This question is required.")

        if not question.is_other_allowed:
            if free_input_text:
                raise serializers.ValidationError("Free input is not allowed.")

        if not question.is_multiple_allowed:
            if answer_options and (free_input_text or len(answer_options) > 1):
                raise serializers.ValidationError("Multiple answer is not allowed.")
        return data


class FormResponseSerializer(
    UserConnectionSerializerMixin,
    serializers.ModelSerializer
):
    class Meta:
        model = FormResponse
        fields = (
            'id',
            'form',
        )
