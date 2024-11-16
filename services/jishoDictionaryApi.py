import os
import sys
from typing import Dict, Union

import requests
from dotenv import load_dotenv

load_dotenv()


class JishoService:
    def __init__(self):
        self.base_url = os.getenv("JISHO_URL")

    def getWordMeaning(self, word: str) -> Dict[str, Union[bool, str, Dict[str, any]]]:
        url = f"{self.base_url}?keyword={word}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                res = response.json()
                # Check if there are results
                if res["data"]:
                    data = res["data"][0]
                    japanese_reading = (
                        data["japanese"][0]["reading"]
                        if data["japanese"][0]["reading"]
                        else ""
                    )
                    meaning = (
                        data["senses"][0]["english_definitions"]
                        if data["senses"][0]["english_definitions"]
                        else ""
                    )
                    return {
                        "success": True,
                        "message": "Data Found",
                        "data": {
                            "meaning": meaning,
                            "japanese_reading": japanese_reading,
                        },
                    }
                else:
                    print("No Data Found")
                    return {"success": True, "message": "No Data Found", "data": {}}
            else:
                print("Unable to Fetch Data")
                return {"success": False, "message": "Unable to Fetch Data", "data": {}}
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"jisho: {str(e)} as line {line_number}")
            return {"success": False, "message": str(e), "data": {}}


# js = JishoService()
# print(js.getWordMeaning("車"))
