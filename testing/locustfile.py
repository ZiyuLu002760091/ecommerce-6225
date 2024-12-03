from locust import HttpUser, task, between
import json

class CheckoutUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between requests (1 to 5 seconds)

    @task
    def create_checkout(self):
        """Simulate POST requests to the /checkouts endpoint."""
        url = "/checkouts"
        payload = {
            "customer": "8326f541-3fd7-41f3-9d38-9bb653f16fbe",
            "address": "7a67b21b-67c7-4521-baae-a0274ce47287",
            "card_hash": "493132_Vm3n79hw1seWbo4Bj4o44FYB6aWxuAFqzgprd9CyqkqAbgCK7aRe33mseDU+pGYbcpBxIYD53l4J7rzmuLAQ1tadu5l941OvgazZUXYdAvkCCm+Tu33DevwUwkuEQa3/E7WeFSkdX8vYAKYmXMKOKlPDPN3CI1dHYQoVr3A/Ou/M2g01BMdYvVzNI86u2ps6C2A0pz06tdUs2/ZXiNR0XKyP5Kf1qk3dPArmRzix3mvJWyBAqLGcr6Yw5YUv2CvYTe4oGi/z/uNHATOElxDEHIw8pHR6DcOsppZjh3gH61kp2JZ8EHGUH/CKFia6jcwu7LahwBJOz6Uj5oC0fiWcig==",
            "installments": 1,
            "items": [
                {
                    "product": "e1222349-d1b0-4195-11bf-6523197605ab",
                    "quantity": 1,
                    "price": 220
                }
            ],
            "payment_method": "e0282812-d1b0-4585-99bf-6510497602ab",
            "status": "e1182812-d1b0-4585-99bf-6510497602ab"
        }

        # Add Authorization header
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMjU4NjIwLCJpYXQiOjE3MzMxNzIyMjAsImp0aSI6IjdjYzIyMDFiZjUxMTQ1OGZiMDJkNWFjZjQzZWEzYjJkIiwidXNlcl9pZCI6IjgzMjZmNTQxLTNmZDctNDFmMy05ZDM4LTliYjY1M2YxNmZiZSJ9.N2Xy2Fneg1UV5w-bBu64v7LgxVKuI9JefIza2UhmTTc"
        }

        # Send POST request with authorization
        response = self.client.post(url, data=json.dumps(payload), headers=headers)

        # Validate response status
        if response.status_code != 201:
            print(f"Failed! Status Code: {response.status_code}, Response: {response.text}")
