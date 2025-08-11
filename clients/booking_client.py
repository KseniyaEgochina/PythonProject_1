import requests


class BookingClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_booking(self,data: dict, headers: dict) -> requests.Response:
        return requests.post(url=f"{self.base_url}/booking", json=data,headers=headers )

    def delete_booking(self,booking_id: int, headers: dict) -> requests.Response:
        return requests.delete(f"{self.base_url}/booking/{str(booking_id)}",headers=headers)



    def get_booking(self, booking_id):
        return requests.get(f"{self.base_url}/booking/{booking_id}")

    def update_booking(self, booking_id, data, headers):
        return requests.put(
            f"{self.base_url}/booking/{booking_id}",
            json=data,
            headers=headers
        )
