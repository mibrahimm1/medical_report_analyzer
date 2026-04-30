import React from 'react';

interface UploadBoxProps {
    onImageSelect: (file: File) => void;
    onReportSelect: (file: File) => void;
    imageFile: File | null;
    reportFile: File | null;
}

export default function UploadBox({ onImageSelect, onReportSelect, imageFile, reportFile }: UploadBoxProps) {
    return (
        <div className="space-y-6 w-full">
            <div className="flex flex-col md:flex-row gap-6 w-full">
                {/* Image Upload */}
                <div className="flex-1 p-6 border-2 border-dashed border-slate-500/50 rounded-2xl bg-black/40 backdrop-blur-xl flex flex-col items-center justify-center min-h-[200px] transition-all hover:border-primary/50">
                    <h3 className="text-xl font-medium text-white mb-2">Chest X-Ray Image</h3>
                    <p className="text-slate-400 text-sm mb-4">PNG, JPG up to 10MB</p>
                    <input 
                        type="file" 
                        accept="image/*" 
                        onChange={(e) => e.target.files && onImageSelect(e.target.files[0])}
                        className="text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-medium file:bg-primary file:text-slate-900 hover:file:opacity-90 cursor-pointer"
                    />
                    {imageFile && <p className="mt-3 text-tertiary text-sm font-medium truncate max-w-[200px]">{imageFile.name}</p>}
                </div>
                
                {/* Report Upload */}
                <div className="flex-1 p-6 border-2 border-dashed border-slate-500/50 rounded-2xl bg-black/40 backdrop-blur-xl flex flex-col items-center justify-center min-h-[200px] transition-all hover:border-primary/50">
                    <h3 className="text-xl font-medium text-white mb-2">Clinical Report</h3>
                    <p className="text-slate-400 text-sm mb-4">PDF or TXT</p>
                    <input 
                        type="file" 
                        accept=".pdf,.txt" 
                        onChange={(e) => e.target.files && onReportSelect(e.target.files[0])}
                        className="text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-medium file:bg-primary file:text-slate-900 hover:file:opacity-90 cursor-pointer"
                    />
                    {reportFile && <p className="mt-3 text-tertiary text-sm font-medium truncate max-w-[200px]">{reportFile.name}</p>}
                </div>
            </div>
        </div>
    );
}
