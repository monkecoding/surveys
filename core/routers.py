from rest_framework import routers

from core.views import FormViewSet, FormRetrieveViewSet, QuestionViewSet, AnswerOptionViewSet, FormResponseViewSet

form_router = routers.SimpleRouter()
form_router.register("form", FormViewSet, "form")

form_retrieve_router = routers.SimpleRouter()
form_retrieve_router.register("form-retrieve", FormRetrieveViewSet, "form-retrieve")

question_router = routers.SimpleRouter()
question_router.register("question", QuestionViewSet, "question")

answer_option_router = routers.SimpleRouter()
answer_option_router.register("answer-option", AnswerOptionViewSet, "answer-option")

form_response_router = routers.SimpleRouter()
form_response_router.register("form-response", FormResponseViewSet, "form-response")