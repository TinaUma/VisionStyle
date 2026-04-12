"use client";

import { useState, useRef } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface AnalysisResult {
  image: {
    filename: string;
    width: number;
    height: number;
    format: string;
  };
  analysis: {
    style: string;
    palette: string[];
    materials: string[];
    mood: string;
    keywords: string[];
    verdict: string;
  };
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFile(f: File) {
    setFile(f);
    setResult(null);
    setError(null);
    setPreview(URL.createObjectURL(f));
  }

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  }

  function onDrop(e: React.DragEvent) {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  }

  async function analyze() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${API_URL}/analyze`, { method: "POST", body: form });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail ?? `Ошибка ${res.status}`);
      }
      setResult(await res.json());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Неизвестная ошибка");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white flex flex-col items-center py-16 px-4">
      <h1 className="text-4xl font-bold mb-2 tracking-tight">VisionStyle</h1>
      <p className="text-gray-400 mb-10 text-center max-w-md">
        Загрузи фото — получи структурированный паспорт стиля
      </p>

      {/* Upload zone */}
      <div
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
        className="w-full max-w-lg border-2 border-dashed border-gray-600 rounded-2xl p-10 flex flex-col items-center gap-4 cursor-pointer hover:border-indigo-500 transition-colors"
      >
        {preview ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={preview} alt="preview" className="max-h-64 rounded-xl object-contain" />
        ) : (
          <>
            <div className="text-5xl">🖼️</div>
            <p className="text-gray-400 text-sm">Перетащи сюда или нажми для выбора</p>
            <p className="text-gray-600 text-xs">JPG, PNG, WebP</p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          onChange={onFileChange}
        />
      </div>

      {file && (
        <button
          onClick={analyze}
          disabled={loading}
          className="mt-6 px-8 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 rounded-xl font-semibold transition-colors"
        >
          {loading ? "Анализирую..." : "Анализировать стиль"}
        </button>
      )}

      {error && (
        <div className="mt-6 w-full max-w-lg bg-red-900/40 border border-red-700 rounded-xl p-4 text-red-300 text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-10 w-full max-w-lg space-y-6">
          <div className="bg-gray-900 rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-1">{result.analysis.style}</h2>
            <p className="text-gray-400 text-sm">{result.analysis.verdict}</p>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3">Палитра</h3>
            <div className="flex gap-3 flex-wrap">
              {result.analysis.palette.map((hex) => (
                <div key={hex} className="flex flex-col items-center gap-1">
                  <div
                    className="w-10 h-10 rounded-lg border border-gray-700"
                    style={{ backgroundColor: hex }}
                  />
                  <span className="text-xs text-gray-500">{hex}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-gray-400 uppercase mb-2">Настроение</h3>
            <p className="text-gray-200">{result.analysis.mood}</p>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-gray-400 uppercase mb-2">Ключевые слова</h3>
            <div className="flex flex-wrap gap-2">
              {result.analysis.keywords.map((kw) => (
                <span key={kw} className="px-3 py-1 bg-indigo-900/50 border border-indigo-700 rounded-full text-sm text-indigo-300">
                  {kw}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-gray-400 uppercase mb-2">Материалы</h3>
            <div className="flex flex-wrap gap-2">
              {result.analysis.materials.map((m) => (
                <span key={m} className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                  {m}
                </span>              ))}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
