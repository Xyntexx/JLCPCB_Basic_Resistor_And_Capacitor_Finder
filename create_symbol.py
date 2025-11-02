from utils.units import convertToShorthandNotation
packages_R = {"0402": "R_0402_1005Metric",
              "0603": "R_0603_1608Metric",
              "0805": "R_0805_2012Metric",
              "1206": "R_1206_3216Metric",
              "1210": "R_1210_3225Metric",
              "2010": "R_2010_5025Metric",
              "2512": "R_2512_6332Metric"}

packages_C = {"0402": "C_0402_1005Metric",
              "0603": "C_0603_1608Metric",
              "0805": "C_0805_2012Metric",
              "1206": "C_1206_3216Metric",
              "1210": "C_1210_3225Metric",
              "2010": "C_2010_5025Metric",
              "2512": "C_2512_6332Metric"}


def createResistorSymbol(value, package, lcsc, x=0, y=0, ref="R0"):
    package_lib = packages_R[package]
    value = convertToShorthandNotation(value)
    # Calculate absolute positions for properties
    ref_x = x + 2.54
    ref_y = y - 1.2701
    val_x = x + 2.54
    val_y = y + 1.2699
    s = f"""(lib_symbols
  (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R" (at 0 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "R res resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_fp_filters" "R_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "R_0_1"
      (rectangle (start -1.016 -2.54) (end 1.016 2.54)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
    )
    (symbol "R_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)

(symbol (lib_id "Device:R") (at {x} {y} 180) (unit 1)
  (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
  (property "Reference" "{ref}" (at {ref_x} {ref_y} 0)
    (effects (font (size 1.27 1.27)) (justify right))
  )
  (property "Value" "{value}" (at {val_x} {val_y} 0)
    (effects (font (size 1.27 1.27)) (justify right))
  )
  (property "Footprint" "Resistor_SMD:{package_lib}" (at 1.778 0 90)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Datasheet" "~" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Description" "Resistor" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "LCSC" "C{lcsc}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (pin "2" (uuid "")
  )
  (pin "1" (uuid "")
  )
  (instances
    (project ""
      (path ""
        (reference "{ref}") (unit 1)
      )
    )
  )
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc, x=x, y=y, ref=ref, ref_x=ref_x, ref_y=ref_y, val_x=val_x, val_y=val_y)


def createResistorSymbolSmall(value, package, lcsc, x=0, y=0, ref="R0"):
    package_lib = packages_R[package]
    value = convertToShorthandNotation(value)
    # Calculate absolute positions for properties
    ref_x = x + 2.54
    ref_y = y - 1.2701
    val_x = x + 2.54
    val_y = y + 1.2699
    s = f"""(lib_symbols
  (symbol "Device:R_Small" (pin_numbers hide) (pin_names (offset 0.254) hide) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 0.762 0.508 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "R_Small" (at 0.762 -1.016 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Resistor, small symbol" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "R resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_fp_filters" "R_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "R_Small_0_1"
      (rectangle (start -0.762 1.778) (end 0.762 -1.778)
        (stroke (width 0.2032) (type default))
        (fill (type none))
      )
    )
    (symbol "R_Small_1_1"
      (pin passive line (at 0 2.54 270) (length 0.762)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -2.54 90) (length 0.762)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)

(symbol (lib_id "Device:R_Small") (at {x} {y} 0) (unit 1)
  (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
  (property "Reference" "{ref}" (at {ref_x} {ref_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "{value}" (at {val_x} {val_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Footprint" "Resistor_SMD:{package_lib}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Datasheet" "~" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Description" "Resistor, small symbol" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "LCSC" "C{lcsc}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (pin "2" (uuid "")
  )
  (pin "1" (uuid "")
  )
  (instances
    (project ""
      (path ""
        (reference "{ref}") (unit 1)
      )
    )
  )
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc, x=x, y=y, ref=ref, ref_x=ref_x, ref_y=ref_y, val_x=val_x, val_y=val_y)


def createCapacitorSymbol(value, package, lcsc, voltage, x=0, y=0, ref="C0"):
    package_lib = packages_C[package]
    value = convertToShorthandNotation(value)
    # Calculate absolute positions for properties
    ref_x = x + 3.81
    ref_y = y - 1.2701
    val_x = x + 3.81
    val_y = y + 1.2699
    s = f"""(lib_symbols
  (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.635 2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C" (at 0.635 -2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0.9652 -3.81 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Unpolarized capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "cap capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_fp_filters" "C_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "C_0_1"
      (polyline
        (pts
          (xy -2.032 -0.762)
          (xy 2.032 -0.762)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy -2.032 0.762)
          (xy 2.032 0.762)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
    )
    (symbol "C_1_1"
      (pin passive line (at 0 3.81 270) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)

(symbol (lib_id "Device:C") (at {x} {y} 0) (unit 1)
  (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
  (property "Reference" "{ref}" (at {ref_x} {ref_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "{value} {voltage}" (at {val_x} {val_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Footprint" "Capacitor_SMD:{package_lib}" (at 0.9652 3.81 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Datasheet" "~" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Description" "Unpolarized capacitor" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "LCSC" "C{lcsc}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (pin "1" (uuid "")
  )
  (pin "2" (uuid "")
  )
  (instances
    (project ""
      (path ""
        (reference "{ref}") (unit 1)
      )
    )
  )
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc, voltage=voltage, x=x, y=y, ref=ref, ref_x=ref_x, ref_y=ref_y, val_x=val_x, val_y=val_y)


def createCapacitorSymbolSmall(value, package, lcsc, voltage, x=0, y=0, ref="C0"):
    package_lib = packages_C[package]
    value = convertToShorthandNotation(value)
    # Calculate absolute positions for properties
    ref_x = x + 2.54
    ref_y = y - 1.2638
    val_x = x + 2.54
    val_y = y + 1.2762
    s = f"""(lib_symbols
  (symbol "Device:C_Small" (pin_numbers hide) (pin_names (offset 0.254) hide) (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.254 1.778 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C_Small" (at 0.254 -2.032 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Unpolarized capacitor, small symbol" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "capacitor cap" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_fp_filters" "C_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "C_Small_0_1"
      (polyline
        (pts
          (xy -1.524 -0.508)
          (xy 1.524 -0.508)
        )
        (stroke (width 0.3302) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy -1.524 0.508)
          (xy 1.524 0.508)
        )
        (stroke (width 0.3048) (type default))
        (fill (type none))
      )
    )
    (symbol "C_Small_1_1"
      (pin passive line (at 0 2.54 270) (length 2.032)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -2.54 90) (length 2.032)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)

(symbol (lib_id "Device:C_Small") (at {x} {y} 0) (unit 1)
  (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
  (property "Reference" "{ref}" (at {ref_x} {ref_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "{value} {voltage}" (at {val_x} {val_y} 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Footprint" "Capacitor_SMD:{package_lib}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Datasheet" "~" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "Description" "Unpolarized capacitor, small symbol" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (property "LCSC" "C{lcsc}" (at 0 0 0)
    (effects (font (size 1.27 1.27)) (hide yes))
  )
  (pin "1" (uuid "")
  )
  (pin "2" (uuid "")
  )
  (instances
    (project ""
      (path ""
        (reference "{ref}") (unit 1)
      )
    )
  )
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc, voltage=voltage, x=x, y=y, ref=ref, ref_x=ref_x, ref_y=ref_y, val_x=val_x, val_y=val_y)
