import numpy as np
from music21 import stream, note, meter, key
import tkinter as tk
from dataclass import dataclass
from typing import List, Tuple

@dataclass
class MelodyAnalysis:
    key: key.key
    time_signature : meter.TimeSignature
    phrases : List[List[note.Note]]
    rhythm_patterns: List[List[float]]
    contour: List[int]
    peak_notes: List[note.Note]
    
class MelodyAnalayzer:
    def __init__(self):
        # Define common chord progressions in different keys
        self.
        +69-0style_-.39655+.
        .3
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        progressions= {
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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

    def analyze_melody(self, melody: stream.Stream) -> MelodyAnalysis:
        
        """Perform comprehensive analysis of the melody"""
        
        key_sig = self.get_key(melody)
        time_sig = self.get_time_signature(melody)
        
        
        notes = melody.flatten().notesAndRests
        phrases = self.detect_phrases(notes)
        rhythm_patterns = self.analyze_rhythm(notes)
        countour = self.analyze_contour(notes)
        peak_notes = self.detect_peak_notes(notes)
        
        return MelodyAnalysis(key_sig, time_sig, phrases, rhythm_patterns, countour, peak_notes)
    
    
    def _get_key(self, melody: stream.Stream) -> key.Key:
        return melody.analyze('key')
    
    def _get_time_signature(self, melody: stream.Stream) -> meter.TimeSignature:
        time_sigs = melody.getTimeSignatures()
        return time_sigs[0] if time_sigs else meter.TimeSignature
        
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