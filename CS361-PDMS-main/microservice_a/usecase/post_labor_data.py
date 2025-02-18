# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: post labor data usecase class
# version: 0.1

import csv
from microservice_a.usecase.base_usecase import BaseUsecase
from microservice_a.constants import Constants

class PostLaborDataUsecase(BaseUsecase):
    def execute(self):
        """
        Function: Execute postLaborData event
        Params: nothing
        Return:
            status(str): status code
        """
        # prepare
        crew_name = self._request_body['crewName']
        labor = self._request_body['labor']

        # write to DB
        try:
            with open(Constants.CSV_LABOR_DATA, "w") as csvfile:
                writer = csv.writer(csvfile)

                # write a header
                writer.writerow(Constants.CSV_HEADER)

                # update DB
                for type, num_wage in labor.items():
                    writer.writerow([crew_name, type, num_wage[0], num_wage[1]])

            status = "200"

        except Exception:
            status = "400"

        return "", status
