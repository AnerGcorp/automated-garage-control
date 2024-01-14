from django.urls import include, path
from rest_framework import routers
from . import views

# app_name = "api"

router = routers.DefaultRouter()
router.register(r'militarybase', views.MilitaryBaseViewSet)
router.register(r'closerelative', views.CloseRelativeViewSet)
router.register(r'soldiers', views.SoldierViewSet)
router.register(r'officers', views.OfficerViewSet)
router.register(r'carmodels', views.CarModelViewSet, basename="carmodel")
router.register(r'duties', views.DutyViewSet)
router.register(r'carmovements', views.CarMovementViewSet)
# customized car movements
router.register(r'customcarmovements', views.CustomCarMovementViewSet, basename="carmovement")
# router.register(r"inside", views.CarsInsideViewSet, basename="CarMovement")
# router.register(r"outside", views.CarsOutsideViewSet, basename="CarMovement")
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]