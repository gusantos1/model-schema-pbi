from functions.data import DataModel
from functions.layout import LayoutModel


if __name__ == "__main__":
    # Data Model
    metadata = DataModel("DataModelSchema-pmo")
    relationships = metadata.relationships()
    tables = metadata.tables()
    measures = metadata.measures()
    columns = metadata.columns()

    # Layout Model
    layout = LayoutModel("Layout")
    filters = layout.filters()

    # Write
    pd.DataFrame(relationships).to_json(
        "data/relationships.json", orient="records", indent=4
    )
    pd.DataFrame(tables).to_json("data/tables.json", orient="records", indent=4)
    pd.DataFrame(measures).to_json("data/measures.json", orient="records", indent=4)
    pd.DataFrame(columns).to_json("data/columns.json", orient="records", indent=4)

    pd.DataFrame(filters).to_json("data/filters.json", orient="records", indent=4)
