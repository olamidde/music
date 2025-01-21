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
        
    def generate_voicing(self, chord_type: str, config: VoicingConfig) -> List[chord.Chord]:
        """Generate voicings for a given chord type."""
        pass