/**
 * IncidentViewer — placeholder component for displaying structured
 * incident analysis results (timeline, tags, contributing factors).
 */
export default function IncidentViewer() {
  return (
    <div className="bg-white rounded-xl shadow border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Analysis Results
      </h2>
      <p className="text-sm text-gray-400 italic">
        Upload an incident PDF above to see structured analysis results here.
      </p>
      {/* Incident analysis output will be rendered here */}
    </div>
  )
}
