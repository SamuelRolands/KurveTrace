import fastf1
from fastf1.plotting import setup_mpl
from fastf1.tools import delta_time
from fastf1.plotting import DRIVER_COLORS
from fastf1 import plotting
import streamlit as st
import matplotlib.pyplot as plt


fastf1.Cache.enable_cache('f1_cache') 


plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=True)


st.title("F1 Telemetry Comparison Tool 🏎️")
st.write("Select two drivers to compare their telemetry data from the 2021 Italian GP (Monza)")


year = 2021
gp = "Italian"
session_type = "R"  # R = Race


with st.spinner('Loading session data...'):
    session = fastf1.get_session(year, gp, session_type)
    session.load()


drivers = session.drivers
driver_names = {drv: session.get_driver(drv)['LastName'] for drv in drivers}

driver1 = st.selectbox("Select Driver 1", options=drivers, format_func=lambda x: driver_names[x])
driver2 = st.selectbox("Select Driver 2", options=drivers, format_func=lambda x: driver_names[x], index=1)

if driver1 == driver2:
    st.warning("Please select two different drivers.")
    st.stop()


lap1 = session.laps.pick_driver(driver1).pick_fastest()
lap2 = session.laps.pick_driver(driver2).pick_fastest()


tel1 = lap1.get_car_data().add_distance()
tel2 = lap2.get_car_data().add_distance()


fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(tel1['Distance'], tel1['Speed'], label=driver_names[driver1])
ax[0].plot(tel2['Distance'], tel2['Speed'], label=driver_names[driver2])
ax[0].set_ylabel("Speed (km/h)")
ax[0].legend()

ax[1].plot(tel1['Distance'], tel1['Throttle'], label=driver_names[driver1])
ax[1].plot(tel2['Distance'], tel2['Throttle'], label=driver_names[driver2])
ax[1].set_ylabel("Throttle (%)")

ax[2].plot(tel1['Distance'], tel1['Brake'], label=driver_names[driver1])
ax[2].plot(tel2['Distance'], tel2['Brake'], label=driver_names[driver2])
ax[2].set_ylabel("Brakes (%)")
ax[2].set_xlabel("Distance (m)")

st.pyplot(fig)


r1 = lap1.get_car_data().add_distance()
r2 = lap2.get_car_data().add_distance()

delta, ref = delta_time.compare_laps(lap1, lap2)

fig_delta, ax_delta = plt.subplots(figsize=(10, 3))
ax_delta.plot(delta['Distance'], delta['Delta'], color='purple')
ax_delta.set_ylabel("Delta Time (s)")
ax_delta.set_xlabel("Distance (m)")
ax_delta.axhline(0, color='black', linestyle='--')
st.subheader("Lap Time Delta")
st.pyplot(fig_delta)


color1 = DRIVER_COLORS.get(driver1, 'blue')
color2 = DRIVER_COLORS.get(driver2, 'red')

ax[0].plot(tel1['Distance'], tel1['Speed'], label=..., color=color1)
