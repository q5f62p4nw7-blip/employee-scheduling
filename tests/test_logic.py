from logic import is_valid_shift_time
from logic import has_shift_conflict


print("Running tests...")


assert is_valid_shift_time("09:00", "17:00") == True
assert is_valid_shift_time("17:00", "09:00") == False

assert has_shift_conflict({"id": 1}) == True
assert has_shift_conflict(None) == False

duplicate_shift = {
    "employee_id": 1,
    "shift_date": "2026-05-31"
}

assert has_shift_conflict(duplicate_shift) == True


print("All tests passed.")