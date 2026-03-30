export default function Home() {
  return (
    <div className="max-w-3xl mx-auto py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        ✈️ AeroOps Copilot
      </h1>
      <p className="text-lg text-gray-600 mb-8">
        A modular AI system for aviation safety &amp; operations. Combining
        RAG-powered SOP retrieval, structured incident analysis, and fatigue
        risk planning into a unified intelligent copilot.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow p-6 border border-gray-100">
          <div className="text-2xl mb-2">🔍</div>
          <h2 className="font-semibold text-gray-800 mb-1">SOP RAG</h2>
          <p className="text-sm text-gray-500">
            Semantic search over FAA SOPs with cross-encoder reranking and
            cited answers.
          </p>
        </div>
        <div className="bg-white rounded-xl shadow p-6 border border-gray-100">
          <div className="text-2xl mb-2">📄</div>
          <h2 className="font-semibold text-gray-800 mb-1">Incident Analysis</h2>
          <p className="text-sm text-gray-500">
            Upload an ASRS incident PDF and get structured intelligence with
            timeline and tags.
          </p>
        </div>
        <div className="bg-white rounded-xl shadow p-6 border border-gray-100">
          <div className="text-2xl mb-2">😴</div>
          <h2 className="font-semibold text-gray-800 mb-1">Fatigue Risk</h2>
          <p className="text-sm text-gray-500">
            Upload a pilot schedule CSV for rule-based + LLM fatigue risk
            assessment.
          </p>
        </div>
      </div>
    </div>
  )
}
