import { useEffect, useRef, useState } from "react";
import { Skeleton } from "@shared/components/ui/skeleton";

interface MicrofrontendLoaderProps {
  name: string;
  url: string;
}

export const MicrofrontendLoader = ({ name, url }: MicrofrontendLoaderProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMicrofrontend = async () => {
      try {
        setLoading(true);
        setError(null);

        // Create iframe for microfrontend
        const iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.style.width = '100%';
        iframe.style.height = '100vh';
        iframe.style.border = 'none';
        iframe.style.overflow = 'hidden';
        
        iframe.onload = () => {
          setLoading(false);
        };

        iframe.onerror = () => {
          setError(`Failed to load ${name} microfrontend`);
          setLoading(false);
        };

        if (containerRef.current) {
          containerRef.current.innerHTML = '';
          containerRef.current.appendChild(iframe);
        }
      } catch (err) {
        setError(`Error loading ${name}: ${err}`);
        setLoading(false);
      }
    };

    loadMicrofrontend();
  }, [name, url]);

  if (error) {
    return (
      <div className="flex items-center justify-center h-full p-8">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600 mb-2">Error Loading {name}</h2>
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-full">
      {loading && (
        <div className="absolute inset-0 flex flex-col space-y-4 p-6">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-4 w-96" />
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
          </div>
          <Skeleton className="h-64" />
        </div>
      )}
      <div ref={containerRef} className="h-full" />
    </div>
  );
};