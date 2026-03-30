import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/', label: '🏠 Home' },
  { to: '/chat', label: '💬 SOP Chat' },
  { to: '/upload-report', label: '📄 Incident Report' },
  { to: '/upload-schedule', label: '😴 Fatigue Risk' },
]

/**
 * Sidebar — main navigation sidebar for the AeroOps Copilot app.
 */
export default function Sidebar() {
  return (
    <nav className="w-56 bg-gray-900 text-white min-h-screen p-4 flex flex-col">
      <div className="mb-8">
        <h1 className="text-lg font-bold">✈️ AeroOps</h1>
        <p className="text-xs text-gray-400">Copilot</p>
      </div>
      <ul className="space-y-1">
        {navItems.map(({ to, label }) => (
          <li key={to}>
            <NavLink
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800'
                }`
              }
            >
              {label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
