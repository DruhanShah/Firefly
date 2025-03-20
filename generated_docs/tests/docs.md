# Documentation for ./tests

This documentation explains the functionality provided in the `test.py` file for timezone parsing and configuration handling.

---

## Timezone Parsing and Configuration Handling

### Purpose
The code snippet provides utilities for:
- Parsing timezone strings formatted as `UTC[+-]hh:mm` into `datetime.timezone` objects.
- Defining a simple configuration class for storing values by name.

### Functionality

#### 1. Time Zone Parsing
- **Function:** `parse_timezone`
  - **Description:** Converts a string representing a timezone offset in the format `UTC[+-]hh:mm` into a `datetime.timezone` object.
  - **Error Handling:** Raises a `ValueError` if the input string does not match the expected format.

#### 2. Configuration Class
- **Class:** `ConfigValue`
  - **Description:** Creates objects to store configuration values identified by a name.

### Key Components
- **Regex Pattern (`UTC_OFFSET_PATTERN`):** Validates that the provided timezone string adheres to the `UTC[+-]hh:mm` format.
- **Regex Object (`UTC_OFFSET_RE`):** Compiles the regex pattern for improved performance.
- **Function (`parse_timezone`):** Parses the input string and returns the corresponding `datetime.timezone` object.
- **Class (`ConfigValue`):** Provides a simple mechanism for handling named configuration values.

---

## Usage Examples

### Parsing a Timezone String
```python
from datetime import timezone

# Parse a timezone string with a positive offset
tz = parse_timezone("UTC+05:30")
print(tz)  # Expected Output: UTC+05:30

# Parse a string representing UTC (no offset)
utc_tz = parse_timezone("UTC")
print(utc_tz)  # Expected Output: UTC
```

### Using the ConfigValue Class
```python
# Create a configuration value with a specified name
config = ConfigValue(name="example_config")
print(config.name)  # Expected Output: example_config
```

---

## Rationale
- **Regex Validation:** Using regex ensures that only correctly formatted timezone strings are processed.
- **Lightweight Configuration:** The `ConfigValue` class provides an uncomplicated way to manage named configuration values.

---

## Additional Information
- The `parse_timezone` function supports only UTC time zones and offsets in the `UTC[+-]hh:mm` format.
- Improper formatting (e.g., `UTC+99:99`) will trigger a `ValueError`.

### Example of Handling an Invalid Timezone Format
```python
try:
    # This input will raise a ValueError due to an invalid time format.
    parse_timezone("UTC+99:99")
except ValueError as e:
    print(e)
```