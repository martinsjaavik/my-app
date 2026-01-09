import { useEffect, useState } from 'react'
import GameBoard from '@/components/game/GameBoard'
import ResultsModal from '@/components/game/ResultsModal'
import HintPanel from '@/components/ai/HintPanel'
import Button from '@/components/ui/Button'
import { useGame } from '@/hooks/useGame'
import { formatDate } from '@/lib/utils'

export default function HomePage() {
  const {
    puzzle,
    remainingWords,
    selectedWords,
    solvedCategories,
    mistakes,
    guesses,
    isLoading,
    isComplete,
    isWon,
    solveTimeMs,
    usedAiHint,
    shakingWords,
    isSubmitting,
    startGame,
    selectWord,
    clearSelection,
    shuffleWords,
    submitGuess,
    getHint,
    resetGame,
  } = useGame()

  const [showResults, setShowResults] = useState(false)
  const [hintsUsed, setHintsUsed] = useState(0)
  const [highlightedWords, setHighlightedWords] = useState<string[]>([])

  // Start game on mount
  useEffect(() => {
    startGame()
  }, [])

  // Show results when game completes
  useEffect(() => {
    if (isComplete) {
      setTimeout(() => setShowResults(true), 500)
    }
  }, [isComplete])

  const handleWordClick = (word: string) => {
    // Clear highlights when selecting
    setHighlightedWords([])
    selectWord(word)
  }

  const handleGetHint = async () => {
    const hint = await getHint()
    if (hint) {
      setHintsUsed((prev) => prev + 1)
    }
    return hint
  }

  const handlePlayAgain = () => {
    setShowResults(false)
    setHintsUsed(0)
    setHighlightedWords([])
    startGame()
  }

  if (isLoading || !puzzle) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-gray-800 rounded-full mx-auto mb-4" />
          <p className="text-gray-600">Loading today's puzzle...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-lg font-medium text-gray-600 mb-1">
            {formatDate(puzzle.date)}
          </h2>
          <p className="text-sm text-gray-500">
            Puzzle #{puzzle.puzzleNumber}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Create four groups of four!
          </p>
        </div>

        {/* Main game area */}
        <div className="grid gap-6 lg:grid-cols-[1fr_280px]">
          {/* Game board */}
          <GameBoard
            words={remainingWords}
            selectedWords={[...selectedWords, ...highlightedWords]}
            solvedCategories={solvedCategories}
            mistakes={mistakes}
            isSubmitting={isSubmitting}
            shakingWords={shakingWords}
            onWordClick={handleWordClick}
            onSubmit={submitGuess}
            onDeselectAll={clearSelection}
            onShuffle={shuffleWords}
          />

          {/* AI Panel */}
          {!isComplete && (
            <div className="lg:order-last">
              <HintPanel
                onRequestHint={handleGetHint}
                onHighlightWords={setHighlightedWords}
                disabled={isComplete}
                hintsUsed={hintsUsed}
              />
            </div>
          )}
        </div>

        {/* One away message */}
        {guesses.length > 0 && guesses[guesses.length - 1].oneAway && (
          <div className="mt-4 text-center">
            <span className="inline-block bg-yellow-100 text-yellow-800 px-4 py-2 rounded-full text-sm font-medium">
              One away...
            </span>
          </div>
        )}
      </div>

      {/* Results modal */}
      <ResultsModal
        isOpen={showResults}
        isWon={isWon}
        puzzleNumber={puzzle.puzzleNumber}
        solvedCategories={solvedCategories}
        guesses={guesses}
        mistakes={mistakes}
        solveTimeMs={solveTimeMs}
        usedAiHint={usedAiHint}
        onPlayAgain={handlePlayAgain}
        onClose={() => setShowResults(false)}
      />
    </div>
  )
}
