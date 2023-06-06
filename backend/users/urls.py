from django.urls import include, path
from users.views import UserSubscribeView, UserSubscriptionsViewSet

app_name = 'users'


urlpatterns = [
    path(
        'users/subscriptions/',
        UserSubscriptionsViewSet.as_view({'get': 'list'}),
    ),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
