// components/harmonizer-form.tsx
import { useState } from 'react';

interface HarmonizerSettings {
  style: 'pop' | 'jazz' | 'classical' | 'blues';
  complexity: 'simple' | 'medium' | 'complex';
}

export function HarmonizerForm({ 
  isEnabled,
  onHarmonize 
}: { 
  isEnabled: boolean;
  onHarmonize: (settings: HarmonizerSettings) => void;
}) {
  const [settings, setSettings] = useState<HarmonizerSettings>({
    style: 'pop',
    complexity: 'medium'
  });

  return (
    <form 
      onSubmit={(e) => {
        e.preventDefault();
        onHarmonize(settings);
      }}
      className="space-y-4"
    >
      <div>
        <label className="block text-sm font-medium mb-1">Style</label>
        <select
          value={settings.style}
          onChange={(e) => setSettings(s => ({ ...s, style: e.target.value as HarmonizerSettings['style'] }))}
          className="w-full p-2 border rounded"
        >
          <option value="pop">Pop</option>
          <option value="jazz">Jazz</option>
          <option value="classical">Classical</option>
          <option value="blues">Blues</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Complexity</label>
        <select
          value={settings.complexity}
          onChange={(e) => setSettings(s => ({ ...s, complexity: e.target.value as HarmonizerSettings['complexity'] }))}
          className="w-full p-2 border rounded"
        >
          <option value="simple">Simple</option>
          <option value="medium">Medium</option>
          <option value="complex">Complex</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={!isEnabled}
        className="w-full bg-blue-500 text-white py-2 rounded disabled:opacity-50"
      >
        Harmonize
      </button>
    </form>
  );
}