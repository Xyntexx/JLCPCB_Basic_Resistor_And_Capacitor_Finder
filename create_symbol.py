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


def createResistorSymbol(value, package, lcsc):
    package_lib = packages_R[package]
    value = convertToShorthandNotation(value)
    s = f"""(lib_symbols
  (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R" (at 0 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "R res resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "R_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
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

(symbol (lib_id "Device:R") (at 133.35 93.98 270) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid 3bdd9ea2-b74c-4d3b-9499-90745dafde71)
  (property "Reference" "R101" (at 133.35 96.52 90)
    (effects (font (size 1.27 1.27)))
  )
  (property "Value" "{value}" (at 134.62 91.44 90)
    (effects (font (size 1.27 1.27)))
  )
  (property "Footprint" "Resistor_SMD:{package_lib}" (at 133.35 92.202 90)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "Datasheet" "~" (at 133.35 93.98 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "LCSC" "C{lcsc}" (at 133.35 93.98 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (pin "1" (uuid 6e207a43-f9f8-4882-b011-013523d3670d))
  (pin "2" (uuid 5d2b3056-f435-42cd-b7f4-1678fa653eac))
  (instances
  )
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc)


def createCapacitorSymbol(value, package, lcsc, voltage):
    package_lib = packages_R[package]
    value = convertToShorthandNotation(value)
    s = f"""(lib_symbols
  (symbol "Device:C_Small" (pin_numbers hide) (pin_names (offset 0.254) hide) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.254 1.778 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C_Small" (at 0.254 -2.032 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "capacitor cap" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Unpolarized capacitor, small symbol" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "C_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
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

(symbol (lib_id "Device:C_Small") (at 63.5 67.31 0) (mirror x) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid af931f83-f0d7-4d1c-af01-4b5144b5078d)
  (property "Reference" "C4" (at 66.04 68.58 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "{value} {voltage}" (at 66.04 66.04 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Footprint" "Capacitor_SMD:{package_lib}" (at 63.5 67.31 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "Datasheet" "~" (at 63.5 67.31 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "LCSC" "{lcsc}" (at 63.5 67.31 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (pin "1" (uuid 2b58b1a6-f663-4b5d-955f-81a6a0feee1d))
  (pin "2" (uuid 973279a1-bf9a-4b95-826e-cbf7c2d552a6))
)
"""
    return s.format(value=value, package_lib=package_lib, lcsc=lcsc, voltage=voltage)
