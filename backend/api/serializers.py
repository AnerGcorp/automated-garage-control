from rest_framework import serializers
from .models import Soldier, BeenMilitaryBase, CloseRelative, \
        Officer, CarModel, Duty, CarMovement

class MilitaryBaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BeenMilitaryBase
        fields = (
            "id",
            "url",
            "military_base",
            "military_base_enter_date",
            "military_base_exit_date",
            "belongs_to"
        )

class CloseRelativeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CloseRelative
        fields = (
            "id",
            "url",
            "birth_year",
            "aaa_field",
            "work_place_and_position",
            "belongs_to"
        )

class SoldierSerializer(serializers.HyperlinkedModelSerializer):
    soldier_base = MilitaryBaseSerializer(many=True)
    soldier_relative = CloseRelativeSerializer(many=True)

    class Meta:
        model = Soldier
        fields = (
            "id",
            "url",
            "military_title",
            "photo",
            "name",
            "surname",
            "last_name",
            "birthday",
            "birth_place",
            "nationality",
            "knowledge",
            "marriage_status",
            "invited_hw",
            "being_abroad",
            "last_job",
            "last_illness",
            "harby_kasam_date",
            "being_in_prison",
            "home_address",
            "specific_notes",
            "soldier_relative",
            "soldier_base"
            )

class OfficerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Officer
        fields = (
            "id",
            "url",
            "military_title",
            "name",
            "surname",
            "last_name",
            "position",
            "photo",
            "note"
        )

class CarModelSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="carmodel-detail")
    # patron = OfficerSerializer()
    # driver = SoldierSerializer()

    class Meta:
        model = CarModel
        fields = (
            "id",
            "rfid",
            "url",
            "model_car",
            "license_number",
            "patron",
            "driver",
            "corr_principal",
            "car_photo",
            "note"
        )

class DutySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Duty
        fields = (
            "id",
            "url",
            "place",
            "position",
            "on_duty",
            "note"
        )

class CarMovementSerializer(serializers.HyperlinkedModelSerializer):
    # car = CarModelSerializer()

    class Meta:
        model = CarMovement
        fields = (
            "id",
            "url",
            "car",
            "time",
            "movement",
            "screenshot",
            "note"
        )

class CustomCarMovementSerializer(serializers.HyperlinkedModelSerializer):
    car = CarModelSerializer()

    class Meta:
        model = CarMovement
        fields = (
            "id",
            "url",
            "car",
            "time",
            "movement",
            "screenshot",
            "note"
        )

# class CarsInsideSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CarMovement
#         fields = "__all__"

# class CarsOutsideSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CarMovement
#         fields = "__all__"