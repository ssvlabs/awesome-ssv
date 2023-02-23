import json
from subprocess import check_output
import requests
from collections import namedtuple
import os
import platform

from typing import List

# output = check_output(["./ssv-keys-lin", "key-shares", "-ks",
#                        "/home/rohit/Documents/hackathon-bogota/ssv-service/validator_keys/keystore-m_12381_3600_1_0_0-1665236798.json",
#                        "-ps", "test", "-oid", "1,2,9,42", "-ok",
#                        "LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBMVg2MUFXY001QUNLaGN5MTlUaEIKby9HMWlhN1ByOVUralJ5aWY5ZjAyRG9sd091V2ZLLzdSVUlhOEhEbHBvQlVERDkwRTVQUGdJSy9sTXB4RytXbwpwQ2N5bTBpWk9UT0JzNDE5bEh3TzA4bXFja1JsZEg5WExmbmY2UThqWFR5Ym1yYzdWNmwyNVprcTl4U0owbHR1CndmTnVTSzNCZnFtNkQxOUY0aTVCbmVaSWhjRVJTYlFLWDFxbWNqYnZFL2cyQko4TzhaZUgrd0RzTHJiNnZXQVIKY3BYWG1uelE3Vlp6ZklHTGVLVU1CTTh6SW0rcXI4RGZ4SEhSeVU1QTE3cFU4cy9MNUp5RXE1RGJjc2Q2dHlnbQp5UE9BYUNzWldVREI3UGhLOHpUWU9WYi9MM1lnSTU4bjFXek5IM0s5cmFreUppTmUxTE9GVVZzQTFDUnhtQ2YzCmlRSURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K,LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBeUtVWTVEUmZZREljengzcjhVY0UKTlpFMFdIQXFuV2FIRjZYRlUydVdObjVOVE94Zkt4ZmZaLzkyeVE1citQVkJPRmQrcHhILzI2QXJVT3dNL1lBRQpRbDZ0VzBtc1FqdUtIU1Q4aUtvTDRTNUt0aDNoeTBqeFRHR1ZZaWdjWG1vRURjd2YxaG8wdWRxRmlEN3dFWXN1CmZHa2E2U1ZQNnBab1NMaU9HZFRKUWVzVDI5WEVCdDZnblhMaFB1MER2K0xsQUJJQ1pqWEFTZWtpSFVKUHRjYlgKRjZFL0lScGpkWHVNSmUyOXZDcmZudXhWWk93a1ptdzJXdGljYlNDOVJpSFRYWUQ1dnVGakZXRHNZMERHUDhzOAoyc1haVHdsNWl4dEhlUWM2N1lLRFN6YU1MNnY1VUVZblhUTzZzNHFVSWVnTXJwZjd3S0xGVWxqRTMwbnNIaVBUCjBRSURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K,LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBelc5VGNJMWxXbmUydkNqZzJlb2UKY3o3NnZ4OVU2QWgvTnZRT0dJY1JTbk5mUWc1amxjM0JuTUM4eW1pQTQzVHJDejl6UFVhUVozZG5idW9DZEY3awpoOWZKcVd3SFFrU2pFQ1ZtVytQS2FVWmQ4aW42cGVGbmgrZEowenR1cUx1aUlJMWQvU05xdGJUaFA2VjQ4TGxDCklsVUhXVFRaKzNVY2dBanlwenIxRmxYU2hGV0w0aGcxeXF3K0p1WW1yTnY2cGZaeWdVbTZQaTBVazVXUVZnUk4KR2RrU3BTb2ZYZERGcElWN0xBU3V0a2dGUytqVnpaL3E5bmh1ejVjNlJWaDYvV1hiZVpDbXhnMGU2R2hIVXY0bAp4SGNaSUkraWhzWk5KM3V5b2NiaWlubE5EaTNMK2hySEUxMExNeVRoN2lVSC8yd1k4MjJKMmdDSEZzNWhkVkNrCm53SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K,LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBNVV3SFltUnJoL3hwbWovd1RHcWwKLysvZEdNWFFlSkg0VUptSjNNWXhyMUU0aGF4ZkhLK3NzSkhXYzYvbWlpRTdZMTBxcy9sNzRvNHdGNnJ2SXYrVApTYnQ2UjdONXNKYUZsYnZ3M2ZCampiZElQTnBHQ0JTaXl3aTc3M3lQZy8vOG04OHMxNTNwYjZmVnViU2QxMzJWClpEZkhmMEdPdnA4b0hxcHY5ampsQ0NlV2phNXUzVzhqN2RwWDBsQTYvaTJRaW4yN3VESHViMHd1eWFEcGprNDcKWG1tOHV2d1VFTWw1L0trREg3Z2FXUjNzNkluZjR4TVpKbHEvMGplVkdoUll5bHg3RFE1WnVBNDNCSGNGMWtxMAo3ZHU0ejFUQ2tFN0ZIZlZRMTdFUnpwUHlmS2l5YlQ4UXdnb3VVV2hGUjJqK3ExbHZGbHJQR0U2OWpIWE9MVWM0CnV3SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K",
#                        "-ssv", "1000"])
# print(str(output).partition("key shares file at ")[2].partition(".json")[0] + ".json")

Operator = namedtuple("Operator", "id pubkey fee name")


class OperatorData:
    API_URL = None
    operator_call = "/api/v1/operators/"

    def __init__(self, api_url):
        """

        :param api_url:
        """
        self.API_URL = api_url

    def make_call(self, url):
        for tries in range(3):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.raise_for_status()
            if tries == 2:
                response.raise_for_status()

    def get_operator_data(self, ids: List[int]):
        operators_data = []
        for id in ids:
            operator_url_id = self.API_URL + self.operator_call + str(id)
            operator_data = self.make_call(operator_url_id)
            operator = Operator(operator_data["id"], operator_data["public_key"], operator_data["fee"],
                                operator_data["name"])
            operators_data.append(operator)
        # print("operator_data")
        # print(operator_data)
        return operators_data


class SSV:
    CLI_PATH_LINUX_MAC = os.getcwd() + "/ssv/ssv-cli"
    CLI_PATH_WIN = os.getcwd() + "/ssv/ssv-cli.exe"
    ssv_share_file = None
    keystore_file = None
    keystore_pass = None

    def __init__(self, keystore_file, keystore_password):
        """

        :param keystore_folder:
        """
        self.keystore_file = keystore_file
        self.keystore_pass = keystore_password

    def generate_shares(self, operator_data: List[Operator], network_fees):
        """

        :return:
        """
        print("===================================================================================")
        operator_ids = [str(operator.id) for operator in operator_data]
        operator_pubkeys = [operator.pubkey for operator in operator_data]
        total_ssv_fee = (sum([operator.fee for operator in operator_data]) + network_fees) * 2628000
        output_folder = os.getcwd() + "/keyshares"
        cli_path = self.CLI_PATH_LINUX_MAC if 'Linux' in platform.system() or 'Darwin' in platform.system() else self.CLI_PATH_WIN
        # output2=check_output(["ls","-la"])
        # print(output2)
        output = check_output(
            [cli_path, "key-shares", "-ks", self.keystore_file, "-ps", self.keystore_pass, "-oid",
               ",".join(operator_ids), "-ok", ",".join(operator_pubkeys), "-ssv", str(total_ssv_fee), "-of",
               output_folder])
        print(output)
        return output_folder + output.decode("utf-8").partition("keyshares")[2].partition(".json")[0] + ".json"

    def get_keyshare(self, share_file_path):
        """

        :return:
        """
        print(share_file_path)
        with open(share_file_path, "r") as file_path:
            print(file_path)
            shares = json.load(file_path)
        file_path.close()
        return shares["payload"]["readable"]


if __name__ == '__main__':
    ssv = SSV(
        "/home/rohit/Documents/hackathon-bogota/ssv-service/validator_keys/keystore-m_12381_3600_1_0_0-1665252210.json",
        "test")
    op = OperatorData("https://api.ssv.network")
    operators = op.get_operator_data([1, 2, 192, 42])
    share_file = str(ssv.generate_shares(operators, 1200084048))
    ssv.get_keyshare(share_file)
