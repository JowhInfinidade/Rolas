import parselmouth
from parselmouth.praat import call
import os
from os.path import exists
import random

# Function to generate the chromatic scale
def generate_chromatic(sample_path, semitones, gap, starting_note, starting_octave, pitched, randomize, dump_samples):
    sample_gap = call("Create Sound from formula", "Gap", 1, 0, float(gap), 48000, "0")
    file_index = 0

    while exists(sample_path + os.sep + str(file_index + 1) + ".wav"):
        file_index += 1

    pitched_sounds = []
    spaced_pitched_sounds = []

    for i in range(semitones):
        starting_key = starting_note + 12 * (starting_octave - 2)

        if not randomize:
            current_sound = call(call(parselmouth.Sound(sample_path + os.sep + str(i % (file_index) + 1) + ".wav"), "Resample", 48000, 1), "Convert to mono")
        else:
            current_sound = call(call(parselmouth.Sound(sample_path + os.sep + str(random.randint(1, file_index)) + ".wav"), "Resample", 48000, 1), "Convert to mono")
        print(current_sound)

        if pitched:
            manipulation = call(current_sound, "To Manipulation", 0.05, 60, 600)
            pitch_tier = call(manipulation, "Extract pitch tier")
            call(pitch_tier, "Formula", f"32.703 * (2 ^ ({i + starting_key + 12}/12))")
            call([pitch_tier, manipulation], "Replace pitch tier")
            pitched_sounds.append(call(manipulation, "Get resynthesis (overlap-add)"))
            spaced_pitched_sounds.append(call(manipulation, "Get resynthesis (overlap-add)"))
        else:
            pitched_sounds.append(current_sound)
            spaced_pitched_sounds.append(current_sound)

        spaced_pitched_sounds.append(sample_gap)

    chromatic = parselmouth.Sound.concatenate(spaced_pitched_sounds)
    chromatic.save(sample_path + os.sep + "chromatic.wav", "WAV")

    if dump_samples and pitched:
        if not os.path.exists(sample_path + os.sep + "pitched_samples"):
            os.makedirs(sample_path + os.sep + "pitched_samples")
        for pitched_sound in pitched_sounds:
            pitched_sound.save(sample_path + os.sep + "pitched_samples" + os.sep + f"pitched_{1 + pitched_sounds.index(pitched_sound)}.wav", "WAV")

# Main function to interact with the user
def main():
    sample_path = input("Enter the path to the sample folder: ")
    semitones = int(input("Enter the range (in semitones): "))
    gap = float(input("Enter the sample gap (in seconds): "))
    starting_note = int(input("Enter the starting note (C=0, C#=1, ..., B=11): "))
    starting_octave = int(input("Enter the starting octave (-1 to 7): "))
    pitched = input("Should the samples be pitched? (yes/no): ").lower() == 'yes'
    randomize = input("Should the samples be randomized? (yes/no): ").lower() == 'yes'
    dump_samples = input("Should the pitched samples be saved? (yes/no): ").lower() == 'yes'

    generate_chromatic(sample_path, semitones, gap, starting_note, starting_octave, pitched, randomize, dump_samples)
    print("Chromatic scale generated!")

if __name__ == '__main__':
    main()
