# Step 1: Fix Corruption and Add Records

Read `setup/data.json`. It contains 5 sensor records, but **record 3** (id=3, sensor_gamma) has a corrupted "value" field -- it was truncated due to a simulated partial write interruption.

Your tasks:

1. **Fix record 3**: The value field is truncated at `"temperature:21.3,humi"`. Repair it so it follows the same format as the other records: `"temperature:XX.X,humidity:XX.X,pressure:XXXX.XX"`. Use reasonable sensor values for the missing fields (humidity and pressure).

2. **Add 5 new records** with IDs 6 through 10. Each record must follow the same structure:
   - `"id"`: integer (6, 7, 8, 9, 10)
   - `"name"`: a sensor name string (e.g., "sensor_zeta", "sensor_eta", etc.)
   - `"value"`: a string in the format `"temperature:XX.X,humidity:XX.X,pressure:XXXX.XX"` with plausible numeric values

After this step, `setup/data.json` must contain exactly 10 records, all with complete and valid value fields.
