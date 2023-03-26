import json
import os

import requests


class DALL_E:
    def __init__(self) -> None:
        self.token = os.environ.get('OPENAI_API_KEY')

    def generate(self, prompt: str):
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            },
            data=json.dumps({
                "prompt": prompt,
                "response_format": "url"
            })
        )

        return json.loads(response.content)
