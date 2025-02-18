# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: Constants data class
# version: 0.1


class Constants:
    # Common
    SUCCESS = "200"
    FAILURE = "400"

    # Personal Data Management Service
    PORT_PDMS = 5555

    # EVENTS
    EVENT_GET_LABOR_COST = "getLaborCost"
    EVENT_POST_LABOR_DATA = "postLaborData"
    EVENT_GET_LABOR_DATA = "getLaborData"
    EVENT_CUSTOMER_AGE_DATA = "customerAgeData"

    # Andrew's program
    CSV_LABOR_DATA = "../csv/labors_data.csv"
    CSV_HEADER = ['crewName', 'type', 'num', 'wage']

    # Shinji's program
    PORT_CUSTOMER = 30001
    CSV_CUSTOMER_DATA = "../csv/customers_data.csv"
    HEADER_AGE = "Age"