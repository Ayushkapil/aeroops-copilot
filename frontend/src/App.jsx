import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar/Sidebar.jsx'
import Home from './pages/Home.jsx'
import Chat from './pages/Chat.jsx'
import UploadReport from './pages/UploadReport.jsx'
import UploadSchedule from './pages/UploadSchedule.jsx'

export default function App() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/upload-report" element={<UploadReport />} />
          <Route path="/upload-schedule" element={<UploadSchedule />} />
        </Routes>
      </main>
    </div>
  )
}
