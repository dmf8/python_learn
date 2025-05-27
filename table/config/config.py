import json


class Column:
    def __init__(self):
        self.name: str = ""
        self.condition: str = ""
        self.ordering: str = ""


class Sheet:
    def __init__(self):
        self.file: str = ""
        self.sheet: str = ""
        self.header: int = 0
        self.columns: list[Column] = []

    def columnNames(self) -> str:
        names = []
        for c in self.columns:
            names.append(c.name)
        return names

    def getSortings(self) -> tuple[list[str], list[bool]]:
        names: str = []
        ascendings: bool = []
        for c in self.columns:
            if c.ordering == "^":
                names.append(c.name)
                ascendings.append(True)
            elif c.ordering == "v":
                names.append(c.name)
                ascendings.append(False)
        return names, ascendings


def parseJson(path: str) -> list[Sheet]:
    sheets: list[Sheet] = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                sheets.append(parseSheet(item))
    return sheets


def parseSheet(sheet: dict) -> Sheet:
    s = Sheet()
    if sheet.__contains__("file"):
        s.file = sheet["file"]
    if sheet.__contains__("sheet"):
        s.sheet = sheet["sheet"]
    if sheet.__contains__("header"):
        if isinstance(sheet["header"], int) and sheet["header"] >= 1:
            s.header = sheet["header"]-1
    if sheet.__contains__("columns") and isinstance(sheet["columns"], list):
        s.columns = parseColumns(sheet["columns"])
    return s


def parseColumns(columns: list[dict]) -> list[Column]:
    cols = []
    for col in columns:
        if isinstance(col, dict):
            c = parseColumn(col)
            cols.append(c)
    return cols


def parseColumn(column: dict) -> Column:
    c = Column()
    if column.__contains__("name"):
        c.name = column["name"]
    if column.__contains__("condition"):
        c.condition = column["condition"]
    if column.__contains__("ordering"):
        c.ordering = column["ordering"]
    return c


class Config:
    def __init__(self, path: str):
        self.sheets: list[Sheet] = parseJson(path)

    def output(self):
        print(self.sheets)
