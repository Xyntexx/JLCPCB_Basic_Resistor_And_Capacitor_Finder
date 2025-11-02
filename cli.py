import json
import sys
import argparse
from utils.db import JLCPCBDatabase
from create_symbol import createResistorSymbol, createCapacitorSymbolSmall, createCapacitorSymbol, createResistorSymbolSmall


def process_components(input_file, output_file, use_small_symbols=True):
    """
    Process a list of components from a JSON file and generate KiCad symbol output.

    Args:
        input_file: Path to JSON file containing component list
        output_file: Path to output file for generated symbols
        use_small_symbols: Whether to use small symbol footprints (default: True)
    """
    # Initialize database
    db = JLCPCBDatabase("cache.sqlite3")

    if not db.status():
        print("Error: Database not found. Please update the database first using the GUI.")
        return False

    db.open()

    # Load components from JSON file
    try:
        with open(input_file, 'r') as f:
            components = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{input_file}': {e}")
        return False

    # Process each component
    results = []
    errors = []

    # Position tracking for spacing symbols in grid
    x_pos = 50
    y_pos = 50
    x_spacing = 25  # Horizontal spacing between symbols
    y_spacing = 15  # Vertical spacing between rows
    symbols_per_row = 5  # Number of symbols per row
    symbol_count = 0

    for idx, component in enumerate(components):
        comp_type = component.get('type', '').lower()
        value = component.get('value', '')
        package = component.get('package', '')
        ref_list = component.get('ref', f'Unknown{idx}')

        # Split multiple references (e.g., "C1,C2" -> ["C1", "C2"])
        refs = [r.strip() for r in ref_list.split(',')]

        print(f"Processing {ref_list}: {value} {package} ({comp_type})")

        try:
            if comp_type == 'capacitor':
                voltage = component.get('voltage', '')
                # Search for component in database
                df = db.get_capacitors(value, package)

                if len(df) == 0:
                    errors.append(f"{ref_list}: No matching capacitor found for {value} {package}")
                    continue

                # Use the first match (best match)
                row = df.iloc[0]
                lcsc = row['lcsc']
                found_value = row['value']
                found_package = row['package']
                found_voltage = row['voltage']

                # Generate a separate symbol for each reference designator
                for ref in refs:
                    # Calculate position for this symbol
                    current_x = x_pos + (symbol_count % symbols_per_row) * x_spacing
                    current_y = y_pos + (symbol_count // symbols_per_row) * y_spacing

                    # Generate symbol with position and reference
                    if use_small_symbols:
                        symbol = createCapacitorSymbolSmall(found_value, found_package, lcsc, found_voltage, current_x, current_y, ref)
                    else:
                        symbol = createCapacitorSymbol(found_value, found_package, lcsc, found_voltage, current_x, current_y, ref)

                    results.append({
                        'ref': ref,
                        'type': 'capacitor',
                        'value': found_value,
                        'voltage': found_voltage,
                        'package': found_package,
                        'lcsc': lcsc,
                        'symbol': symbol
                    })

                    symbol_count += 1

            elif comp_type == 'resistor':
                # Search for component in database
                df = db.get_resistors(value, package)

                if len(df) == 0:
                    errors.append(f"{ref_list}: No matching resistor found for {value} {package}")
                    continue

                # Use the first match (best match)
                row = df.iloc[0]
                lcsc = row['lcsc']
                found_value = row['value']
                found_package = row['package']

                # Generate a separate symbol for each reference designator
                for ref in refs:
                    # Calculate position for this symbol
                    current_x = x_pos + (symbol_count % symbols_per_row) * x_spacing
                    current_y = y_pos + (symbol_count // symbols_per_row) * y_spacing

                    # Generate symbol with position and reference
                    if use_small_symbols:
                        symbol = createResistorSymbolSmall(found_value, found_package, lcsc, current_x, current_y, ref)
                    else:
                        symbol = createResistorSymbol(found_value, found_package, lcsc, current_x, current_y, ref)

                    results.append({
                        'ref': ref,
                        'type': 'resistor',
                        'value': found_value,
                        'package': found_package,
                        'lcsc': lcsc,
                        'symbol': symbol
                    })

                    symbol_count += 1
            else:
                errors.append(f"{ref_list}: Unknown component type '{comp_type}'")
                continue

            print(f"  Found: LCSC C{lcsc}")

        except Exception as e:
            errors.append(f"{ref_list}: Error processing component - {str(e)}")
            continue

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# KiCad Symbol Output\n")
        f.write(f"# Generated from: {input_file}\n")
        f.write(f"# Total components: {len(results)}\n\n")

        for result in results:
            f.write(f"# {result['ref']}: {result['value']} {result.get('voltage', '')} {result['package']} - LCSC C{result['lcsc']}\n")
            f.write(result['symbol'])
            f.write("\n\n")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Successfully processed: {len(results)} components")
    print(f"Errors: {len(errors)}")

    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")

    print(f"\nOutput written to: {output_file}")
    print(f"{'='*60}")

    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Batch process JLCPCB components and generate KiCad symbols',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python cli.py components.json output.kicad_sym
  python cli.py components.json output.kicad_sym --large-symbols
  python cli.py input.json -o symbols.txt
        '''
    )

    parser.add_argument('input', help='Input JSON file containing component list')
    parser.add_argument('output', nargs='?', default='output.kicad_sym',
                       help='Output file for generated symbols (default: output.kicad_sym)')
    parser.add_argument('-o', '--output-file', dest='output_alt',
                       help='Alternative way to specify output file')
    parser.add_argument('--large-symbols', action='store_true',
                       help='Use large symbol footprints instead of small')

    args = parser.parse_args()

    # Determine output file
    output_file = args.output_alt if args.output_alt else args.output

    # Process components
    use_small = not args.large_symbols
    success = process_components(args.input, output_file, use_small_symbols=use_small)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
