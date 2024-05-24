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

# Function to generate a sine wave with enhanced bass
def generate_bassy_sine_wave(frequency, duration=0.65, sample_rate=44100, bassy = False):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = apply_adsr_envelope(wave, sample_rate)
    if bassy:
        wave = enhance_bass(wave, sample_rate)
    wave = np.int16(wave * 32767)  # Convert to 16-bit PCM
    stereo_wave = np.stack((wave, wave), axis=-1)  # Make it 2D for stereo
    print(stereo_wave)
    return stereo_wave * 3

# Function to apply a bass enhancement
def enhance_bass(wave, sample_rate, bass_boost_freq=20, bass_boost_gain=1.12):
    # Create a sub-bass sine wave
    t = np.linspace(0, len(wave) / sample_rate, len(wave), endpoint=False)
    sub_bass = np.sin(1.5 * np.pi * bass_boost_freq * t) * bass_boost_gain
    # Mix the sub-bass with the original wave
    enhanced_wave = wave + sub_bass
    # Normalize to prevent clipping
    max_amplitude = max(np.abs(enhanced_wave))
    if max_amplitude > 1:
        enhanced_wave /= max_amplitude
    print(enhanced_wave)
    return enhanced_wave

# Function to apply ADSR envelope to a waveform
def apply_adsr_envelope(wave, sample_rate, attack=0.5, decay=0.1, sustain=0.5, release=0.005):
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
    wave = generate_bassy_sine_wave(frequency)
    sound = pygame.sndarray.make_sound(wave)
    sound.play()

def on_press(key):
    try:
        if key.char != None:
            print(f'Alphanumeric key pressed: {key.char}')
            play_sound(ord(key.char) * uniform(0.2, 1.9))  # Play sound on key press
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