"""
███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗██████╗ ██╗   ██╗
██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║██╔══██╗╚██╗ ██╔╝
███████╗ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║██████╔╝ ╚████╔╝ 
╚════██║  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║██╔═══╝   ╚██╔╝  
███████║   ██║   ██║ ╚████║   ██║   ██║  ██║██║        ██║   
╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝        ╚═╝                                                             
"""

# Imports
from pynput import keyboard
import pygame
import numpy as np
from random import uniform

# FUNCTIONS

# Function to generate a sine wave sound with ADSR envelope for the given frequency
def generate_sine_wave(frequency, duration=0.65, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = apply_adsr_envelope(wave, sample_rate)
    wave = np.int16(wave * 32767)  # Convert to 16-bit PCM
    stereo_wave = np.stack((wave, wave), axis=-1)  # Make it 2D for stereo
    return stereo_wave

# Function to apply ADSR envelope to a waveform
def apply_adsr_envelope(wave, sample_rate, attack=0.01, decay=0.1, sustain=0.4, release=0.005):
    total_samples = len(wave)
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples

    if sustain_samples < 0:
        raise ValueError("Duration is too short for the given ADSR parameters")

    attack_curve = np.linspace(0, 1, attack_samples)
    decay_curve = np.linspace(1, sustain, decay_samples)
    sustain_curve = np.ones(sustain_samples) * sustain
    release_curve = np.linspace(sustain, 0, release_samples)

    envelope = np.concatenate((attack_curve, decay_curve, sustain_curve, release_curve))
    return wave * envelope

# Function to play a sound
def play_sound(frequency):
    wave = generate_sine_wave(frequency)
    sound = pygame.sndarray.make_sound(wave)
    sound.play()


def on_press(key):
    try:
        if key.char != None:
            print(f'Alphanumeric key pressed: {key.char}')
            play_sound(ord(key.char) * uniform(1.5, 2.7))  # Play sound on key press
    except AttributeError:
        print(f'Special key pressed: {key}')

def on_release(key):
    print(f'Key released: {key}')
    if key == keyboard.Key.backspace:
        play_sound(250)

# EXECUTION
if __name__ == '__main__':
    # Initialize pygame mixer
    pygame.mixer.init(frequency=44100, size=-16, channels=2)  # Stereo sound
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()