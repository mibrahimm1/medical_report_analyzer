import React from 'react';

interface ResultGridProps {
    imageSrc: string;
}

export default function ResultGrid({ imageSrc }: ResultGridProps) {
    return (
        <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 flex flex-col items-center h-full">
            <h3 className="text-xl font-semibold text-white mb-6 self-start">Detected Anomalies</h3>
            <div className="relative w-full flex-1 flex items-center justify-center rounded-xl overflow-hidden border border-slate-600/50 bg-slate-800/50 p-2">
                <img src={imageSrc} alt="Annotated X-Ray" className="max-w-full max-h-[400px] object-contain rounded-lg shadow-2xl" />
            </div>
        </div>
    );
}
