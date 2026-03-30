/**
 * FatigueDashboard — placeholder component for displaying fatigue risk
 * assessment results (score, risk level, mitigations).
 */
export default function FatigueDashboard() {
  return (
    <div className="bg-white rounded-xl shadow border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Fatigue Risk Dashboard
      </h2>
      <p className="text-sm text-gray-400 italic">
        Upload a schedule CSV above to see fatigue risk results here.
      </p>
      {/* Risk score gauge and mitigation recommendations will render here */}
    </div>
  )
}
