
export function AudioPlayer({ audioUrl }: { audioUrl: string | null }) {
    if (!audioUrl) {
      return (
        <div className="h-full flex items-center justify-center text-gray-500">
          Harmonized audio will appear here
        </div>
      );
    }
  
    return (
      <div>
        <audio controls className="w-full">
          <source src={audioUrl} type="audio/midi" />
          Your browser does not support the audio element.
        </audio>
      </div>
    );
  }
   