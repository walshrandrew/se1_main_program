# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Microservice A
# Due Date:
# Description: get labor cost usecase class
# version: 0.1


from base_usecase import BaseUsecase
from constants import Constants


class GetLaborCostUsecase(BaseUsecase):

    def execute(self):
        """
        Function: Execute getLaborCost event
        Params:
        Return:
            total_labor_cost (int): total labor cost derived from requests
            status(str): status code
        """
        # parse request body
        labors = self._request_body["labor"]
        duration = self._request_body["duration"]

        # calculate the total labor cost
        ttl_cost = 0
        try:
            for workers, wage in labors.values():
                ttl_cost += int(workers) * int(wage)
            ttl_cost *= int(duration)

            status = Constants.SUCCESS
        except Exception:
            status = "400"

        # create a response body
        ttl_cost_dict = {"ttlLaborCost": str(ttl_cost)}

        return ttl_cost_dict, status
