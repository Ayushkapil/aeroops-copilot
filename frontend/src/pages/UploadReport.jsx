import IncidentViewer from '../components/IncidentViewer/IncidentViewer.jsx'

export default function UploadReport() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        Incident Report Analysis
      </h1>
      <p className="text-gray-500 mb-6">
        Upload an ASRS or NTSB incident PDF to extract structured intelligence.
      </p>
      <div className="bg-white rounded-xl shadow p-6 border border-gray-100 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload PDF
        </label>
        <input
          type="file"
          accept=".pdf"
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          disabled
        >
          Analyze Report
        </button>
      </div>
      <IncidentViewer />
    </div>
  )
}
