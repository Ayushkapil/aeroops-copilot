import FatigueDashboard from '../components/FatigueDashboard/FatigueDashboard.jsx'

export default function UploadSchedule() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        Fatigue Risk Assessment
      </h1>
      <p className="text-gray-500 mb-6">
        Upload a pilot schedule CSV to receive a rule-based and LLM-powered
        fatigue risk assessment.
      </p>
      <div className="bg-white rounded-xl shadow p-6 border border-gray-100 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload Schedule CSV
        </label>
        <input
          type="file"
          accept=".csv"
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
        />
        <button
          className="mt-4 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          disabled
        >
          Assess Fatigue Risk
        </button>
      </div>
      <FatigueDashboard />
    </div>
  )
}
