import swisseph as swe
from datetime import datetime, timedelta
import pytz


# Download ephemeris files from https://www.astro.com/ftp/swisseph/ephe/
# Extract to a folder and set path:
swe.set_ephe_path('./ephe/')  # REPLACE WITH YOUR PATH

def get_planetary_positions(date):
    """Get planetary positions in zodiac signs for a given date."""
    date_utc = date.astimezone(pytz.utc) if date.tzinfo else date.replace(tzinfo=pytz.utc)
    jd = swe.julday(date_utc.year, date_utc.month, date_utc.day, date_utc.hour + date_utc.minute/60)
    
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
        'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO
    }
    
    positions = {}
    for name, planet in planets.items():
        pos_data = swe.calc_ut(jd, planet)

        
        # Handle nested tuple structure
        if isinstance(pos_data, tuple) and len(pos_data) == 2:
            pos, _ = pos_data  # Extract the first element (planetary positions)
        else:
            pos = pos_data  # Fallback for unexpected structure
        
        # Ensure pos is a tuple with at least one element
        if not isinstance(pos, tuple) or len(pos) < 1:
            print(f"Unexpected output for {name}: {pos}")
            positions[name] = 'Unknown'
            continue
        
        lon = pos[0]  # Extract ecliptic longitude (first element of the tuple)
        if not isinstance(lon, (int, float)):
            print(f"Unexpected longitude for {name}: {lon}")
            positions[name] = 'Unknown'
            continue
        
        sign_num = int(lon // 30)  # Calculate zodiac sign index (0 = Aries, 1 = Taurus, etc.)
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        positions[name] = signs[sign_num]
    
    return positions

def get_lunar_phase(date):
    """Calculate lunar phase name."""
    date_utc = date.astimezone(pytz.utc) if date.tzinfo else date.replace(tzinfo=pytz.utc)
    jd = swe.julday(date_utc.year, date_utc.month, date_utc.day)
    
    # Get Sun and Moon positions
    sun_data = swe.calc_ut(jd, swe.SUN)
    moon_data = swe.calc_ut(jd, swe.MOON)
    
    # Extract ecliptic longitude (first element of the tuple)
    sun_lon = sun_data[0][0] if isinstance(sun_data[0], tuple) else sun_data[0]
    moon_lon = moon_data[0][0] if isinstance(moon_data[0], tuple) else moon_data[0]
    
    # Calculate phase angle
    phase = (moon_lon - sun_lon) % 360
    phase_index = int((phase / 360) * 28)
    
    phases = [
        ('New Moon', 0), ('Waxing Crescent', 45), ('First Quarter', 90),
        ('Waxing Gibbous', 135), ('Full Moon', 180), ('Waning Gibbous', 225),
        ('Last Quarter', 270), ('Waning Crescent', 315)
    ]
    
    for phase_name, threshold in phases:
        if phase < threshold + 22.5:
            return phase_name
    return 'New Moon'

def get_aspects(date, orb=5):
    """Calculate major planetary aspects between planets."""
    date_utc = date.astimezone(pytz.utc) if date.tzinfo else date.replace(tzinfo=pytz.utc)
    jd = swe.julday(date_utc.year, date_utc.month, date_utc.day)
    
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
        'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO
    }
    
    aspects = []
    aspect_defs = {
        0: ('Conjunction', 0),
        60: ('Sextile', 60),
        90: ('Square', 90),
        120: ('Trine', 120),
        180: ('Opposition', 180)
    }
    
    # Check all planet pairs
    pairs = [(p1, p2) for p1 in planets for p2 in planets if p1 < p2]
    for p1, p2 in pairs:
        pos1_data = swe.calc_ut(jd, planets[p1])
        pos2_data = swe.calc_ut(jd, planets[p2])
        
        # Extract ecliptic longitude (first element of the tuple)
        pos1 = pos1_data[0][0] if isinstance(pos1_data[0], tuple) else pos1_data[0]
        pos2 = pos2_data[0][0] if isinstance(pos2_data[0], tuple) else pos2_data[0]
        
        # Calculate angle between planets
        angle = abs(pos1 - pos2) % 360
        angle = min(angle, 360 - angle)
        
        # Check for aspects within orb tolerance
        for aspect_deg, (aspect_name, _) in aspect_defs.items():
            if abs(angle - aspect_deg) <= orb:
                aspects.append(f"{p1} {aspect_name} {p2}")
    
    return aspects

if __name__ == "__main__":
    date = datetime(2023, 10, 25)
    positions = get_planetary_positions(date)
    print(positions)
