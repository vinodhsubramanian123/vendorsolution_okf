import time
from locust import HttpUser, task, between

class IKPPlatformUser(HttpUser):
    # Simulate users waiting between 1 to 5 seconds between tasks
    wait_time = between(1, 5)
    
    @task(3)
    def check_health(self):
        """Simulate frequent simple health checks."""
        self.client.get("/api/v1/health")

    @task(1)
    def generate_boq(self):
        """Simulate less frequent but heavy BOQ generation requests."""
        payload = {
            "query": "I need a high performance AI server with 8 GPUs for deep learning",
            "vendor_preference": "hpe",
            "include_alternatives": False
        }
        
        with self.client.post("/api/v1/boq/generate", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                # Basic check to see if the workflow succeeded
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure(f"Workflow failed: {data.get('message', 'Unknown error')}")
            else:
                response.failure(f"HTTP Status {response.status_code}: {response.text}")
