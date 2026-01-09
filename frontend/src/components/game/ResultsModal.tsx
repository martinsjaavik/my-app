import { useEffect, useState } from 'react'
import Button from '@/components/ui/Button'
import type { Category, Guess } from '@/lib/types'
import { formatTime, generateShareText, copyToClipboard } from '@/lib/utils'
import { DIFFICULTY_COLORS } from '@/lib/types'

interface ResultsModalProps {
  isOpen: boolean
  isWon: boolean
  puzzleNumber: number
  solvedCategories: Category[]
  guesses: Guess[]
  mistakes: number
  solveTimeMs: number | null
  usedAiHint: boolean
  onPlayAgain: () => void
  onClose: () => void
}

export default function ResultsModal({
  isOpen,
  isWon,
  puzzleNumber,
  solvedCategories,
  guesses,
  mistakes,
  solveTimeMs,
  usedAiHint,
  onPlayAgain,
  onClose,
}: ResultsModalProps) {
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (copied) {
      const timer = setTimeout(() => setCopied(false), 2000)
      return () => clearTimeout(timer)
    }
  }, [copied])

  if (!isOpen) return null

  const handleShare = async () => {
    const shareText = generateShareText(puzzleNumber, guesses, isWon)
    await copyToClipboard(shareText)
    setCopied(true)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />
      <div className="relative bg-white rounded-2xl shadow-xl max-w-md w-full mx-4 p-6 animate-bounce-in">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold mb-2">
            {isWon ? 'Congratulations!' : 'Better luck next time!'}
          </h2>
          <p className="text-gray-600">
            Connections #{puzzleNumber}
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <div className="text-2xl font-bold">{4 - mistakes}</div>
            <div className="text-xs text-gray-500">Categories</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{mistakes}</div>
            <div className="text-xs text-gray-500">Mistakes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">
              {solveTimeMs ? formatTime(solveTimeMs) : '--'}
            </div>
            <div className="text-xs text-gray-500">Time</div>
          </div>
        </div>

        {/* Categories solved */}
        <div className="space-y-2 mb-6">
          {solvedCategories.map((category) => {
            const colors = DIFFICULTY_COLORS[category.difficulty]
            return (
              <div
                key={category.id}
                className={`${colors.bg} ${colors.text} rounded-lg py-2 px-4 text-center`}
              >
                <div className="font-bold text-sm uppercase">{category.name}</div>
                <div className="text-xs opacity-80">
                  {category.words.join(', ')}
                </div>
              </div>
            )
          })}
        </div>

        {usedAiHint && (
          <p className="text-center text-sm text-gray-500 mb-4">
            * AI hint was used
          </p>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <Button
            variant="outline"
            className="flex-1"
            onClick={handleShare}
          >
            {copied ? 'Copied!' : 'Share'}
          </Button>
          <Button
            variant="primary"
            className="flex-1"
            onClick={onPlayAgain}
          >
            Play Again
          </Button>
        </div>
      </div>
    </div>
  )
}
