import pandas as pd
from datetime import datetime
import re
from word2number import w2n
from dateutil import parser


def standardize_date(date_str, previous_normalized_value=None):
    """
    Standardize the date format to YYYY-MM-DD, YYYY, or other specified formats.
    Handles special cases like "now", "original", and "Previous".
    """
    # Handle special cases
    # Convert date_str to lower case for case-insensitive comparison
    lower_date_str = date_str.lower()

    # Handle special cases
    if lower_date_str in ["now", "original", "previous","today"]:
        return previous_normalized_value

    # Patterns for date matching
    patterns = [
        '%m/%y', '%m/%Y',   # 8/61 format
        '%B %y', '%B %Y',   # April 2063 format
        '%b %y', '%b %Y',
        '%Y%m%d',
        '%d %B %y', '%d %B %Y', # 22 April 2063 format
        '%d-%b-%y', '%d-%b-%Y',  # 27-Nov-63 format
        '%d/%m/%Y', '%d/%m/%y',
        '%d.%m.%Y', '%d.%m.%y',
        '%d-%m-%Y', '%d-%m-%y',
        '%Y/%m/%d',
        '%Y'  # Year only
    ]
    
    # Attempt to match patterns
    for pattern in patterns:
        try:
            parsed_date = datetime.strptime(date_str, pattern)

            # Ensure the year is after 2000 for two-digit year formats
            if '%y' in pattern and parsed_date.year < 2000:
                parsed_date = parsed_date.replace(year=parsed_date.year + 100)

            # Format the date based on the pattern
            if pattern == '%Y':
                return parsed_date.strftime('%Y')
            elif pattern in('%B %Y','%B %y'):
                return parsed_date.strftime('%Y-%m')
            else:
                return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue


    # Return None if no pattern matches
    return None



def standardize_time(time_str, previous_normalized_value=None):
    
    # Convert date_str to lower case for case-insensitive comparison
    lower_time_str = time_str.lower()

    # Handle special cases
    if lower_time_str in ["now", "original", "previous","today"]:
        return previous_normalized_value
    
    # 处理特殊格式 '1635hr on 21/5/12' 和其他格式
    special_format_regex = re.compile(
        r'(\d{1,2})[:.]?(\d{2})(am|pm|hr|hrs)?\s?(?:at|on|,|and)?\s(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})|'
        r'(\d{2})(\d{2})hr\s?on\s(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})',
        re.IGNORECASE
    )
    
    match = special_format_regex.search(time_str)
    if match:
        groups = match.groups()
        if groups[0] is not None:  # Matches the first pattern
            hour, minute, ampm, day, month, year = groups[:6]
            hour = int(hour)

            # Adjust for 12-hour time with am/pm provided, considering 24-hour format
            if ampm:
                if ampm.lower() == 'pm' and hour < 12:
                    hour += 12
                elif ampm.lower() == 'am' and hour == 12:
                    hour = 0
            else:
                # Handle 24-hour format
                hour = hour % 24
        else:  # Matches the second pattern
            hour, minute, day, month, year = groups[6:]
            hour, minute = int(hour), int(minute)

        # Handle two-digit year
        year = f'20{year}' if len(year) == 2 else year

        try:
            # Ensure all components are integers
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)

            # Construct and format the datetime object
            return datetime(year, month, day, hour, minute).strftime('%Y-%m-%dT%H:%M')
        except ValueError:
            pass  # Handle the ValueError if conversion fails 
   
    # 处理 "at 3.36pm on 0408.13" 这样的格式
    datetime_regex = re.compile(r'(?:at\s)?(\d{1,2})([:.]?)(\d{2})(am|pm|hr|hrs)?\s?(?:on\s(?:the\s)?)?(\d{1,2})[./]?(\d{1,2})[./]?(\d{2,4})', re.IGNORECASE)
    match = datetime_regex.search(time_str)
    if match:
        hour, separator, minute, ampm, day, month, year = match.groups()

        hour = int(hour)
        minute = int(minute)

        # 处理带有 'pm' 或 'am' 的24小时制时间格式
        if ampm:
            if ampm.lower() in ['pm', 'hrs', 'hr'] and hour < 12:
                hour += 12
            elif ampm.lower() == 'am' and hour == 12:
                hour = 0

        # 处理年份
        year = f'20{year}' if len(year) == 2 else year

        try:
            # Construct and format the datetime object
            return datetime(int(year), int(month), int(day), hour, int(minute)).strftime('%Y-%m-%dT%H:%M')
        except ValueError:
            pass  # Continue to try other formats if a ValueError is raised
    
    # 处理 "on 06.08.13 at 6.00pm" 等格式
    new_format_regex = re.compile(
        r'(?:on\s)?(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})\s?(?:at|on)?\s(\d{1,2})([.:])?(\d{2})(am|pm|hr|hrs)',
        re.IGNORECASE
    )

    match = new_format_regex.search(time_str)
    if match:
        day, month, year, hour, separator, minute, ampm = match.groups()

        hour = int(hour)
        minute = int(minute)

        # 处理带有 'pm' 或 'am' 的24小时制时间格式
        if ampm:
            if ampm.lower() in ['pm', 'hrs', 'hr'] and hour < 12:
                hour += 12
            elif ampm.lower() == 'am' and hour == 12:
                hour = 0

        # 处理年份
        year = f'20{year}' if len(year) == 2 else year

        try:
            # 构造并格式化datetime对象
            return datetime(int(year), int(month), int(day), hour, minute).strftime('%Y-%m-%dT%H:%M')
        except ValueError:
            pass  # 如果转换失败，尝试其他格式


    # at 3.40pm - 处理只有时间没有日期的情况
    time_only_regex = re.compile(
        r'(?:at\s*)?(\d{1,2})[.:](\d{2})\s*(am|pm)(?!\s+on\s+\d{1,2}[/.]\d{1,2}[/.]\d{2,4})',
        re.IGNORECASE
    )

    match = time_only_regex.search(time_str)
    if match:
        hour, minute, ampm = match.groups()
        hour = int(hour)
        
        # Convert 12-hour time to 24-hour time
        if ampm.lower() == 'pm' and hour < 12:
            hour += 12
        elif ampm.lower() == 'am' and hour == 12:
            hour = 0

        # Ensure hour is within 0 to 23
        hour = hour % 24

        # Return the standardized time format
        return datetime(1900, 1, 1, hour, int(minute)).strftime('T%H:%M')
    
    
    # 处理新的时间格式 '2512-10-20 00:00:00'
    iso_format_regex = re.compile(
        r'(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})',
        re.IGNORECASE
    )
    iso_match = iso_format_regex.search(time_str)
    if iso_match:
        year, month, day, hour, minute, second = iso_match.groups()
        return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime('%Y-%m-%dT%H:%M:%S')
    
        
    # 尝试使用 dateutil 解析器
    try:
        dt = parser.parse(time_str, dayfirst=True)
        return dt.strftime('%Y-%m-%dT%H:%M')
    except ValueError:
        pass  # 如果 dateutil 无法解析，尝试其他自定义规则

    # 可以添加更多的自定义解析规则...
    
    return None  




def standardize_duration(duration_str):
    """
    Standardize the duration format to ISO 8601 duration format.
    Converts durations specified in words or complex formats into the standard format.
    """
    # Handle ranges like '9-10 weeks'
    range_regex = re.compile(r'(\d+)-(\d+)\s*(weeks?|months?|years?|days?)', re.IGNORECASE)
    range_match = range_regex.match(duration_str)
    if range_match:
        start, end, unit = range_match.groups()
        avg = (float(start) + float(end)) / 2
        unit = unit[0].upper()  # 'weeks' -> 'W', 'months' -> 'M', etc.
        return f"P{avg}{unit}"

    # Handle formats like '40/year'
    per_year_regex = re.compile(r'(\d+)/\s*(year)', re.IGNORECASE)
    per_year_match = per_year_regex.match(duration_str)
    if per_year_match:
        num, _ = per_year_match.groups()
        return f"P{num}Y"

    # Regular expressions for different duration formats
    patterns = [
        (re.compile(r'(\d+|\w+)\s*(years?|yrs?)|P(\d+)Y', re.IGNORECASE), "Y"),
        (re.compile(r'(\d+|\w+)\s*(months?|mths?)|P(\d+)M', re.IGNORECASE), "M"),
        (re.compile(r'(\d+|\w+)\s*(weeks?|wks?)|P(\d+)W', re.IGNORECASE), "W"),
        (re.compile(r'(\d+|\w+)\s*days?|P(\d+)D', re.IGNORECASE), "D")
    ]

    for regex, unit in patterns:
        match = regex.match(duration_str)
        if match:
            num = next((m for m in match.groups() if m is not None), None)
            if num and not num.isnumeric():
                try:
                    num = w2n.word_to_num(num.lower())
                except ValueError:
                    continue
            if num:
                return f"P{num}{unit}"

    return None

def standardize_set(set_str):
    """
    Standardize the 'SET' category format.
    """
    if set_str.lower() == 'twice':
        return 'R2'
    elif set_str.lower() == 'years':
        return 'RP1D'
    else:
        return None

def integrate_standardization_functions(extracted_data):
    """
    Integrate the date standardization function into the existing dataframe processing flow,
    handling the 'DATE', 'TIME', 'DURATION', and 'SET' categories.
    """
    previous_normalized_value = None

    def process_row(row):
        nonlocal previous_normalized_value
        if row['Category'] == 'DATE':
            normalized_value = standardize_date(row['Original Text'], previous_normalized_value)
            previous_normalized_value = normalized_value
            return normalized_value
        elif row['Category'] == 'TIME':
            normalized_value = standardize_time(row['Original Text'], previous_normalized_value)
            previous_normalized_value = normalized_value
            return normalized_value
        elif row['Category'] == 'DURATION':
            return standardize_duration(row['Original Text'])
        elif row['Category'] == 'SET':
            return standardize_set(row['Original Text'])
        else:
            return row['Normalized Value']

    # Apply the processing function to each row in the dataframe
    extracted_data['Normalized Value Corrected'] = extracted_data.apply(process_row, axis=1)
    return extracted_data

file_path = './extracted_data.csv'  # Updated file path
extracted_data = pd.read_csv(file_path)
extracted_data = integrate_standardization_functions(extracted_data)

# Displaying the first few rows of the dataframe with the corrected normalized values
# print(extracted_data)

# Save the dataframe to a new CSV file
output_file_path = './processed_data2.csv'  # Specify your desired output file path
extracted_data.to_csv(output_file_path, index=False)  # Set index=False to exclude row indices from the CSV file

print(f"Data successfully saved to {output_file_path}")
# Test the function with provided examples
# test_date = ['27-Nov-63', 'December 2062']
# standardized_date = [standardize_date(date) for date in test_date]
# print(standardized_date)

# test_times = ['10.40am on 23.9.14', 'at 3.40pm', '4:26pm on 16/54/14', '2013/9/23 14:00']
# standardized_times = [standardize_time(time) for time in test_times]
# print(standardized_times)
