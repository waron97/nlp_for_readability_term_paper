import json
import requests
import dpath

from ..util import dget
from ..constants import OPEANAI_API_KEY


class GPT3():
    def __init__(self) -> None:
        self.token = OPEANAI_API_KEY
        self._base_url = "https://api.openai.com/v1"

    def __make_request(self, body={}, endpoint: str = "", method: str = "GET"):
        url = f"{self._base_url}/{endpoint}"
        b = json.dumps(body)
        response = requests.request(
            method,
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            data=b if method == "POST" else None
        ).content

        loaded = json.loads(response)
        return dget(loaded, "choices/0/text")

    def list_models(self):
        response = self.__make_request(endpoint="models")
        return response

    def complete(
        self,
        prompt,
        model: str = "text-davinci-003",
        max_tokens: int = 3000,
        temperature: float = 0.9,
        top_p: float = 1,
        n: int = 1
    ):
        body = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n
        }

        return self.__make_request(body=body, endpoint="completions", method="POST")
