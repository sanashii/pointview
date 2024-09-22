import pyttsx3
import winsound

# Sound alert using a predefined beep sound
frequency = 1000  # Set Frequency To 1000 Hertz
duration = 1000   # Set Duration To 3000 ms == 3 seconds

def say_alert(message, speed=150):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Beep sound alert
    winsound.Beep(frequency, duration)

    # Set properties
    engine.setProperty('rate', speed)  # Speed (higher is faster)
    engine.setProperty('volume', 1)     # Volume (0.0 to 1.0)

    # Speak the message
    engine.say(message)

    # Wait for the speech to finish
    engine.runAndWait()

# Call the function with your alert message and desired speed
say_alert("Program is finished running", speed=150)  # Adjust speed as needed

