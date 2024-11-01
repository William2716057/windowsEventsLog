import win32evtlog
import datetime

# Get user input
date_input = input("Enter date in YYYY-MM-DD format: ")

# Convert input to a date
date = datetime.datetime.strptime(date_input, "%Y-%m-%d")
start_of_month = date.replace(day=1)
start_of_next_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1)

# Event IDs
event_ids = {6006, 6008, 6005, 4624, 4719, 4907, 4946, 4688, 4689 }

# Open the System event log
server = 'localhost'  # For local machine
log_type = 'System'
log_handle = win32evtlog.OpenEventLog(server, log_type)

# Set flags for the log query
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

# Read and filter events
events = []
while True:
    records = win32evtlog.ReadEventLog(log_handle, flags, 0)
    if not records:
        break
    for record in records:
        event_id = record.EventID & 0xFFFF  # Extract event ID
        event_time = record.TimeGenerated
        if event_id in event_ids and start_of_month <= event_time < start_of_next_month:
            events.append({
                "TimeGenerated": event_time,
                "EventID": event_id,
            })

# Close log handle
win32evtlog.CloseEventLog(log_handle)

# Display results
for event in events:
    print(f"TimeGenerated: {event['TimeGenerated']}, EventID: {event['EventID']}")