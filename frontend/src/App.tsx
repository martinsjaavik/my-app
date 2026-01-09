import { Routes, Route } from 'react-router-dom'
import Header from '@/components/layout/Header'
import HomePage from '@/pages/HomePage'

// Placeholder pages - will be implemented later
function ArchivePage() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Puzzle Archive</h2>
        <p className="text-gray-600">Coming soon...</p>
      </div>
    </div>
  )
}

function LeaderboardPage() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Leaderboard</h2>
        <p className="text-gray-600">Coming soon...</p>
      </div>
    </div>
  )
}

function MultiplayerPage() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Multiplayer</h2>
        <p className="text-gray-600">Coming soon...</p>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/archive" element={<ArchivePage />} />
        <Route path="/leaderboard" element={<LeaderboardPage />} />
        <Route path="/multiplayer" element={<MultiplayerPage />} />
      </Routes>
    </div>
  )
}
