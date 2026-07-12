import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from ics import Calendar, Event

# --- CONFIGURATION ---
LATITUDE = 45.487
LONGITUDE = -122.804
TIMEZONE = "America/Los_Angeles"
LOCATION_NAME = "Beaverton"
DAYS_AHEAD = 1800

PLANETARY_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
DAY_RULERS = {
    0: "Moon",     # Monday
    1: "Mars",     # Tuesday
    2: "Mercury",  # Wednesday
    3: "Jupiter",  # Thursday
    4: "Venus",    # Friday
    5: "Saturn",   # Saturday
    6: "Sun"       # Sunday
}

def get_planetary_hours():
    loc = LocationInfo(LOCATION_NAME, "", TIMEZONE, LATITUDE, LONGITUDE)
    tz = pytz.timezone(TIMEZONE)
    cal = Calendar()
    
    today = datetime.date.today()
    
    for i in range(DAYS_AHEAD):
        current_day = today + datetime.timedelta(days=i)
        
        try:
            s = sun(loc.observer, date=current_day, tzinfo=tz)
            sunrise = s['sunrise']
            sunset = s['sunset']
        except Exception:
            continue
            
        next_day = current_day + datetime.timedelta(days=1)
        next_s = sun(loc.observer, date=next_day, tzinfo=tz)
        next_sunrise = next_s['sunrise']
        
        day_length = (sunset - sunrise).total_seconds() / 12
        night_length = (next_sunrise - sunset).total_seconds() / 12
        
        weekday = current_day.weekday()
        starting_ruler = DAY_RULERS[weekday]
        start_index = PLANETARY_ORDER.index(starting_ruler)
        
        for hour in range(12):
            ruler = PLANETARY_ORDER[(start_index + hour) % 7]
            start_time = sunrise + datetime.timedelta(seconds=hour * day_length)
            end_time = start_time + datetime.timedelta(seconds=day_length)
            
            e = Event(
                name=f"Hour of {ruler} (Day {hour + 1})",
                begin=start_time,
                end=end_time,
                description=f"Planetary hour ruled by {ruler}"
            )
            cal.events.add(e)
            
        for hour in range(12):
            ruler = PLANETARY_ORDER[(start_index + 12 + hour) % 7]
            start_time = sunset + datetime.timedelta(seconds=hour * night_length)
            end_time = start_time + datetime.timedelta(seconds=night_length)
            
            e = Event(
                name=f"Hour of {ruler} (Night {hour + 1})",
                begin=start_time,
                end=end_time,
                description=f"Planetary hour ruled by {ruler}"
            )
            cal.events.add(e)
            
    with open("planetary_hours.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    get_planetary_hours()
