import os
from locust import HttpUser, between, task
from dotenv import load_dotenv
import random

load_dotenv()


class UserBehavior(HttpUser):
    host = os.getenv('SERVER')

    # Simulated users will wait between 1 and 3 seconds between requests
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post(
            "/login", json={"username": os.getenv('USER'), "password": os.getenv('PW')})
        if response.status_code != 200:
            print(
                f"Login failed with status code: {response.status_code}, content: {response.text}")
            return
        try:
            token = response.json()['access_token']
            self.headers = {"Authorization": f"Bearer {token}"}
        except Exception as e:
            print(
                f"Error decoding JSON: {e}. Response content: {response.text}")

    @task(1)
    def get_all_information(self):
        self.client.get("/information/all", headers=self.headers)

    @task(1)
    def get_thumbnails(self):
        response = self.client.get("/thumbnails", headers=self.headers)
        try:
            thumbnails = response.json()
            for site in thumbnails:
                self.client.get(f"/static/{site['url']}", headers=self.headers)
        except Exception as e:
            print(
                f"Error decoding JSON for thumbnails: {e}. Response content: {response.text}")

    @task(10)
    def get_photo(self):
        response = self.client.get(
            "/images/Andong_GB_Education/2023-08-24", headers=self.headers)
        photos = response.json()
        random_photo = random.choice(photos)
        self.client.get(
            f"/images/Andong_GB_Education/2023-08-24/{random_photo.replace('.jpg','')}", headers=self.headers)

    @task(10)
    def get_video(self):
        response = self.client.get(
            "/video/Andong_GB_Education", headers=self.headers)
        videos = response.json()
        random_video = random.choice(videos)
        self.client.get(
            f"/video/Andong_GB_Education/{random_video}",  headers=self.headers)
