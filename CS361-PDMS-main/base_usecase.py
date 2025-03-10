# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: Common usecase class
# version: 0.1

class BaseUsecase:
    def __init__(self, request_body):
        self._request_body = request_body
