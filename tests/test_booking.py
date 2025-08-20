import requests
import pytest
import json

from models.booking import CreateBookingResponse
from src.constanst import BookingData
from tests.conftest import booking_client


# BASE_URL = "https://restful-booker.herokuapp.com"


def test_client_booking(created_booking):
    try:
        parsed = CreateBookingResponse(**created_booking)
    except Exception as e:
        raise AssertionError(f"Структура ответа не соответствует данным: {e}")

    assert parsed.booking.bookingdates.checkin == "2026-01-01"

    assert created_booking["booking"]["firstname"] == BookingData.FIRSTNAME.value, (
        "Вернулось не корректное имя\n"
        f"Response:\n{created_booking}\n"
        f"Ожидаемое имя: {BookingData.FIRSTNAME}"
    )
    assert created_booking["booking"]["lastname"] == BookingData.LASTNAME.value, (
        "Вернулась не корректная фамилия\n"
        f"Response:\n{created_booking}\n"
        f"Ожидаемая фамилия: {BookingData.LASTNAME}"
    )


def test_update_booking_with_token(
    booking_client, created_booking, updated_booking_payload, auth_headers
):
    booking_id = created_booking["bookingid"]
    update_response = booking_client.update_booking(
        booking_id, updated_booking_payload.build(), auth_headers
    )
    assert update_response.status_code == 200, "Обновление не удалось"
    get_response = booking_client.get_booking(booking_id)
    updated_data = get_response.json()
    assert updated_data["firstname"] == updated_booking_payload.firstname
    assert updated_data["lastname"] == updated_booking_payload.lastname
    assert updated_data["totalprice"] == updated_booking_payload.totalprice
    assert updated_data["depositpaid"] == updated_booking_payload.depositpaid
    assert (
        updated_data["bookingdates"]["checkin"]
        == updated_booking_payload.bookingdates.checkin
    )
    assert updated_data["additionalneeds"] == updated_booking_payload.additionalneeds


def test_update_booking_without_token(booking_client, created_booking):
    booking_id = created_booking["bookingid"]
    update_data = {"firstname": "ShouldFail"}
    response = booking_client.update_booking(
        booking_id, update_data, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 403, "Ожидалась ошибка доступа"


def test_update_booking_with_invalid_token(booking_client, created_booking):
    booking_id = created_booking["bookingid"]
    invalid_headers = {
        "Content-Type": "application/json",
        "Cookie": "token=invalid_token_here",
    }
    response = booking_client.update_booking(
        booking_id, {"firstname": "Test"}, invalid_headers
    )
    assert response.status_code == 403, "Ожидалась ошибка доступа"


def print_booking(booking, title="Детали бронирования"):
    """Выводит информацию о бронировании в консоль"""
    print(f"\n{'-' * 50}")
    print(f"{title.upper():^50}")
    print(f"{'-' * 50}")
    print(f"ID: {booking.get('bookingid', 'N/A')}")
    print(f"Имя: {booking.get('firstname', 'N/A')}")
    print(f"Фамилия: {booking.get('lastname', 'N/A')}")
    print(f"Цена: {booking.get('totalprice', 'N/A')}")
    print(f"Депозит: {'Да' if booking.get('depositpaid', False) else 'Нет'}")
    dates = booking.get("bookingdates", {})
    print(f"Заезд: {dates.get('checkin', 'N/A')}")
    print(f"Выезд: {dates.get('checkout', 'N/A')}")
    print(f"Дополнительно: {booking.get('additionalneeds', 'Нет')}")
    print(f"{'-' * 50}\n")


def test_create_and_verify_bookings(
    booking_client, valid_booking_payload, headers, auth_headers
):
    """Тест создания и проверки бронирований"""
    firstname = valid_booking_payload.firstname
    print(f"\n=== Начало теста для имени: {firstname} ===")

    initial_response = requests.get(
        f"{booking_client}/booking", params={"firstname": firstname}
    )
    initial_count = (
        len(initial_response.json()) if initial_response.status_code == 200 else 0
    )
    print(f"Начальное количество бронирований: {initial_count}")

    created_ids = []
    for i in range(1, 4):
        response = booking_client.create_booking(valid_booking_payload.build(), headers)
        assert response.status_code == 200, f"Ошибка создания бронирования #{i}"

        booking_data = response.json()
        booking_id = booking_data["bookingid"]
        created_ids.append(booking_id)

        details = booking_client.get_booking(booking_id).json()
        print_booking(details, f"Созданное бронирование #{i}")

    response = requests.get(
        f"{booking_client}/booking", params={"firstname": firstname}
    )
    current_count = len(response.json())
    print(f"\nТекущее количество бронирований: {current_count}")
    print(f"Ожидаемое количество: {initial_count + 3}")

    assert current_count == initial_count + 3, "Неверное количество бронирований"

    print("\nОчистка: удаление тестовых бронирований...")
    for booking_id in created_ids:
        delete_response = booking_client.delete_booking(booking_id, auth_headers)
        assert delete_response.status_code in (
            200,
            201,
            204,
        ), f"Ошибка удаления {booking_id}"
        print(f"Бронирование {booking_id} успешно удалено")


def test_update_with_invalid_token(booking_client, created_booking):
    """Тест обновления с невалидным токеном"""
    booking_id = created_booking["bookingid"]
    print(f"\n=== Тест обновления бронирования {booking_id} с неверным токеном ===")

    current_data = booking_client.get_booking(booking_id).json()
    print_booking(current_data, "Текущие данные")

    invalid_headers = {
        "Content-Type": "application/json",
        "Cookie": "token=invalid_token_here",
    }
    response = booking_client.update_booking(
        booking_id, {"firstname": "InvalidUpdate"}, invalid_headers
    )

    print(f"Результат обновления: статус {response.status_code}")
    assert response.status_code == 403, "Ожидалась ошибка 403"
    print("Тест пройден: доступ запрещен как и ожидалось")
