def find_duplicates_ignore_case(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        item_lower = item.lower()
        if item_lower in seen:
            duplicates.add(item_lower)
        else:
            seen.add(item_lower)
    return duplicates
