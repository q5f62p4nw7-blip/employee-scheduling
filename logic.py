def is_valid_shift_time(start_time, end_time):
    return start_time < end_time


def has_shift_conflict(existing_shift):
    return existing_shift is not None