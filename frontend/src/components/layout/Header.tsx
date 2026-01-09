import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Connections AI</h1>
          </Link>
          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className="text-sm font-medium text-gray-600 hover:text-black transition-colors"
            >
              Play
            </Link>
            <Link
              to="/archive"
              className="text-sm font-medium text-gray-600 hover:text-black transition-colors"
            >
              Archive
            </Link>
            <Link
              to="/leaderboard"
              className="text-sm font-medium text-gray-600 hover:text-black transition-colors"
            >
              Leaderboard
            </Link>
            <Link
              to="/multiplayer"
              className="text-sm font-medium text-gray-600 hover:text-black transition-colors"
            >
              Multiplayer
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
