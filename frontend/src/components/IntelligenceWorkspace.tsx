'use client';

import React, { Fragment } from 'react';
import { Tab } from '@headlessui/react';
import { motion } from 'framer-motion';

interface IntelligenceWorkspaceProps {
    rawReport: {
        findings: string;
        impression: string;
    };
    patientSummary: string;
}

export default function IntelligenceWorkspace({ rawReport, patientSummary }: IntelligenceWorkspaceProps) {
    return (
        <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex flex-col h-full shadow-2xl">
            <Tab.Group>
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-white">Intelligence Workspace</h3>
                </div>
                
                <Tab.List className="flex space-x-2 rounded-xl bg-slate-800/50 p-1 mb-6 border border-slate-700/50">
                    <Tab as={Fragment}>
                        {({ selected }) => (
                            <button
                                className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 transition-all outline-none
                                ${selected 
                                    ? 'bg-primary text-slate-900 shadow' 
                                    : 'text-slate-400 hover:bg-white/[0.05] hover:text-white'
                                }`}
                            >
                                Raw Clinical Report
                            </button>
                        )}
                    </Tab>
                    <Tab as={Fragment}>
                        {({ selected }) => (
                            <button
                                className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 transition-all outline-none
                                ${selected 
                                    ? 'bg-secondary text-white shadow' 
                                    : 'text-slate-400 hover:bg-white/[0.05] hover:text-white'
                                }`}
                            >
                                Patient Summary
                            </button>
                        )}
                    </Tab>
                </Tab.List>

                <Tab.Panels className="flex-1 overflow-y-auto pr-2 relative min-h-[400px]">
                    <Tab.Panel className="focus:outline-none h-full">
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4 }}
                            className="font-mono text-sm text-green-400 bg-black/40 p-5 rounded-xl border border-green-900/30 h-full flex flex-col"
                        >
                            <h4 className="text-green-300 font-bold mb-2 uppercase border-b border-green-900/50 pb-1 shrink-0">Findings</h4>
                            <div className="whitespace-pre-wrap leading-relaxed mb-6 overflow-y-auto shrink">{rawReport.findings}</div>
                            
                            <h4 className="text-green-300 font-bold mb-2 uppercase border-b border-green-900/50 pb-1 shrink-0">Impression</h4>
                            <div className="whitespace-pre-wrap leading-relaxed overflow-y-auto flex-1">{rawReport.impression}</div>
                        </motion.div>
                    </Tab.Panel>

                    <Tab.Panel className="focus:outline-none h-full flex flex-col">
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4 }}
                            className="flex-1 flex flex-col"
                        >
                            <div className="text-slate-200 text-lg leading-loose font-light whitespace-pre-wrap bg-slate-800/30 p-6 rounded-xl border border-slate-700/30 flex-1 overflow-y-auto">
                                {patientSummary}
                            </div>
                            <div className="mt-6 pt-4 border-t border-slate-700/50 shrink-0">
                                <p className="text-xs text-slate-400 text-center uppercase tracking-wider font-semibold">
                                    Disclaimer: AI Generated. Please consult a physician for medical advice.
                                </p>
                            </div>
                        </motion.div>
                    </Tab.Panel>
                </Tab.Panels>
            </Tab.Group>
        </div>
    );
}
