from urllib.parse import urljoin

from django.urls import path, include

import core.routers

API_V1_PREFIX = "v1/"

urlpatterns = [
    path(API_V1_PREFIX, include(core.routers.form_router.urls)),
    path(API_V1_PREFIX, include(core.routers.form_retrieve_router.urls)),
    path(API_V1_PREFIX, include(core.routers.question_router.urls)),
    path(API_V1_PREFIX, include(core.routers.answer_option_router.urls)),
    path(API_V1_PREFIX, include(core.routers.form_response_router.urls)),
    path(API_V1_PREFIX, include("rest_framework.urls")),
    path(urljoin(API_V1_PREFIX, "auth/"), include("djoser.urls")),
    path(urljoin(API_V1_PREFIX, "auth/"), include("djoser.urls.authtoken")),
]
