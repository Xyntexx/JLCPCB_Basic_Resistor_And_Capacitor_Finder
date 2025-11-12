import decimal, pathlib
import sqlite3
import json
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
        if hasattr(self, 'db'):
            self.db.close()
        create_database.download_files()
        create_database.create_database()
        #update the database updated time
        self.optimize()
        self.open()

    def open(self):
        if not self.status():
            raise FileNotFoundError("Database not found")
        self.db = sqlite3.connect(self.db_path)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.tables = self.get_tables()

        # Get category IDs for resistors and capacitors
        self.cursor.execute("SELECT id FROM categories WHERE category = 'Resistors' LIMIT 1")
        result = self.cursor.fetchone()
        self.resistor_category_ids = [result[0]] if result else []

        # Get all resistor category IDs (there are multiple subcategories)
        self.cursor.execute("SELECT id FROM categories WHERE category = 'Resistors'")
        self.resistor_category_ids = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT id FROM categories WHERE subcategory = 'Multilayer Ceramic Capacitors MLCC - SMD/SMT'")
        result = self.cursor.fetchone()
        self.capacitor_category_id = result[0] if result else None

    def optimize(self):
        print("Optimizing database")
        if not self.status():
            raise FileNotFoundError("Database not found")
        db = sqlite3.connect(self.db_path)
        # delete everything except basic components
        db.execute("DELETE FROM components WHERE basic = 0")
        db.commit()
        db.close()
        print("Database optimized")

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

    def get_table_columns(self, table_name):
        self.cursor.execute("PRAGMA table_info({})".format(table_name))
        return self.cursor.fetchall()

    def get_resistors(self, value, package):
        """Get resistors matching value and package. Returns list of dicts."""
        target_value = None

        if value != "":
            target_value = getUnitValue(value, "Ω")
            if target_value is None:
                raise ValueInvalid("Value is Invalid")

        # Build query
        category_placeholders = ','.join(['?'] * len(self.resistor_category_ids))

        if target_value is not None:
            # Search for exact or close values
            query = f"""
            SELECT c.lcsc, c.description, c.package, m.name as manufacturer, c.stock, c.extra
            FROM components c
            JOIN manufacturers m ON c.manufacturer_id = m.id
            WHERE c.category_id IN ({category_placeholders})
            AND c.basic = 1
            """
            params = list(self.resistor_category_ids)

            if package:
                query += " AND c.package LIKE ?"
                params.append(f"%{package}%")

            query += " ORDER BY c.stock DESC LIMIT 100"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            # Parse values and find closest matches
            results = []
            for row in rows:
                # Extract description from extra JSON field
                description = row['description']
                if not description and row['extra']:
                    try:
                        extra_data = json.loads(row['extra'])
                        description = extra_data.get('description', '')
                    except (json.JSONDecodeError, TypeError):
                        description = ''

                parsed_value = getUnitValue(description, "Ω", force_unit=True)
                if parsed_value is not None:
                    results.append({
                        'lcsc': str(row['lcsc']),
                        'description': description,
                        'package': row['package'],
                        'manufacturer': row['manufacturer'],
                        'voltage': "",
                        'value': parsed_value,
                        'diff': abs(parsed_value - target_value)
                    })

            # Sort by difference and take top 10
            results.sort(key=lambda x: x['diff'])
            results = results[:10]

            if not results:
                raise ValueInvalid("Value is Invalid")

            # Convert values to prefix notation
            for r in results:
                r['value'] = convertToPrefix(r['value'], unit="Ω")
                del r['diff']

            return results
        else:
            # No value specified, return all resistors
            query = f"""
            SELECT c.lcsc, c.description, c.package, m.name as manufacturer, c.extra
            FROM components c
            JOIN manufacturers m ON c.manufacturer_id = m.id
            WHERE c.category_id IN ({category_placeholders})
            AND c.basic = 1
            """
            params = list(self.resistor_category_ids)

            if package:
                query += " AND c.package LIKE ?"
                params.append(f"%{package}%")

            query += " ORDER BY c.stock DESC LIMIT 100"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            if not rows:
                raise PackageInvalid("Package is Invalid")

            results = []
            for row in rows:
                # Extract description from extra JSON field
                description = row['description']
                if not description and row['extra']:
                    try:
                        extra_data = json.loads(row['extra'])
                        description = extra_data.get('description', '')
                    except (json.JSONDecodeError, TypeError):
                        description = ''

                parsed_value = getUnitValue(description, "Ω", force_unit=True)
                results.append({
                    'lcsc': str(row['lcsc']),
                    'description': description,
                    'package': row['package'],
                    'manufacturer': row['manufacturer'],
                    'voltage': "",
                    'value': convertToPrefix(parsed_value, unit="Ω") if parsed_value else ""
                })

            return results[:10]

    def get_capacitors(self, value: str, package: str):
        """Get capacitors matching value, voltage and package. Returns list of dicts."""
        target_value = None

        if value != "":
            target_value = getUnitValue(value, "F")
            if target_value is None:
                raise ValueInvalid("Value is Invalid")

        # Build query
        if target_value is not None:
            # Search for exact or close values
            query = """
            SELECT c.lcsc, c.description, c.package, m.name as manufacturer, c.stock, c.extra
            FROM components c
            JOIN manufacturers m ON c.manufacturer_id = m.id
            WHERE c.category_id = ?
            AND c.basic = 1
            """
            params = [self.capacitor_category_id]

            if package:
                query += " AND c.package LIKE ?"
                params.append(f"%{package}%")

            query += " ORDER BY c.stock DESC LIMIT 100"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            # Parse values and find closest matches
            results = []
            for row in rows:
                # Extract description from extra JSON field
                description = row['description']
                if not description and row['extra']:
                    try:
                        extra_data = json.loads(row['extra'])
                        description = extra_data.get('description', '')
                    except (json.JSONDecodeError, TypeError):
                        description = ''

                parsed_value = getUnitValue(description, "F", force_unit=True)
                parsed_voltage = getUnitValue(description, "V", force_unit=True)
                if parsed_value is not None:
                    results.append({
                        'lcsc': str(row['lcsc']),
                        'description': description,
                        'package': row['package'],
                        'manufacturer': row['manufacturer'],
                        'voltage': parsed_voltage,
                        'value': parsed_value,
                        'diff': abs(parsed_value - target_value)
                    })

            # Sort by difference and take top 10
            results.sort(key=lambda x: x['diff'])
            results = results[:10]

            if not results:
                raise ValueInvalid("Value is Invalid")

            # Convert values to prefix notation
            for r in results:
                r['value'] = convertToPrefix(r['value'], unit="F")
                r['voltage'] = convertToPrefix(r['voltage'], unit="V")
                del r['diff']

            return results
        else:
            # No value specified, return all capacitors
            query = """
            SELECT c.lcsc, c.description, c.package, m.name as manufacturer, c.extra
            FROM components c
            JOIN manufacturers m ON c.manufacturer_id = m.id
            WHERE c.category_id = ?
            AND c.basic = 1
            """
            params = [self.capacitor_category_id]

            if package:
                query += " AND c.package LIKE ?"
                params.append(f"%{package}%")

            query += " ORDER BY c.stock DESC LIMIT 100"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            if not rows:
                raise PackageInvalid("Package is Invalid")

            results = []
            for row in rows:
                # Extract description from extra JSON field
                description = row['description']
                if not description and row['extra']:
                    try:
                        extra_data = json.loads(row['extra'])
                        description = extra_data.get('description', '')
                    except (json.JSONDecodeError, TypeError):
                        description = ''

                parsed_value = getUnitValue(description, "F", force_unit=True)
                parsed_voltage = getUnitValue(description, "V", force_unit=True)
                results.append({
                    'lcsc': str(row['lcsc']),
                    'description': description,
                    'package': row['package'],
                    'manufacturer': row['manufacturer'],
                    'voltage': convertToPrefix(parsed_voltage, unit="V") if parsed_voltage else "",
                    'value': convertToPrefix(parsed_value, unit="F") if parsed_value else ""
                })

            return results[:10]
