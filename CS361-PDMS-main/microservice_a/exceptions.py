# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: Exception classes
# version: 0.1

class DbNotFoundException(Exception):
    def __str__(self):
        return (f"[ERROR] Database not found")

class InvalidEventException(Exception):
    def __str__(self):
        return (f"[ERROR] Invalid Event")