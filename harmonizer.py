import numpy as np
from music21 import *
import tkinter as tk
from tkinter, import ttk, filedialog

class MelodyHarmonizer:
    def __init__(self):
        # Define common chord progressions in different keys
        self.style_progressions= {
            'major': [
                ['I', 'IV', 'V', 'I'],
                ['I', 'vi', 'IV', 'V'],
                ['I', 'V', 'vi', 'IV']
            ],
            'minor': [
                ['i', 'iv', 'V', 'i'],
                ['i', 'VI', 'III', 'V'],
                ['i', 'iv', 'v', 'i']
            ]
        }
        
        self.chord_structures = {
            'major': [0, 4, 7],      # Major triad
            'minor': [0, 3, 7],      # Minor triad
            'dominant': [0, 4, 7, 10] # Dominant seventh
        }

    def analyze_melody(self, melody_stream):
        """Analyze the given melody to determine key and important features"""
        key = melody_stream.analyze('key')
        
        time_sig = melody_stream.getTimeSignatures()[0]
        
        notes = melody_stream.flatten().notesAndRests
        
        return key, time_sig, notes

    def generate_harmony(self, melody_stream, style='simple'):
        """Generate harmony for the given melody"""
        # Analyze melody
        key, time_sig, melody_notes = self.analyze_melody(melody_stream)
        
        # Create a new stream for harmony
        harmony = stream.Stream()
        
        # Determine appropriate chord progression
        if key.mode == 'major':
            progression = self.common_progressions['major'][0]  # Use first progression for now
        else:
            progression = self.common_progressions['minor'][0]
        
        # Generate chords based on melody notes and progression
        current_measure = 0
        chords = []
        
        for note in melody_notes:
            if isinstance(note, note.Note):
                # Find suitable chord from progression
                chord = self._find_suitable_chord(note, key, progression[current_measure % len(progression)])
                chords.append(chord)
            else:
                # For rests, continue previous chord or add rest
                chords.append(note.Rest())
                
            current_measure = len(chords) // time_sig.numerator
        
        # Add chords to harmony stream
        for chord in chords:
            harmony.append(chord)
        
        return harmony

    def _find_suitable_chord(self, melody_note, key, chord_roman):
        """Find a suitable chord that contains or complements the melody note"""
        # Convert Roman numeral to chord
        chord_obj = roman.RomanNumeral(chord_roman, key)
        
        # Get base chord notes
        chord_notes = chord_obj.pitches
        
        # If melody note is in chord, return chord as is
        if melody_note.pitch in chord_notes:
            return chord_obj
        
        # Otherwise, create modified chord that works with melody note
        modified_chord = self._modify_chord_for_melody(chord_obj, melody_note)
        return modified_chord

    def _modify_chord_for_melody(self, chord, melody_note):
        """Modify chord to better fit with melody note"""
        # Get chord notes
        chord_notes = list(chord.pitches)
        
        # If melody note is within one step of any chord note, use seventh chord
        for note in chord_notes:
            if abs(interval.Interval(note, melody_note.pitch).semitones) <= 2:
                # Add seventh if not already present
                if len(chord_notes) == 3:  # triad
                    seventh = chord_notes[0].transpose(10)  # add dominant seventh
                    chord_notes.append(seventh)
                    return chord.Chord(chord_notes)
        
        return chord

    def create_midi(self, melody, harmony, output_file='harmonized_melody.mid'):
        """Combine melody and harmony into MIDI file"""
        combined = stream.Score()
        combined.append(melody)
        combined.append(harmony)
        combined.write('midi', fp=output_file)

# Example usage
def harmonize_melody(melody_file):
    # Load melody from MIDI file
    melody = converter.parse(melody_file)
    
    # Create harmonizer instance
    harmonizer = MelodyHarmonizer()
    
    # Generate harmony
    harmony = harmonizer.generate_harmony(melody)
    
    # Create output MIDI file
    harmonizer.create_midi(melody, harmony)
    
    return melody, harmony