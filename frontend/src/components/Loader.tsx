export default function Loader() {
    return (
        <div className="flex flex-col items-center justify-center p-12 bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl w-full">
            <div className="w-16 h-16 border-4 border-primary/30 border-t-primary rounded-full animate-spin mb-6"></div>
            <h3 className="text-2xl font-semibold text-white animate-pulse">Analyzing Multimodal Data...</h3>
            <p className="text-slate-400 mt-2 text-lg">Running YOLOv11 & Gemini 2.5 Flash pipeline</p>
        </div>
    );
}
