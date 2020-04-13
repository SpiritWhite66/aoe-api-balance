from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path('api/v1/match/', # urls list all and create new one
        views.MatchReadCreate.as_view(),
        name='MatchReadCreate'
    ),
    path('api/v1/balancer/', # urls list all and create new one
        views.Balancer.as_view(),
        name='Balancer'
    )
]