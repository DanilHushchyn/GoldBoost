import json

import pytest
from ninja_extra.testing import TestClient
from src.main.utils import make_request

from src.users.api import UsersController
from src.users.models import User, Character, Subscriber
from src.users.schemas import UserOutSchema, CharacterOutSchema, MessageOutSchema


client = TestClient(UsersController)

headers = {
    'Accept-Language': 'en'
}


@pytest.mark.django_db
class TestUsersController:
    def test_get_my_profile(self, access_token):
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-profile/',
                                          schema=UserOutSchema,
                                          client=client,
                                          headers=headers)
        assert is_valid is True
        assert response.status_code == 200

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         {
                                             "first_name": "string",
                                             "last_name": "string",
                                             "payment_method": "PayPal",
                                             "communication": "Telegram",
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "first_name": "Jack",
                                             "last_name": "Dawkins",
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "communication": "Telegramchik",
                                         },
                                         422,
                                         False,
                                 ),
                                 (
                                         {
                                             "payment_method": "PayPALL",
                                         },
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_update_my_profile(self, payload, expected_status,
                               schema_status, access_token):
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-profile/',
                                          schema=UserOutSchema,
                                          client=client,
                                          method='patch',
                                          payload=json.dumps(payload),
                                          headers=headers)
        if response.status_code == 200:
            for key, value in payload.items():
                if isinstance(value, bool):
                    assert value is payload[key]
                else:
                    assert value == payload[key]

        assert is_valid is schema_status
        assert response.status_code == expected_status

    def test_create_default_character(self, access_token):
        headers['Authorization'] = access_token
        Character.objects.all().delete()
        for i in range(1, 4):
            response, is_valid = make_request(request_str=f'/create-default-character/',
                                              schema=CharacterOutSchema,
                                              method='post',
                                              client=client,
                                              headers=headers)
            if i == 4:
                assert is_valid is False
                assert response.status_code == 409
            else:
                assert is_valid is True
                assert response.status_code == 200

    def test_get_my_characters(self, access_token):
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-characters/',
                                          schema=CharacterOutSchema,
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200

    def test_delete_character_by_id(self, access_token):
        user = User.objects.get(email='user@example.com')
        char_id = Character.objects.filter(user=user).last().id
        headers['Authorization'] = access_token
        response, is_valid = make_request(request_str=f'/my-character/{char_id}',
                                          schema=MessageOutSchema,
                                          method='delete',
                                          client=client,
                                          headers=headers)

        assert is_valid is True
        assert response.status_code == 200
        response, is_valid = make_request(request_str=f'/my-character/{char_id}',
                                          schema=MessageOutSchema,
                                          method='delete',
                                          client=client,
                                          headers=headers)
        assert is_valid is False
        assert response.status_code == 404

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         {
                                             "battle_tag": "battle_tag",
                                             "name": "name",
                                             "faction": "Alliance",
                                             "additional_info": "",
                                             "class_and_spec": "Paladin",
                                             "realm": ""
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "additional_info": "super",
                                             "realm": "realm"
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "class_and_spec": "Paladinchik"
                                         },
                                         422,
                                         False,
                                 ),
                                 (
                                         {
                                             "faction": "Allianceeee"
                                         },
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_update_my_character(self, payload, expected_status,
                                 schema_status, access_token):
        headers['Authorization'] = access_token
        user = User.objects.get(email='user@example.com')
        char_id = Character.objects.filter(user=user).first().id
        response, is_valid = make_request(request_str=f'/my-character/{char_id}',
                                          schema=CharacterOutSchema,
                                          client=client,
                                          method='patch',
                                          payload=json.dumps(payload),
                                          headers=headers)
        if response.status_code == 200:
            for key, value in payload.items():
                if isinstance(value, bool):
                    assert value is payload[key]
                else:
                    assert value == payload[key]
        assert is_valid is schema_status
        assert response.status_code == expected_status

    @pytest.mark.parametrize("payload,expected_status,schema_status",
                             [
                                 (
                                         {
                                             "email": "user@example.com",
                                         },
                                         400,
                                         False,
                                 ),
                                 (
                                         {
                                             "email": "subscriber@example.com",
                                         },
                                         200,
                                         True,
                                 ),
                                 (
                                         {
                                             "email": "email"
                                         },
                                         422,
                                         False,
                                 ),
                             ]
                             )
    def test_subscribe(self, payload, expected_status,
                       schema_status):
        Subscriber.objects.all().delete()

        response, is_valid = make_request(request_str=f'/subscribe/',
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          payload=json.dumps(payload),
                                          headers=headers)

        assert is_valid is schema_status
        assert response.status_code == expected_status

    def test_subscribe_constraint(self):
        Subscriber.objects.all().delete()

        payload = {
            "email": "subscriber@example.com"
        }
        Subscriber.objects.create(email="subscriber@example.com")
        response, is_valid = make_request(request_str=f'/subscribe/',
                                          schema=MessageOutSchema,
                                          client=client,
                                          method='post',
                                          payload=json.dumps(payload),
                                          headers=headers)
        assert is_valid is False
        assert response.status_code == 409
