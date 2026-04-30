'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UploadBox from '@/components/UploadBox';
import Loader from '@/components/Loader';
import VisionWorkspace from '@/components/VisionWorkspace';
import IntelligenceWorkspace from '@/components/IntelligenceWorkspace';

interface AnalysisResponse {
    annotated_image: string;
    summary: string;
    detections: any[];
    raw_report: {
        findings: string;
        impression: string;
    };
}

export default function Home() {
    const [imageFile, setImageFile] = useState<File | null>(null);
    const [reportFile, setReportFile] = useState<File | null>(null);
    const [status, setStatus] = useState<'idle' | 'loading' | 'result'>('idle');
    const [result, setResult] = useState<AnalysisResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async () => {
        if (!imageFile || !reportFile) {
            setError("Please upload both an X-Ray image and a clinical report.");
            return;
        }

        setError(null);
        setStatus('loading');

        const formData = new FormData();
        formData.append("image", imageFile);
        formData.append("report", reportFile);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/api/analyze`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Failed to analyze data.");
            }

            const data = await response.json();
            setResult(data);
            setStatus('result');
        } catch (err: any) {
            console.error(err);
            setError(err.message || "An error occurred during analysis.");
            setStatus('idle');
        }
    };

    const handleReset = () => {
        setImageFile(null);
        setReportFile(null);
        setResult(null);
        setError(null);
        setStatus('idle');
    };

    return (
        <div className="overflow-x-hidden">
            <main className="min-h-[100vh] p-6 md:p-8 lg:p-12 flex flex-col items-center">
                <div className="max-w-[1400px] w-full flex flex-col gap-8 h-full">
                    <header className="text-center mb-4">
                        <h1 className="text-4xl md:text-5xl font-medium tracking-tight text-primary mb-4 drop-shadow-sm leading-tight">
                            Multimodal Medical Report Analyzer
                        </h1>
                        <p className="text-slate-400 text-lg md:text-xl max-w-3xl mx-auto font-light leading-relaxed">
                            Upload a Chest X-Ray and a clinical report to begin.
                        </p>
                    </header>

                    <AnimatePresence mode="wait">
                        {error && (
                            <motion.div 
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                className="bg-red-500/10 border border-red-500/50 text-red-400 px-6 py-4 rounded-xl backdrop-blur-md font-medium text-center shadow-lg w-full max-w-3xl mx-auto"
                            >
                                {error}
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <AnimatePresence mode="wait">
                        {status === 'idle' && (
                            <motion.div 
                                key="idle"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{ duration: 0.4 }}
                                className="flex flex-col items-center gap-10 w-full max-w-4xl mx-auto"
                            >
                                <UploadBox 
                                    onImageSelect={setImageFile} 
                                    onReportSelect={setReportFile}
                                    imageFile={imageFile}
                                    reportFile={reportFile}
                                />
                                <button 
                                    onClick={handleAnalyze}
                                    disabled={!imageFile || !reportFile}
                                    className="px-10 py-4 bg-primary hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed rounded-full text-slate-900 font-medium text-xl shadow-lg shadow-primary/25 transition-all transform hover:scale-105 active:scale-95"
                                >
                                    Analyze Now
                                </button>
                            </motion.div>
                        )}

                        {status === 'loading' && (
                            <motion.div 
                                key="loading"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="flex justify-center w-full max-w-xl mx-auto"
                            >
                                <Loader />
                            </motion.div>
                        )}

                        {status === 'result' && result && (
                            <motion.div 
                                key="result"
                                initial={{ opacity: 0, y: 40 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.7, ease: "easeOut" }}
                                className="flex flex-col gap-8 w-full flex-1"
                            >
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full min-h-[600px]">
                                    <VisionWorkspace 
                                        originalImageFile={imageFile} 
                                        annotatedImageBase64={result.annotated_image} 
                                    />
                                    <IntelligenceWorkspace 
                                        rawReport={result.raw_report} 
                                        patientSummary={result.summary} 
                                    />
                                </div>
                                <div className="flex justify-center mt-2 pb-8">
                                    <button 
                                        onClick={handleReset}
                                        className="px-10 py-4 bg-slate-800/80 backdrop-blur-xl border border-white/10 hover:bg-slate-700 hover:border-white/20 rounded-full text-white font-semibold text-lg shadow-xl transition-all transform hover:scale-105 active:scale-95"
                                    >
                                        Start New Analysis
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </main>

            {/* About the Project Section */}
            <section className="w-full bg-slate-900/40 border-t border-white/5 py-24 px-6 md:px-8 lg:px-12 flex justify-center">
                <div className="max-w-[1400px] w-full flex flex-col gap-16">
                    <div className="text-center">
                        <h2 className="text-3xl md:text-4xl font-medium text-white mb-6">How it Works</h2>
                        <p className="text-slate-400 text-lg md:text-xl max-w-3xl mx-auto leading-relaxed">
                            This application uses advanced multimodal AI to analyze both visual and textual medical data simultaneously. By combining computer vision with natural language processing, it provides comprehensive insights that bridge the gap between imaging and clinical notes.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
                        {/* Connecting Line */}
                        <div className="hidden md:block absolute top-6 left-[16%] right-[16%] h-[2px] bg-gradient-to-r from-primary/10 via-primary/30 to-primary/10 z-0"></div>

                        {/* Step 1 */}
                        <div className="bg-slate-800/40 p-8 rounded-3xl border border-white/5 backdrop-blur-sm relative z-10 flex flex-col items-center text-center hover:bg-slate-800/60 transition-colors">
                            <div className="w-14 h-14 rounded-full bg-slate-900 border-2 border-primary/30 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(48,255,245,0.15)]">
                                <span className="text-primary font-bold text-xl">1</span>
                            </div>
                            <h3 className="text-xl font-medium text-white mb-4">Upload Data</h3>
                            <p className="text-slate-400 leading-relaxed text-sm">
                                Provide a Chest X-Ray image (PNG/JPG) and the corresponding clinical report (PDF/TXT). The system securely handles standard medical formats.
                            </p>
                        </div>
                        
                        {/* Step 2 */}
                        <div className="bg-slate-800/40 p-8 rounded-3xl border border-white/5 backdrop-blur-sm relative z-10 flex flex-col items-center text-center hover:bg-slate-800/60 transition-colors">
                            <div className="w-14 h-14 rounded-full bg-slate-900 border-2 border-primary/30 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(48,255,245,0.15)]">
                                <span className="text-primary font-bold text-xl">2</span>
                            </div>
                            <h3 className="text-xl font-medium text-white mb-4">AI Analysis</h3>
                            <p className="text-slate-400 leading-relaxed text-sm">
                                Our multimodal LLM processes the image to detect anomalies and cross-references them with the clinical text to ensure consistency and accuracy.
                            </p>
                        </div>

                        {/* Step 3 */}
                        <div className="bg-slate-800/40 p-8 rounded-3xl border border-white/5 backdrop-blur-sm relative z-10 flex flex-col items-center text-center hover:bg-slate-800/60 transition-colors">
                            <div className="w-14 h-14 rounded-full bg-slate-900 border-2 border-primary/30 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(48,255,245,0.15)]">
                                <span className="text-primary font-bold text-xl">3</span>
                            </div>
                            <h3 className="text-xl font-medium text-white mb-4">Review Insights</h3>
                            <p className="text-slate-400 leading-relaxed text-sm">
                                Explore an interactive workspace featuring annotated visual findings side-by-side with a simplified, patient-friendly text summary.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
