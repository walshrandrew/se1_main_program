# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: getlabor data usecase class
# version: 0.1

import csv
from microservice_a.usecase.base_usecase import BaseUsecase
from microservice_a.constants import Constants

class GetLaborDataUsecase(BaseUsecase):
    def execute(self):
        """
        Function: Execute getLaborData event
        Params: nothing
        Return:
            body(dict): response body
            status(str): status code
        """
        # prepare
        crew_name = self._request_body["crewName"]
        labor = {}

        # get labor data with the specified crew name
        try:
            with open(Constants.CSV_LABOR_DATA, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) # skip a header

                for row in reader:
                    if row[0] == crew_name:
                        labor[row[1]] = [row[2], row[3]]

            status = "200"

        except Exception:
            status = "400"

        return {"labor":labor}, status