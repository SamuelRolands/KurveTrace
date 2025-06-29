import fastf1
session = fastf1.get_session(2023, 'Monza', 'Q')
session.load()
laps = session.laps.pick_driver('VER')  # Verstappen
lap = laps.pick_fastest()
telemetry = lap.get_car_data()
print("Hello")