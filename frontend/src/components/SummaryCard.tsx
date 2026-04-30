import React from 'react';

interface SummaryCardProps {
    summary: string;
}

export default function SummaryCard({ summary }: SummaryCardProps) {
    return (
        <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 flex flex-col h-full">
            <h3 className="text-xl font-semibold text-white mb-6">Patient-Friendly Explanation</h3>
            <div className="flex-1 overflow-y-auto pr-2">
                <p className="text-slate-200 leading-relaxed whitespace-pre-line text-lg font-light">
                    {summary}
                </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-700/50">
                <p className="text-xs text-slate-400 text-center uppercase tracking-wider font-semibold">
                    Disclaimer: AI Generated. Please consult a physician for medical advice.
                </p>
            </div>
        </div>
    );
}
