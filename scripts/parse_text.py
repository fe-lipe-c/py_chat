import re
from datetime import datetime


def convert_to_date(date_string):
    try:
        return datetime.strptime(date_string, "%B %d, %Y").date()
    except ValueError:
        print(f"Invalid date format: {date_string}")
        return None


def convert_to_time(time_string):
    try:
        return datetime.strptime(time_string, "%H:%M:%S").time()
    except ValueError:
        print(f"Invalid time format: {time_string}")
        return None


def parse_text(input_text):
    # Dictionary mapping Portuguese names to English names
    name_map = {
        "Segunda-feira": "Monday",
        "Terça-feira": "Tuesday",
        "Quarta-feira": "Wednesday",
        "Quinta-feira": "Thursday",
        "Sexta-feira": "Friday",
        "Sábado": "Saturday",
        "Domingo": "Sunday",
    }

    # Replacing Portuguese words with English counterparts
    for portuguese, english in name_map.items():
        input_text = input_text.replace(portuguese, english)

    # Dictionary mapping Portuguese names to English names
    name_map = {
        "Janeiro": "January",
        "Fevereiro": "February",
        "Março": "March",
        "Abril": "April",
        "Maio": "May",
        "Junho": "June",
        "Julho": "July",
        "Agosto": "August",
        "Setembro": "September",
        "Outubro": "October",
        "Novembro": "November",
        "Dezembro": "December",
    }

    # Replacing Portuguese words with English counterparts
    for portuguese, english in name_map.items():
        input_text = input_text.replace(portuguese, english)

    # Define the regex patterns
    date_pattern = r"\b(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (\w+ \d+, \d{4})\b"
    # message_pattern = r"(\d{2}:\d{2}:\d{2}) ((?:\w+\s(?=\w))+\w+): ((?:.|\n)+?)(?=\d{2}:\d{2}:\d{2} \w+ \w+:|\Z)"
    message_pattern = r"(\d{2}:\d{2}:\d{2}) (.*?): ((?:(?!\d{2}:\d{2}:\d{2}).|\n)+?)(?=\d{2}:\d{2}:\d{2} |\Z)"
    # message_pattern = r"(\d{2}:\d{2}:\d{2}) (.*?):\s*((?:(?!\d{2}:\d{2}:\d{2}).|\n)+?)(?=\d{2}:\d{2}:\d{2} |\Z)"
    page_pattern = r"\n\nPAGE \d+\s*/\s*\d+\n"
    page_pattern_2 = r"\nPAGE \d+\s*/\s*\d+\n"

    # Remove the page markers
    input_text = re.sub(page_pattern, " ", input_text)
    input_text = re.sub(page_pattern_2, " ", input_text)
    # Use regex to find all dates
    dates = re.findall(date_pattern, input_text, re.DOTALL)

    # Use regex to find all messages
    messages = re.findall(message_pattern, input_text, re.DOTALL)
    if not messages:
        print("No messages found")
        return []

    # Initialize the current date
    current_date = None
    last_time = None
    parsed_messages = []

    dates = [convert_to_date(i) for i in dates]
    dates_iter = iter(dates)

    # Iterate over the messages
    for i, message in enumerate(messages):
        # Extract the time, sender, and content from the message
        time_str, sender, content = message

        time = convert_to_time(time_str)
        if time is None:
            print(f"Skipping message {i+1} due to invalid time: {message}")
            continue

        # Convert the time to a datetime object
        # get the current date
        if i == 0 or time < last_time:
            try:
                current_date = next(dates_iter)
            except StopIteration:
                print(f"Ran out of dates on message {i+1}: {message}")
                # break

        last_time = time

        # Add the message to the parsed messages
        parsed_messages.append(
            {
                "date": current_date,
                "time": time,
                "sender": sender,
                "content": content.strip(),
            }
        )

    return parsed_messages
