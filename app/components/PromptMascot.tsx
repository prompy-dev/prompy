'use client';

import Image from 'next/image';

interface PromptMascotProps {
  isAnimating?: boolean;
}

export function PromptMascot({ isAnimating = false }: PromptMascotProps) {

  return (
    <div className="relative w-25 h-25">
      {/* Mascot placeholder - this will be replaced with an actual image */}
      {/* <div
        className={`
          w-24 h-24 bg-[#61dcfb] rounded-full flex items-center justify-center
          ${isAnimating ? 'animate-pulse' : ''}
          transition-all duration-300 ease-in-out
          shadow-lg hover:shadow-xl
        `}
      > */}
        <Image
          src="/prompy.svg"
          alt="Prompy Logo"
          width={200}
          height={200}
        />
      {/* </div> */}

      {/* Dots for thinking animation */}
      {isAnimating && (
        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-1">
          <div
            className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
            style={{ animationDelay: '0ms' }}
          ></div>
          <div
            className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
            style={{ animationDelay: '300ms' }}
          ></div>
          <div
            className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
            style={{ animationDelay: '600ms' }}
          ></div>
        </div>
      )}
    </div>
  );
}