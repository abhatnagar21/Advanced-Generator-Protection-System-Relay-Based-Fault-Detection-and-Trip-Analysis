import numpy as np
import matplotlib.pyplot as plt
import datetime

class GeneratorProtection:
    def __init__(self, current, voltage, frequency, excitation, rotor_current, power, impedance, power_angle, zero_seq_voltage, rotor_leakage, v_per_hz, ct_ratio=1000):
        self.current = current  # Generator current in A
        self.voltage = voltage  # Generator voltage in p.u.
        self.frequency = frequency  # Generator frequency in Hz
        self.excitation = excitation  # Excitation voltage in p.u.
        self.rotor_current = rotor_current  # Rotor circuit current in A
        self.power = power  # Active power in MW
        self.impedance = impedance  # Impedance in p.u.
        self.power_angle = power_angle  # Power angle in degrees
        self.zero_seq_voltage = zero_seq_voltage  # Zero sequence voltage in p.u.
        self.rotor_leakage = rotor_leakage  # Rotor leakage current in A
        self.v_per_hz = v_per_hz  # Volts per Hz ratio
        self.ct_ratio = ct_ratio  # Current transformer ratio
        self.event_log = []  # Stores relay activation events

    def log_event(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.event_log.append(f"{timestamp} - {event}")

    def overcurrent_protection(self, pickup_factor=1.2):
        pickup_current = pickup_factor * self.current / self.ct_ratio
        if self.current > pickup_current:
            self.log_event("Overcurrent Trip Activated")
            return True
        return False

    def differential_protection(self, terminal_current1, terminal_current2):
        differential_current = abs(terminal_current1 - terminal_current2)
        if differential_current > (0.2 * self.current):
            self.log_event("Differential Protection Trip")
            return True
        return False

    def voltage_protection(self, overvoltage_limit=1.1, undervoltage_limit=0.9):
        if self.voltage > overvoltage_limit:
            self.log_event("Overvoltage Trip")
            return "Overvoltage Trip"
        elif self.voltage < undervoltage_limit:
            self.log_event("Undervoltage Trip")
            return "Undervoltage Trip"
        return "Voltage Normal"

    def reverse_power_protection(self, threshold=0.05):
        if self.power < threshold:
            self.log_event("Reverse Power Trip")
            return True
        return False

    def negative_sequence_protection(self, unbalanced_current, threshold=0.1):
        if unbalanced_current > threshold * self.current:
            self.log_event("Negative Sequence Trip")
            return True
        return False

    def frequency_protection(self, overfreq_limit=51, underfreq_limit=49):
        if self.frequency > overfreq_limit:
            self.log_event("Overfrequency Trip")
            return "Overfrequency Trip"
        elif self.frequency < underfreq_limit:
            self.log_event("Underfrequency Trip")
            return "Underfrequency Trip"
        return "Frequency Normal"

    def loss_of_excitation_protection(self, threshold=0.5):
        if self.impedance > threshold:
            self.log_event("Loss of Excitation Trip")
            return True
        return False

    def stator_earth_fault_protection(self, threshold=0.05):
        if self.zero_seq_voltage > threshold:
            self.log_event("Stator Earth Fault Trip")
            return True
        return False

    def rotor_earth_fault_protection(self, threshold=0.1):
        if self.rotor_leakage > threshold:
            self.log_event("Rotor Earth Fault Trip")
            return True
        return False

    def out_of_step_protection(self, limit=120):
        if abs(self.power_angle) > limit:
            self.log_event("Out-of-Step Trip")
            return True
        return False

    def overfluxing_protection(self, limit=1.2):
        if self.v_per_hz > limit:
            self.log_event("Overfluxing Trip")
            return True
        return False

    def display_event_log(self):
        print("Event Log:")
        for event in self.event_log:
            print(event)

# Example usage
gen_prot = GeneratorProtection(current=1200, voltage=1.05, frequency=50, excitation=1.0, rotor_current=50, power=-0.01, impedance=0.6, power_angle=130, zero_seq_voltage=0.06, rotor_leakage=0.12, v_per_hz=1.3)

print("Overcurrent Trip:", gen_prot.overcurrent_protection())
print("Voltage Protection:", gen_prot.voltage_protection())
print("Frequency Protection:", gen_prot.frequency_protection())
print("Reverse Power Protection:", gen_prot.reverse_power_protection())
print("Loss of Excitation:", gen_prot.loss_of_excitation_protection())
print("Out of Step Protection:", gen_prot.out_of_step_protection())
print("Overfluxing Protection:", gen_prot.overfluxing_protection())

# Display event log
gen_prot.display_event_log()

# Graphical Representation
frequencies = np.linspace(48, 52, 100)
overfrequency_trips = [1 if f > 51 else 0 for f in frequencies]
underfrequency_trips = [1 if f < 49 else 0 for f in frequencies]

power_angles = np.linspace(0, 180, 100)
out_of_step_trips = [1 if angle > 120 else 0 for angle in power_angles]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(frequencies, overfrequency_trips, label='Overfrequency Trip', color='r')
plt.plot(frequencies, underfrequency_trips, label='Underfrequency Trip', color='b')
plt.axvline(50, color='g', linestyle='--', label='Nominal Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Trip Signal')
plt.title('Generator Frequency Protection')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(power_angles, out_of_step_trips, label='Out-of-Step Trip', color='m')
plt.axvline(120, color='black', linestyle='--', label='Out-of-Step Limit')
plt.xlabel('Power Angle (degrees)')
plt.ylabel('Trip Signal')
plt.title('Out-of-Step Protection')
plt.legend()
plt.grid()

plt.show()
