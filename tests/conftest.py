import pytest
import requests

from clients.booking_client import BookingClient
from models.booking import BookingDates, Booking
from src.constanst import BookingData
from src.setings import settings


@pytest.fixture
def booking_client():
    return BookingClient(base_url=settings.base_url)


@pytest.fixture
def valid_booking_payload():
    return Booking (
        firstname=BookingData.FIRSTNAME.value,
        lastname= BookingData.LASTNAME.value,
        totalprice=1000,
        depositpaid=True,
        bookingdates=BookingDates(
            checkin="2026-01-01",
            checkout="2026-01-01"
        ),
        additionalneeds="Breakfast"
    )


@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

@pytest.fixture
def created_booking(booking_client,valid_booking_payload,headers):
    response = booking_client.create_booking(valid_booking_payload.build(),headers)
    data = response.json()
    yield data
    booking_client.delete_booking(data['bookingid'],headers)

@pytest.fixture
def updated_booking_payload():
    return Booking(
        firstname="UpdatedFirstName",
        lastname="UpdatedLastName",
        totalprice=2000,
        depositpaid=False,
        bookingdates=BookingDates(
            checkin="2026-02-01",
            checkout="2026-02-10"
        ),
        additionalneeds="Dinner"
    )

@pytest.fixture
def auth_headers(auth_data):
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_data}"
    }

@pytest.fixture
def auth_data ():
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{settings.base_url}/auth", json=auth_data)
    assert response.status_code == 200, "Не удалось получить токен"
    return response.json()["token"]



