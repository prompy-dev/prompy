"use client";

import { CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import Image from "next/image";
import { Button } from "./ui/button";
import { ArrowLeft } from "lucide-react";
import { ChatResponse } from "@/lib/types";

interface ScorePanelHeaderProps {
	feedback: ChatResponse;
	onBack?: () => void;
}

export function ScorePanelHeader({ feedback, onBack }: ScorePanelHeaderProps) {
	// Score colors
	const getScoreColor = (score: number) => {
		if (score >= 8) return "text-green-500";
		if (score >= 6) return "text-blue-500";
		if (score >= 4) return "text-amber-500";
		return "text-rose-500";
	};

	// Score description
	const getScoreDescription = (score: number) => {
		if (score >= 10) return "Perfect!";
		if (score >= 8) return "Wow!";
		if (score >= 6) return "Nice!";
		if (score >= 4) return "Getting there...";
		return "Meh...";
	};

	return (
		<CardHeader className="w-full flex-row">
			<div className="flex flex-col flex-1 justify-between">
				<CardTitle className="text-3xl font-walter-turncoat pr-0 leading-none">
					Prompy's Score
				</CardTitle>
				{onBack && (
					<Button
						onClick={onBack}
						className="absolute top-2 right-2 md:hidden text-[10px] px-2 py-1 h-6 bg-[#61dcfb] hover:bg-[#61dcfb]/90 text-white font-walter-turncoat"
					>
						<ArrowLeft className="ml-1 h-3 w-3" />
						New Prompt
					</Button>
				)}
				<div className="w-full flex items-center">
					<div className="w-full">
						<div className="flex items-baseline justify-between">
							<span
								className={`text-2xl font-bold ${getScoreColor(
									feedback.score,
								)}`}
							>
								{feedback.score}/10
							</span>
						</div>
						<Progress
							value={feedback.score * 10}
							className={`h-5 bg-secondary`}
							indicatorClassName={
								feedback.score >= 8
									? "bg-green-500"
									: feedback.score >= 6
										? "bg-blue-500"
										: feedback.score >= 4
											? "bg-amber-500"
											: "bg-rose-500"
							}
						/>
					</div>
				</div>
			</div>
			<div className="flex flex-col self-center flex-1 items-center">
				<Image
					src="/prompy_basic.svg"
					alt="Prompy Logo"
					width={100}
					height={100}
				/>
				<span className="text-xl font-bold text-center font-walter-turncoat">
					{getScoreDescription(feedback.score)}
				</span>
			</div>
		</CardHeader>
	);
}
