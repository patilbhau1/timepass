import pyttsx3

engine = pyttsx3.init()

# Get list of available voices
voices = engine.getProperty('voices')

# Set voice (adjust index as needed)
engine.setProperty('voice', voices[1].id)  # Example: voices[1] or voices[0]

# Adjust rate (speed) and volume
engine.setProperty('rate', 170)  # Adjust the speaking rate
engine.setProperty('volume', 1.0)  # Adjust the volume (0.0 to 1.0)

# Speak text
engine.say("Hello! I am your sweet and natural voice assistant.")
engine.runAndWait()
