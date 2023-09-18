import decimal, pathlib
import sqlite3, openpyxl
import pandas as pd
from utils.units import convertToBaseUnits, convertToPrefix
import create_database

COLUMNS = ["lcsc", "description", "value", "package", "manufacturer", "voltage"]


def getUnitValue(input_string, unit, force_unit=False):
    input_string = input_string.split(" ")
    for i in range(len(input_string)):
        if input_string[i].endswith(unit):
            input_string[i] = input_string[i][:-1]
        else:
            if force_unit:
                continue
        try:
            return convertToBaseUnits(input_string[i])
        except ValueError:
            pass
        except decimal.InvalidOperation:
            pass
    return None


class ValueInvalid(Exception):
    pass


class PackageInvalid(Exception):
    pass


class JLCPCBDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def status(self):
        # check if the database exists
        try:
            open(self.db_path, "r")
        except FileNotFoundError:
            return False
        # check date created of the database file
        created = pathlib.Path(self.db_path).stat().st_ctime

        return created

    def update(self):
        create_database.download_files()
        create_database.create_database()

    def open(self):
        if not self.status():
            raise FileNotFoundError("Database not found")
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()
        self.tables = self.get_tables()

        self.manufacturers = pd.read_sql_query("SELECT * from manufacturers", self.db)
        self.categories = pd.read_sql_query("SELECT * from categories", self.db)
        self.basic = pd.read_sql_query("SELECT * from components WHERE basic = 1", self.db)
        self.basic = pd.merge(self.basic, self.manufacturers, left_on='manufacturer_id', right_on='id')
        self.basic = pd.merge(self.basic, self.categories, left_on='category_id', right_on='id')
        self.basic = self.basic.rename(columns={'name': 'manufacturer'})

        resistor_id = self.categories[self.categories['category'] == 'Resistors']['id'].values[0]
        capacitor_id = self.categories[self.categories['subcategory'] == 'Multilayer Ceramic Capacitors MLCC - SMD/SMT']['id'].values[0]
        self.resistors = self.basic[self.basic['category_id'] == resistor_id]
        self.capacitors = self.basic[self.basic['category_id'] == capacitor_id]

        self.resistors['value'] = self.resistors['description'].apply(getUnitValue, unit="Ω", force_unit=True)
        # add empty voltage column
        self.resistors['voltage'] = ""
        # remove all other columns except value and package
        self.resistors = self.resistors[COLUMNS]
        self.capacitors['value'] = self.capacitors['description'].apply(getUnitValue, unit="F", force_unit=True)
        self.capacitors['voltage'] = self.capacitors['description'].apply(getUnitValue, unit="V", force_unit=True)
        # remove all other columns except value and package
        self.capacitors = self.capacitors[COLUMNS]

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

    def get_table_columns(self, table_name):
        self.cursor.execute("PRAGMA table_info({})".format(table_name))
        return self.cursor.fetchall()

    def get_resistors(self, value, package):
        df = self.resistors.copy()
        if value != "":
            value = getUnitValue(value, "Ω")
            df = self.resistors[self.resistors['value'] == value]
        if value is None:
            raise ValueInvalid("Value is Invalid")
        if len(df) == 0:
            # find the closest values
            df = self.resistors.copy()
            df['diff'] = df['value'].apply(lambda x: abs(x - value) if x is not None else None)
            df = df.sort_values(by=['diff'])
            df = df.head(10)
        if package != "":
            # check if the package is found in the description
            df = df[df['description'].str.contains(package)]
        if len(df) == 0:
            raise PackageInvalid("Package is Invalid")

        df.loc[:, 'value'] = df['value'].apply(convertToPrefix, unit="Ω")
        # convert to list of dicts
        return df

    def get_capacitors(self, value: str, package: str):
        # if value is empty return all capacitors
        df = self.capacitors.copy()
        if value != "":
            value = getUnitValue(value, "F")
            df = self.capacitors[self.capacitors['value'] == value]
        if value is None:
            raise ValueInvalid("Value is Invalid")
        if len(df) == 0:
            # find the closest values
            df = self.capacitors.copy()
            df['diff'] = df['value'].apply(lambda x: abs(x - value) if x is not None else None)
            df = df.sort_values(by=['diff'])
            df = df.head(10)
        if package != "":
            # check if the package is found in the description
            df = df[df['description'].str.contains(package)]
        if len(df) == 0:
            raise PackageInvalid("Package is Invalid")

        df.loc[:, 'value'] = df['value'].apply(convertToPrefix, unit="F")
        df.loc[:, 'voltage'] = df['voltage'].apply(convertToPrefix, unit="V")
        # convert to list of dicts
        return df

    def get_basic(self):
        return self.basic

    def save_to_excel(self, filename):
        self.basic.to_excel(filename)

