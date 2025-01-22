from typing import List, Dict, Optional, Tuple
from music21 import chord, note, pitch, interval
from dataclasses import dataclass
import logging 

@dataclass
class VoicingConfig:
    """Configuration for chord voicing."""
    voicing_style: str = 'default'
    voicing_complexity: str = 'simple'
    voicing_range: str = 'C3-C5'
    voicing_root: str = 'C'
    voicing_mode: str = 'major'
    voicing_inversion: int = 0
    voicing_bass: bool = False
    voicing_bass_octave: int = 3
    max_spacing: int = 12
    min_spaciing: int = 2
    preferred_range : Tuple[int, int] = (48, 72) #MIDI Note range (C3 - C5)
    preferred_bass_range: Tuple[int, int] = (36, 48)
    voice_crossing: bool = False
    parallel_threshold: float = 0.8 


class VoicingGenerator: 
    "Handles Generation of Chord Voicings based on different styles"
    
    def __init__(self):
        self.style_configs = {
            'pop': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = False),
            'jazz': VoicingConfig(max_spacing = 10, min_spacing = 2, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
            'rock': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
            'classical': VoicingConfig(max_spacing = 16, min_spacing = 2, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = False),
            'blues': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
            'country': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
            'latin': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
            'hiphop': VoicingConfig(max_spacing = 12, min_spacing = 3, preferred_range = (48, 72), preferred_bass_range = (36, 48), voice_crossing = True),
        }
        
        # defining the chord extensions for each style
        self.style_extensions = {
            'pop': {'major': [], 'minor': [], 'dominant': [7]},
            'jazz': {'major': [11], 'minor': [10], 'dominant': [7, 11]},
            'classical': {'major': [], 'minor': [], 'dominant': []},
            'blues': {'major': [7], 'minor': [7], 'dominant': [7, 9]},
        }
        
    
    def apply_voicing(self, chord_type: List[chord.Chord], style: str = 'pop', melody: List[note.Note] = None) -> List[chord.Chord]:
        """Apply voicing to a list of chords."""
        config = self.style_confights[style]
        voiced_chords = []
        prev_chord = None
        
        for i, current_chord in enumerate(chord_type):
            melody_note = melody_notes[i] if melody_notes else None
            
            chord_type = self.determine_chord_type(current_chord)
            extended_cord = self.add_extensions(current_chord, chord_type, style)
            
            voiced_chord = self.generate_voicing(extended_cord, config, melody_note)
            
            # apply voice leading if there is a previous chord 
            if prev_chord:
                voiced_chord = self.apply_voice_leading(prev_chord, voiced_chord, config)
            
            voiced_chords.append(voiced_chord)
            previous_chord = voiced_chord
            
        return voiced_chords
    
    def generate_voicing(self, chord_type: str, config: VoicingConfig) -> List[chord.Chord]:
        """Generate voicings for a given chord type."""
        pass
    
    def determine_chord_type(self, ch: chord.Chord) -> str:
        """Determine the chord type from a chord object."""
        
        if ch.isMajorTriad():
            return 'major'
        elif ch.isMinorTriad():
            return 'minor'
        elif ch.isDominantSeventh():
            return 'dominant'
        else:
            return 'major'
        
    def add_extensions(self, ch: chord.Chord, chord_type : str, style : str) -> chord.Chord:
        extensions = self.style_extensions[style][chord_type]
        base_notes =  [p.midi for p in ch.pitches]
        root = base_notes[0]
        
        for ext in extensions:
            if ext == 7:
                seventh = root + (10 if chord_type == 'dominant' else 11)
                if seventh not in base_notes: 
                    ch.add(pitch.Pitch(midi = seventh))
            elif ext == 9:
                ninth = root + (14 if chord_type == 'dominant' else 13)
                if ninth not in base_notes:
                    ch.add(pitch.Pitch(midi = ninth))
            elif ext == 13:
                thirteenth = root + 21
                if thirteenth not in base_notes:
                    ch.add(pitch.Pitch(midi = thirteenth))
                    
        return ch
    
    def generate_voicing(self, ch: chord.Chord, config: VoicingConfig, melody_note: Optional[note.Note] = None) -> chord.Chord:
        "Generate initial voicing for chord"
        
        root = ch.root()
        while root.midi < config.preferred_range[0]:
            root.octave +=1
        while root.midi > config.preferred_range[1]:
            root.octave -=1
        

        voiced_notes = [root]
        remaining_notes = sorted([p for p in ch.pitches if p.name != root.name], key=lambda p: p.midi)
        
        # add the remaining notes to the voicing, making sure they are in the correct octave
        for note_to_add in remaining_notes:
            best_octave = self.find_best_octave(note_to_add, voiced_notes[-1], config)
            note_to_add.octave = best_octave
            voiced_notes.append(note_to_add)
        
        # if the melody note is provided, we need to adjust the voicing to fit the melody note by making sure its the highest note in the chord
        if melody_note:
            while voiced_notes[-1].midi < melody_note.pitch.midi:
                voiced_notes[-1].octave -= 1
        return chord.Chord(voiced_notes)
    
    def find_best_octave(self, note_to_add: pitch.Pitch, prev_note: pitch.Pith, config: VoicingConfig) -> int:
        
        curr_octave = prev_note.octave
        interval_semitones = interval.Interval(prev_note, note_to_add).semitones
        
        while interval_semitones < config.min_spacing:
            curr_octave += 1
            interval_semitones += 12
        
        while interval_semitones > config.max_spacing:
            curr_octave -= 1
            interval_semitones -= 12
            
        return curr_octave

    def apply_voice_leading(self, prev_chord: chord.Chord, current_chord: chord.Chord, config: VoicingConfig) -> chord.Chord:
        """Apply voice leading to the current chord based on the previous chord."""
        pass
    
    def fix_parallel_motion(self, prev_chord : chord.Chord, curr_chord: chord.Chord) -> chord.Chord:
        
        "Adjust voicing to avoid parallell motion"

        for i in range(1, len(curr_chord.pitches)):
            original_pitch = curr_chord.pitches[i].midi 
            
            for step in [-2, -1, 1, 2]:
                curr_chord.pitches[i].midi = original_pitch + step
                if not self.is_parallel_motion(prev_chord.pitches[i], original_pitch):
                    return curr_chord
            
            curr_chord.pitches[i].midi = original_pitch
        
        return curr_chord
    
    def minimize_voice_movement(self, prev_chord : chord.Chord, curr_chord: chord.Chord, config: VoicingConfig) -> chord.Chord:
        """ Minimize movement between voices in consecutive chords"""
        
        for i in range(len(curr_chord.pitches)):
            curr_pitch = curr_chord.pitches[i]
            target_pitch = prev_chord.pitches[i]
            
            while abs(curr_pitch - target_pitch) > 6:
                if curr_pitch < target_pitch:
                    curr_pitch += 12
                else:
                    curr_pitch -= 12
            
            if i > 0:
                prev_voice = curr_chord.pitches[i - 1]
                if curr_pitch - prev_voice < config.min_spacing:
                    break
            if i < len(curr_chord.pitches) - 1:
                next_voice = curr_chord[i + 1].midi
                if next_voice - curr_pitch < config.min_spacing:
                    break 
            
            curr_chord.pitches[i].midi = curr_pitch
                   
        return curr_chord             