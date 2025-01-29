from typing import List, Dict, Optional
from music21 import stream, converter
from ..utils.music_theory import get_key_signature
from ..styles.progressions import get_style_progression
from .analysis import MelodyAnalyzer
from .voicing import VoicingGenerator

class MelodyHarmonizer:
    """Main harmonizer class that coordinates the harmonization process."""
    
    def __init__(self):
        self.analyzer = MelodyAnalyzer()
        self.voicing_generator = VoicingGenerator()
        
    def harmonize(self, 
                 melody_path: str, 
                 style: str = 'pop',
                 complexity: str = 'medium',
                 output_path: Optional[str] = None) -> stream.Score:
        """
        Harmonize a given melody file.
        
        Args:
            melody_path: Path to the input melody file
            style: Harmonization style ('pop', 'jazz', 'classical', 'blues')
            complexity: Harmonization complexity ('simple', 'medium', 'complex')
            output_path: Optional path to save the output file
            
        Returns:
            music21.stream.Score object containing the harmonized piece
        """
        # Load and analyze melody
        melody = converter.parse(melody_path)
        analysis = self.analyzer.analyze_melody(melody)
        
        # Get style-specific progression
        progression = get_style_progression(style, analysis.key)
        
        # Generate initial harmony
        harmony = self._generate_harmony(analysis, progression, complexity)
        
        # Apply voicing based on style
        voiced_harmony = self.voicing_generator.apply_voicing(harmony, style)
        
        # Combine melody and harmony
        score = self._create_score(melody, voiced_harmony)
        
        # Save if output path is provided
        if output_path:
            score.write('midi', fp=output_path)
        return score
    
    def _generate_harmony(self, 
                         analysis: 'MelodyAnalysis',
                         progression: List[str],
                         complexity: str) -> stream.Stream:
        """Generate initial harmony based on analysis and style."""
        harmony = stream.Stream()
        
        # Implementation varies based on complexity
        if complexity == 'simple':
            # Generate basic chord progression
            harmony = self._generate_simple_harmony(analysis, progression)
        elif complexity == 'medium':
            # Add passing chords and basic variations
            harmony = self._generate_medium_harmony(analysis, progression)
        else:  # complex
            # Add advanced harmonization techniques
            harmony = self._generate_complex_harmony(analysis, progression)
            
        return harmony
    
    def _create_score(self, 
                     melody: stream.Stream,
                     harmony: stream.Stream) -> stream.Score:
        """Combine melody and harmony into a single score."""
        score = stream.Score()
        
        # Create melody part
        melody_part = stream.Part()
        melody_part.append(melody.flatten())
        
        # Create harmony part
        harmony_part = stream.Part()
        harmony_part.append(harmony)
        
        # Add both parts to score
        score.append(melody_part)
        score.append(harmony_part)
        
        return score
    
    def _generate_simple_note()