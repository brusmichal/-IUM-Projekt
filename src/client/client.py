from typing import Literal

import requests

from datamodels.models import ServiceInput, ServiceOutput, ServiceOutputAB


class Client:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def get_solution(
        self, endpoint: Literal["ml", "simple", "linear"], input: ServiceInput
    ) -> ServiceOutput:
        url = f"http://{self.host}:{self.port}/{endpoint}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(url=url, headers=headers, json=input)
        return response.json()

    def get_solution_ab(
        self,
        a_method: Literal["ml", "simple", "linear"],
        b_method: Literal["ml", "simple", "linear"],
        input: ServiceInput,
    ) -> ServiceOutputAB:
        url = f"http://{self.host}:{self.port}/ab"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "a-method": a_method,
            "b-method": b_method,
        }
        response = requests.post(url=url, headers=headers, json=input)
        return response.json()
