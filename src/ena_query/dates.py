from dateutil.parser import parse

def clean_date(date_str):
    if len(date_str) > 15:
        return None
    try:
        return int(parse(date_str).year)
    except Exception as e:
        print(f"Error parsing date: {date_str} - {e}")
        return None

