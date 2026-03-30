import ChatWindow from '../components/Chat/ChatWindow.jsx'
import CitationPanel from '../components/CitationPanel/CitationPanel.jsx'

export default function Chat() {
  return (
    <div className="flex gap-6 h-full">
      <div className="flex-1">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">SOP Chat</h1>
        <ChatWindow />
      </div>
      <div className="w-80">
        <CitationPanel />
      </div>
    </div>
  )
}
