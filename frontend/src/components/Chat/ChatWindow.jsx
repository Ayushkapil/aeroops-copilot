import { useState } from 'react'

/**
 * ChatWindow — placeholder chat interface for SOP queries.
 * Renders a message list and input box. API integration pending.
 */
export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "Hello! Ask me any aviation SOP question and I'll retrieve relevant regulations with citations.",
    },
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim()) return
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), role: 'user', content: input },
      {
        id: Date.now() + 1,
        role: 'assistant',
        content: '⚠️ SOP RAG pipeline not yet implemented. Coming soon!',
      },
    ])
    setInput('')
  }

  return (
    <div className="flex flex-col bg-white rounded-xl shadow border border-gray-100 h-[600px]">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-xl px-4 py-2 text-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      <div className="border-t p-4 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask an aviation question…"
          className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  )
}
