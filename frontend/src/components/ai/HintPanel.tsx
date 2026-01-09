import { useState } from 'react'
import Button from '@/components/ui/Button'
import type { AiHint } from '@/lib/types'
import { cn } from '@/lib/utils'

interface HintPanelProps {
  onRequestHint: () => Promise<AiHint | null>
  onHighlightWords: (words: string[]) => void
  disabled?: boolean
  hintsUsed: number
  maxHints?: number
}

export default function HintPanel({
  onRequestHint,
  onHighlightWords,
  disabled,
  hintsUsed,
  maxHints = 3,
}: HintPanelProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [currentHint, setCurrentHint] = useState<AiHint | null>(null)
  const [error, setError] = useState<string | null>(null)

  const canRequestHint = hintsUsed < maxHints && !disabled

  const handleRequestHint = async () => {
    if (!canRequestHint) return

    setIsLoading(true)
    setError(null)

    try {
      const hint = await onRequestHint()
      if (hint) {
        setCurrentHint(hint)
      }
    } catch (err) {
      setError('Failed to get hint. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleShowWords = () => {
    if (currentHint?.suggestedWords) {
      onHighlightWords(currentHint.suggestedWords)
    }
  }

  return (
    <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-800">AI Assistant</h3>
        <span className="text-sm text-gray-500">
          {hintsUsed}/{maxHints} hints used
        </span>
      </div>

      {currentHint ? (
        <div className="space-y-3">
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <p className="text-gray-700">{currentHint.hint}</p>
            <div className="mt-2 flex items-center gap-2">
              <span className="text-xs text-gray-500">
                Confidence: {Math.round(currentHint.confidence * 100)}%
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleShowWords}
            >
              Show suggested words
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setCurrentHint(null)}
            >
              Clear
            </Button>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}
          <p className="text-sm text-gray-600">
            Stuck? Ask the AI for a hint about one of the remaining categories.
          </p>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleRequestHint}
            disabled={!canRequestHint || isLoading}
            className="w-full"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
                Thinking...
              </span>
            ) : (
              'Get AI Hint'
            )}
          </Button>
          {!canRequestHint && hintsUsed >= maxHints && (
            <p className="text-xs text-gray-500 text-center">
              No more hints available
            </p>
          )}
        </div>
      )}
    </div>
  )
}
