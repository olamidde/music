import numpy as np
from music21 import *


class MelodyHarmonizer:
    
    def __init__(self):
        
        self.common_progressions = {
            'major': ['I', 'IV', 'V', 'vi'],
            'minor': ['i', 'iv', 'v', 'vi'],
            'diminished': ['i', 'iv', 'vi'],
            'augmented': ['I', 'vi', 'V'],
            'whole': ['I', 'vi', 'V', 'vi'],
            'half': ['i', 'iv', 'vi', 'vi'],
            'diminished': ['i', 'iv', 'vi'],
            'augmented': ['I', 'vi', 'V'],
            'whole': ['I', 'vi', 'V', 'vi'],
            'half': ['i', 'iv', 'vi', 'vi'],
        }
        
        self.cord_structures = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'dominant': [0, 4, 7, 10]
        }
        
        # come back to this
        self.chord_quality = { 
                              }
        
    def analyze_melody(self, melody_stream):
        
        key = melody_stream.analyze('key')
         
        time_signature = melody_stream.getTimeSignature()[0]
        
        notes = melody_stream.flatten().notesAndRests
        
        return key, time_signature, notes

    def generate_harmony(self, melody_stream, style='simple'):
        
        key, time_sig, melody_notes = self.analyze_melody(melody_stream)
        
        harmony = stream.Stream()
        
        if key.mode == 'major':
            progression = self.common_progressions['major'][0]
        else:
            progression = self.common_progressions['minor'][0]
            
        current_measure = 0 
        chord = []
             
    def generate_chord(self, strings, ):
        
         
        pass
    
    
    def play(self): 
        pass
    