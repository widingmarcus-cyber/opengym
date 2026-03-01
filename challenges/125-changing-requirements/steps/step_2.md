Requirements have CHANGED. Update setup/converter.py:
1. Add Kelvin support: celsius_to_kelvin(c), kelvin_to_celsius(k)
2. Add a unified convert(value, from_unit, to_unit) function that handles all 6 conversions (C<->F, C<->K, F<->K)
3. The convert() function should raise ValueError for unknown units
4. Keep the existing celsius_to_fahrenheit and fahrenheit_to_celsius functions working
DO NOT start from scratch -- build on your previous implementation.
