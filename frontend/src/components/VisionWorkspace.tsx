'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Switch } from '@headlessui/react';

interface VisionWorkspaceProps {
    originalImageFile: File | null;
    annotatedImageBase64: string;
}

export default function VisionWorkspace({ originalImageFile, annotatedImageBase64 }: VisionWorkspaceProps) {
    const [originalUrl, setOriginalUrl] = useState<string | null>(null);
    const [showGrounding, setShowGrounding] = useState(true);

    useEffect(() => {
        if (originalImageFile) {
            const url = URL.createObjectURL(originalImageFile);
            setOriginalUrl(url);
            return () => URL.revokeObjectURL(url);
        }
    }, [originalImageFile]);

    return (
        <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex flex-col h-full shadow-2xl">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-semibold text-white">Vision Workspace</h3>
                
                <div className="flex items-center gap-3 bg-slate-800/50 py-2 px-4 rounded-xl border border-slate-700/50">
                    <span className="text-sm font-medium text-slate-300">AI Grounding</span>
                    <Switch
                        checked={showGrounding}
                        onChange={setShowGrounding}
                        className={`${
                            showGrounding ? 'bg-primary' : 'bg-slate-600'
                        } relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-slate-900`}
                    >
                        <span className="sr-only">Toggle AI Grounding</span>
                        <span
                            className={`${
                                showGrounding ? 'translate-x-6' : 'translate-x-1'
                            } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
                        />
                    </Switch>
                </div>
            </div>

            <div className="relative w-full flex-1 flex items-center justify-center rounded-xl overflow-hidden border border-slate-700/50 bg-slate-950/50 p-2 min-h-[400px]">
                {/* Base Image */}
                {originalUrl && (
                    <img 
                        src={originalUrl} 
                        alt="Original X-Ray" 
                        className="absolute inset-0 w-full h-full object-contain p-2" 
                    />
                )}
                
                {/* Overlay Image (Annotated) */}
                <AnimatePresence>
                    {showGrounding && (
                        <motion.img 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.5, ease: "easeInOut" }}
                            src={annotatedImageBase64} 
                            alt="Annotated X-Ray" 
                            className="absolute inset-0 w-full h-full object-contain p-2 z-10 drop-shadow-xl" 
                        />
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
