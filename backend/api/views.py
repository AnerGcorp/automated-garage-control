from rest_framework import viewsets
from .serializers import SoldierSerializer, OfficerSerializer, \
    CarModelSerializer, DutySerializer, CarMovementSerializer, \
    MilitaryBaseSerializer, CloseRelativeSerializer, \
    CustomCarMovementSerializer
from .models import BeenMilitaryBase, CloseRelative, Soldier, \
    Officer, CarModel, Duty, CarMovement
from django.shortcuts import render
from datetime import date, datetime, timedelta

# Create your views here.
class MilitaryBaseViewSet(viewsets.ModelViewSet):
    queryset = BeenMilitaryBase.objects.all().order_by("id")
    serializer_class = MilitaryBaseSerializer

class CloseRelativeViewSet(viewsets.ModelViewSet):
    queryset = CloseRelative.objects.all().order_by("id")
    serializer_class = CloseRelativeSerializer

class SoldierViewSet(viewsets.ModelViewSet):
    queryset = Soldier.objects.all().order_by("surname")
    serializer_class = SoldierSerializer

class OfficerViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.all().order_by('military_title')
    serializer_class = OfficerSerializer

class CarModelViewSet(viewsets.ModelViewSet):
    # queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

    def get_queryset(self):
        # print(self.request.query_params)
        if self.request.query_params.get("getcar"):
            rfid = self.request.query_params.get("getcar")
            query = "SELECT * \
                FROM api_carmodel \
                WHERE \
                    rfid='{}'".format(rfid)
            queryset = CarModel.objects.raw(query)
            return queryset

        if self.request.query_params.get("all") == "true":
            # query = "SELECT * \
            #     FROM api_carmodel"
            # queryset = CarModel.objects.raw(query)
            queryset = CarModel.objects.all()
            return queryset

    #     # # serializer_class = CarModelSerializer
    #     # return queryset

class DutyViewSet(viewsets.ModelViewSet):
    queryset = Duty.objects.all().order_by('-date')
    serializer_class = DutySerializer

class CarMovementViewSet(viewsets.ModelViewSet):
    # today = date.today()
    queryset = CarMovement.objects.all().order_by('-time')
    serializer_class = CarMovementSerializer

class CustomCarMovementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomCarMovementSerializer

    def get_queryset(self):

        # print(self.request.query_params)

        today = date.today().strftime("%Y-%m-%d 00:00:00")
        tomorrow = date.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y-%m-%d 00:00:00")
        # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # print("Displaying DATES")
        # print("NOW", now)
        # print("TODAY", today)
        # print("TOMORROW", tomorrow)
        if self.request.query_params.get("enter") == "true":
            query = "SELECT * \
                FROM api_carmovement \
                WHERE \
                    movement='Girdi' \
                AND \
                    time \
                BETWEEN \
                    CAST('{0}' AS DATETIME) \
                AND \
                    CAST('{1}' AS DATETIME)".format(today, tomorrow)
            queryset = CarMovement.objects.raw(query)
            return queryset

        if self.request.query_params.get("exit") == "true":
            query = "SELECT * \
                FROM api_carmovement \
                WHERE \
                    movement='Çykdy' \
                AND \
                    time \
                BETWEEN \
                    CAST('{0}' AS DATETIME) \
                AND \
                    CAST('{1}' AS DATETIME)".format(today, tomorrow)
            queryset = CarMovement.objects.raw(query)
            return queryset

        if self.request.query_params.get("all") == "true":
            query = "SELECT * \
                FROM api_carmovement \
                WHERE \
                    time \
                BETWEEN \
                    CAST('{0}' AS DATETIME) \
                AND \
                    CAST('{1}' AS DATETIME)".format(today, tomorrow)
            queryset = CarMovement.objects.raw(query)
            return queryset

        if self.request.query_params.get("getlast"):
            carId = self.request.query_params.get("getlast")
            print(carId)
            query = "SELECT * \
                FROM api_carmovement \
                WHERE \
                    car_id = {0} \
                AND \
                    time \
                BETWEEN \
                    CAST('{1}' AS DATETIME) \
                AND \
                    CAST('{2}' AS DATETIME) \
                ORDER BY id DESC \
                LIMIT 1".format(carId, today, tomorrow)
            queryset = CarMovement.objects.raw(query)
            return queryset

        queryset = CarMovement.objects.all()
        return queryset

# class CarsInsideViewSet(viewsets.ModelViewSet):
#     # get date
#     today = date.today().strftime("%Y-%m-%d 00:00:00")
#     tomorrow = date.today() + timedelta(days=1)
#     tomorrow = tomorrow.strftime("%Y-%m-%d 00:00:00")
#     # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # print("Displaying DATES")
#     # print("NOW", now)
#     # print("TODAY", today)
#     # print("TOMORROW", tomorrow)

#     query = "SELECT * \
#         FROM api_carmovement \
#         WHERE \
#             movement='Girdi' \
#         AND \
#             time \
#         BETWEEN \
#             CAST('{0}' AS DATETIME) \
#         AND \
#             CAST('{1}' AS DATETIME)".format(today, tomorrow)

#     queryset = CarMovement.objects.raw(query)
#     serializer_class = CarsInsideSerializer

# class CarsOutsideViewSet(viewsets.ModelViewSet):
#     # get date
#     today = date.today().strftime("%Y-%m-%d 00:00:00")
#     tomorrow = date.today() + timedelta(days=1)
#     tomorrow = tomorrow.strftime("%Y-%m-%d 00:00:00")
#     # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # print("Displaying DATES")
#     # print("NOW", now)
#     # print("TODAY", today)
#     # print("TOMORROW", tomorrow)

#     query = "SELECT * \
#         FROM api_carmovement \
#         WHERE \
#             movement='Çykdy' \
#         AND \
#             time \
#         BETWEEN \
#             CAST('{0}' AS DATETIME) \
#         AND \
#             CAST('{1}' AS DATETIME)".format(today, tomorrow)

#     queryset = CarMovement.objects.raw(query)

#     serializer_class = CarsInsideSerializer