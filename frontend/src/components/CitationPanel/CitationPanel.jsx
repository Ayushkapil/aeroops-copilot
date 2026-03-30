/**
 * CitationPanel — placeholder sidebar component for displaying source
 * citations returned by the SOP RAG pipeline.
 */
export default function CitationPanel() {
  return (
    <div className="bg-white rounded-xl shadow border border-gray-100 p-4">
      <h2 className="text-sm font-semibold text-gray-700 mb-3">
        📎 Citations
      </h2>
      <p className="text-xs text-gray-400 italic">
        Source citations will appear here when a RAG answer is generated.
      </p>
      {/* Citation cards will be rendered here */}
    </div>
  )
}
