# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: customer age data usecase class
# version: 0.1

import csv
from microservice_a.usecase.base_usecase import BaseUsecase
from microservice_a.constants import Constants
from microservice_a.exceptions import DbNotFoundException

class CustomerAgeDataUsecase(BaseUsecase):
    def execute(self):
        """
        Function: Execute customerAgeData event
        Params: nothing
        Return:
            customer_age_dict (dict): dict containing the list of age
            status(str): status code
        """
        # get data from database and get age data
        try:
            age_list = []
            with open(Constants.CSV_CUSTOMER_DATA, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    age_list.append(row[Constants.HEADER_AGE])

            # create a response body
            customer_age_dict = {"customerAge": age_list}
            status = Constants.SUCCESS
        except DbNotFoundException as e:
            print(e)
            status = Constants.FAILURE

        return customer_age_dict, status