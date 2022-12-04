import json
from typing import List


class LayoutModel:
    def __init__(self, directory: str):
        self.__layout = self.__read_layout(directory)

    def __read_layout(self, directory: str) -> List[dict]:
        """..."""
        with open(directory, "rb") as file:
            data = json.load(file)
            return data["sections"]

    def filters(self) -> List[dict]:
        """..."""
        data = []
        for section in self.__layout:
            for visual in section["visualContainers"]:
                page = section["displayName"]
                filters = self.__filter_formatter(section["filters"])
                cfg = json.loads(visual["config"])
                if "singleVisual" in cfg and "vcObjects" in cfg["singleVisual"]:
                    prop = cfg["singleVisual"]["vcObjects"]
                    title = (
                        prop["title"][0]["properties"]["text"]["expr"]["Literal"][
                            "Value"
                        ].replace("'", "")
                        if (
                            "title" in prop and "text" in prop["title"][0]["properties"]
                        )
                        else None
                    )
                    visualType = cfg["singleVisual"]["visualType"]
                    if "prototypeQuery" in cfg["singleVisual"]:
                        select = cfg["singleVisual"]["prototypeQuery"]["Select"]
                        sources = [
                            {
                                "name": item["Name"].split(".")[1],
                                "table": item["Name"].split(".")[
                                    0
                                ],  # não ta batendo com table
                                "type": "Measure" if "Measure" in item else "Column",
                            }
                            for item in select
                        ]
                        response = {
                            "page": page,
                            "title": title,
                            "visual_type": visualType,
                            "source": sources,
                            "filter": filters,
                        }
                        data.append(response)
        return data

    @staticmethod
    def __filter_formatter(filters):
        """
        ...
        """
        data = []
        for item in json.loads(filters):
            if "filter" in item:
                condition = item["filter"]["Where"][0]["Condition"]
                table = item["filter"]["From"][0]["Entity"]

                if condition.get("In"):
                    table_column = (
                        table
                        + "."
                        + condition["In"]["Expressions"][0]["Column"]["Property"]
                    )
                    filter_value = condition["In"]["Values"][0][0]["Literal"][
                        "Value"
                    ].replace("'", "")
                    result = {table_column: filter_value}
                else:
                    operator = list(condition.keys())[0]
                    table_column = (
                        table
                        + "."
                        + condition[operator]["Expression"]["In"]["Expressions"][0][
                            "Column"
                        ]["Property"]
                    )
                data.append(result)
        return json.dumps(data, ensure_ascii=False)
