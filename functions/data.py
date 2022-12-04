import json
import re
import pandas as pd
import numpy as np
from typing import List


class DataModel:
    def __init__(self, directory: str):
        self.__model = self.__read_model(directory)
        self.__tables = self.__no_hidden(self.__model["tables"])

    def relationships(self):
        return self.__relationship_formatter(self.__model["relationships"])

    def tables(self):
        return self.__tables_formatter(self.__tables)

    def measures(self):
        return self.__measures_formatter(self.__tables)

    def columns(self):
        return self.__columns_formatter(self.__tables)

    @staticmethod
    def __columns_formatter(df: pd.DataFrame) -> List[dict]:
        """
        ...
        """
        data = df[["name", "columns"]].to_dict(orient="records")
        columns = []

        for item in data:
            if len(item["columns"]) > 1:
                for col in item["columns"][1:]:
                    name = col["name"]
                    dtype = col["dataType"]
                    table = item["name"]
                    row = {
                        "column": name,
                        "type": dtype,
                        "table": table,
                    }
                    columns.append(row)
        return columns

    @staticmethod
    def __measures_formatter(df: pd.DataFrame) -> List[dict]:
        """
        ...
        """
        df = df.replace({np.nan: None})
        data = df[["name", "measures"]].to_dict(orient="records")
        measures = []

        for item in data:
            if item["measures"]:
                for measure in item["measures"]:
                    name = measure["name"]
                    expression = measure["expression"]
                    dtype = measure["dataType"]
                    table = item["name"]
                    row = {
                        "measure": name,
                        "expression": expression,
                        "type": dtype,
                        "table": table,
                    }
                    measures.append(row)
        return measures

    @staticmethod
    def __relationship_formatter(data: List[dict]) -> List[dict]:
        """
        ...
        """
        df = pd.DataFrame(data)
        df = df[["fromTable", "fromColumn", "toTable", "toColumn"]]
        return df.to_dict(orient="records")

    @staticmethod
    def __tables_formatter(df: pd.DataFrame) -> List[dict]:
        """
        ...
        """
        df = df[["name", "partitions"]]
        data = df.to_dict(orient="records")

        for item in data:
            item["mode"] = item["partitions"][0]["mode"]
            item["source"] = item["partitions"][0]["source"]["expression"]
            item["source_items"] = re.split(
                f"\\n",
                item["partitions"][0]["source"]["expression"].replace("    ", ""),
            )
            del item["partitions"]
        return data

    @staticmethod
    def __no_hidden(data: List[dict]) -> pd.DataFrame:
        """
        ...
        """
        df_raw = pd.DataFrame(data)
        if "isHidden" in df_raw:
            df = df_raw.loc[df_raw["isHidden"] != True]
            df = df.drop(columns=["isHidden"])
            return df
        return df_raw

    @staticmethod
    def __read_model(directory: str) -> List[dict]:
        """
        ...
        """
        with open(directory, "rb") as file:
            data = json.load(file)
            return data["model"]
