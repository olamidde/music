import numpy as np
from music21 import stream, note, meter, key, roman
import tkinter as tk
from dataclass import dataclass
from typing import List, Tuple, Dict

@dataclass
class MelodyAnalysis:
    key: key.Key
    time_signature: meter.TimeSignature
    phrases: List[List[note.Note]]
    rhythm_patterns: List[List[float]]
    contour: List[int]
    peak_notes: List[note.Note]
    cadences: List[Tuple[note.Note, str]]  # (note, cadence_type)
    tension_points: List[Tuple[note.Note, float]]  # (note, tension_value)
    style_features: Dict[str, float]  # Style-specific analysis scores

class MelodyAnalyzer:
    def __init__(self):
        # Define common chord progressions in different keys
        self.style_progressions = {
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
        
        key_sig = self._get_key(melody)
        time_sig = self._get_time_signature(melody)
        
        notes = melody.flatten().notesAndRests
        phrases = self._detect_phrases(notes)
        rhythm_patterns = self._analyze_rhythm(notes)
        contour = self._analyze_contour(notes)
        peak_notes = self._detect_peak_notes(notes)
        cadences = self._detect_cadences(notes, key_sig)
        tension_points = self._analyze_tension(notes, key_sig)
        style_features = self._analyze_style_features(notes, rhythm_patterns)
        
        return MelodyAnalysis(
            key_sig, time_sig, phrases, rhythm_patterns, 
            contour, peak_notes, cadences, tension_points, style_features
        )

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
            progression = self.style_progressions['major'][0]  # Use first progression for now
        else:
            progression = self.style_progressions['minor'][0]
        
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

    def _detect_phrases(self, notes: List[note.Note]) -> List[List[note.Note]]:
        """Detect musical phrases using breathing points and melodic patterns."""
        phrases = []
        current_phrase = []
        
        for i, note in enumerate(notes):
            current_phrase.append(note)
            
            # Check for phrase endings based on multiple criteria
            if (i < len(notes) - 1 and
                (self._is_breathing_point(note, notes[i + 1]) or
                 self._is_cadential_pattern(current_phrase) or
                 len(current_phrase) > 8)):  # Max phrase length
                
                phrases.append(current_phrase)
                current_phrase = []
        
        if current_phrase:
            phrases.append(current_phrase)
        
        return phrases

    def _detect_cadences(self, notes: List[note.Note], key: key.Key) -> List[Tuple[note.Note, str]]:
        """Identify different types of cadences in the melody."""
        cadences = []
        
        for i in range(len(notes) - 1):
            current_note = notes[i]
            next_note = notes[i + 1]
            
            # Perfect Authentic Cadence (ending on tonic)
            if next_note.pitch.name == key.tonic.name:
                if current_note.pitch.name == key.dominantHarmonic.name:
                    cadences.append((next_note, 'PAC'))
                    
            # Half Cadence (ending on dominant)
            elif next_note.pitch.name == key.dominantHarmonic.name:
                cadences.append((next_note, 'HC'))
                
            # Deceptive Cadence (V to vi)
            elif (current_note.pitch.name == key.dominantHarmonic.name and
                  next_note.pitch.name == key.getRelativeMinor().tonic.name):
                cadences.append((next_note, 'DC'))
        
        return cadences

    def _analyze_tension(self, notes: List[note.Note], key: key.Key) -> List[Tuple[note.Note, float]]:
        """Analyze melodic tension based on intervals and harmony."""
        tension_points = []
        scale_degrees = key.getScale()
        
        for i, note in enumerate(notes):
            tension = 0.0
            
            # Add tension for non-scale tones
            if note.pitch not in scale_degrees:
                tension += 0.5
                
            # Add tension for large intervals
            if i > 0:
                interval = abs(note.pitch.ps - notes[i-1].pitch.ps)
                tension += interval / 12.0  # Normalize by octave
                
            # Add tension for high register notes
            tension += (note.pitch.ps - 60) / 24.0  # Normalize around middle C
            
            tension_points.append((note, min(1.0, tension)))  # Cap tension at 1.0
            
        return tension_points

    def _analyze_style_features(self, notes: List[note.Note], rhythm_patterns: List[List[float]]) -> Dict[str, float]:
        """Analyze style-specific features of the melody."""
        features = {}
        
        # Rhythmic complexity
        unique_patterns = len(set(tuple(p) for p in rhythm_patterns))
        features['rhythmic_complexity'] = min(1.0, unique_patterns / 10.0)
        
        # Melodic range
        pitches = [n.pitch.ps for n in notes if isinstance(n, note.Note)]
        pitch_range = max(pitches) - min(pitches)
        features['pitch_range'] = min(1.0, pitch_range / 24.0)  # Normalize to 2 octaves
        
        # Syncopation
        syncopated_notes = sum(1 for n in notes if self._is_syncopated(n))
        features['syncopation'] = min(1.0, syncopated_notes / len(notes))
        
        return features

    def _is_breathing_point(self, current: note.Note, next_note: note.Note) -> bool:
        """Detect natural breathing points in the melody."""
        if isinstance(current, note.Rest) or isinstance(next_note, note.Rest):
            return True
            
        # Check for longer duration followed by shorter one
        if current.duration.quarterLength > next_note.duration.quarterLength * 2:
            return True
            
        # Check for descending interval larger than a fifth
        if (isinstance(current, note.Note) and isinstance(next_note, note.Note) and
            current.pitch.ps - next_note.pitch.ps > 7):
            return True
            
        return False

    def _is_cadential_pattern(self, phrase: List[note.Note]) -> bool:
        """Detect if a phrase ends with a typical cadential pattern."""
        if len(phrase) < 3:
            return False
            
        # Look for typical rhythmic patterns at phrase endings
        last_three = phrase[-3:]
        durations = [n.duration.quarterLength for n in last_three]
        
        # Common cadential rhythm patterns
        cadential_patterns = [
            [1.0, 1.0, 2.0],  # Short-short-long
            [0.5, 0.5, 2.0],  # Shorter-shorter-long
            [1.0, 2.0, 2.0],  # Short-long-long
        ]
        
        return any(self._is_similar_rhythm(durations, pattern) for pattern in cadential_patterns)

    def _is_similar_rhythm(self, rhythm1: List[float], rhythm2: List[float], threshold: float = 0.1) -> bool:
        """Compare two rhythm patterns for similarity."""
        if len(rhythm1) != len(rhythm2):
            return False
            
        return all(abs(r1 - r2) < threshold for r1, r2 in zip(rhythm1, rhythm2))

    def _is_syncopated(self, note_obj: note.Note) -> bool:
        """Detect if a note is syncopated."""
        if not hasattr(note_obj, 'beat'):
            return False
            
        # Check if note starts on a weak beat
        beat = note_obj.beat
        return beat % 1 != 0 and note_obj.duration.quarterLength >= 1.0

# Example usage
def harmonize_melody(melody_file):
    # Load melody from MIDI file
    melody = converter.parse(melody_file)
    
    # Create harmonizer instance
    harmonizer = MelodyAnalyzer()
    
    # Generate harmony
    harmony = harmonizer.generate_harmony(melody)
    
    # Create output MIDI file
    harmonizer.create_midi(melody, harmony)
    
    return melody, harmony