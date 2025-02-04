import React, { useState, useRef } from 'react';
import { AlertCircle, Music, Settings, Play, Download } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const HarmonizerGUI = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [style, setStyle] = useState('pop');
  const [complexity, setComplexity] = useState('medium');
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && (file.name.endsWith('.mid') || file.name.endsWith('.musicxml'))) {
      setSelectedFile(file);
      setStatus('File loaded: ' + file.name);
    } else {
      setStatus('Please select a MIDI or MusicXML file');
    }
  };

  const handleHarmonize = async () => {
    if (!selectedFile) {
      setStatus('Please select a file first');
      return;
    }
    setIsProcessing(true);
    // Harmonization logic would go here
    setIsProcessing(false);
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center space-x-4 mb-8">
        <Music className="w-8 h-8 text-blue-500" />
        <h1 className="text-2xl font-bold">Melody Harmonizer</h1>
      </div>

      {/* File Input */}
      <div className="p-6 border rounded-lg bg-white shadow-sm">
        <div className="flex flex-col items-center gap-4">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
          >
            Select Melody File
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".mid,.musicxml"
            onChange={handleFileSelect}
            className="hidden"
          />
          {selectedFile && (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Selected File</AlertTitle>
              <AlertDescription>{selectedFile.name}</AlertDescription>
            </Alert>
          )}
        </div>
      </div>

      {/* Settings */}
      <div className="p-6 border rounded-lg bg-white shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <Settings className="w-5 h-5" />
          <h2 className="text-lg font-semibold">Harmonization Settings</h2>
        </div>
        
        <div className="grid gap-4">
          <div className="space-y-2">
            <label className="block text-sm font-medium">Style</label>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              className="w-full p-2 border rounded-md"
            >
              <option value="pop">Pop</option>
              <option value="jazz">Jazz</option>
              <option value="classical">Classical</option>
              <option value="blues">Blues</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium">Complexity</label>
            <select
              value={complexity}
              onChange={(e) => setComplexity(e.target.value)}
              className="w-full p-2 border rounded-md"
            >
              <option value="simple">Simple</option>
              <option value="medium">Medium</option>
              <option value="complex">Complex</option>
            </select>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={handleHarmonize}
          disabled={!selectedFile || isProcessing}
          className="flex-1 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Play className="w-4 h-4" />
          {isProcessing ? 'Processing...' : 'Harmonize'}
        </button>
        
        <button
          disabled={!selectedFile || isProcessing}
          className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Download className="w-4 h-4" />
          Download
        </button>
      </div>

      {/* Status */}
      {status && (
        <Alert>
          <AlertDescription>{status}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default HarmonizerGUI;