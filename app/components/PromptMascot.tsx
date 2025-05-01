"use client";

import Image from "next/image";

interface PromptMascotProps {
	isAnimating?: boolean;
}

export function PromptMascot({ isAnimating = false }: PromptMascotProps) {
	const imgSrc = isAnimating ? "/prompy_thinking.svg" : "/prompy_basic.svg";

	return (
		<div className="relative w-25 h-25">
			<Image
				src={imgSrc}
				alt="Prompy Logo"
				width={200}
				height={200}
				priority={true}
				className={`
            ${isAnimating ? "animate-rotate" : ""}
          `}
			/>

			{/* Dots for thinking animation */}
			{isAnimating && (
				<div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-1">
					<div
						className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
						style={{ animationDelay: "0ms" }}
					></div>
					<div
						className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
						style={{ animationDelay: "300ms" }}
					></div>
					<div
						className="w-2 h-2 bg-[#61dcfb] rounded-full animate-bounce"
						style={{ animationDelay: "600ms" }}
					></div>
				</div>
			)}
		</div>
	);
}
