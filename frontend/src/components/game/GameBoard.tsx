import { useState, useCallback } from 'react'
import WordTile from './WordTile'
import CategoryRow from './CategoryRow'
import GameControls from './GameControls'
import MistakeCounter from './MistakeCounter'
import type { Category } from '@/lib/types'
import { shuffleArray } from '@/lib/utils'

interface GameBoardProps {
  words: string[]
  selectedWords: string[]
  solvedCategories: Category[]
  mistakes: number
  isSubmitting: boolean
  shakingWords: string[]
  onWordClick: (word: string) => void
  onSubmit: () => void
  onDeselectAll: () => void
  onShuffle: () => void
}

export default function GameBoard({
  words,
  selectedWords,
  solvedCategories,
  mistakes,
  isSubmitting,
  shakingWords,
  onWordClick,
  onSubmit,
  onDeselectAll,
  onShuffle,
}: GameBoardProps) {
  const canSubmit = selectedWords.length === 4
  const canShuffle = words.length > 0
  const isGameOver = mistakes >= 4 || solvedCategories.length === 4

  return (
    <div className="w-full max-w-lg mx-auto space-y-4">
      {/* Solved categories */}
      <div className="space-y-2">
        {solvedCategories.map((category, index) => (
          <CategoryRow
            key={category.id}
            category={category}
            animateIn={index === solvedCategories.length - 1}
          />
        ))}
      </div>

      {/* Word grid */}
      {words.length > 0 && !isGameOver && (
        <div className="grid grid-cols-4 gap-2">
          {words.map((word) => (
            <WordTile
              key={word}
              word={word}
              isSelected={selectedWords.includes(word)}
              isDisabled={isSubmitting}
              isShaking={shakingWords.includes(word)}
              onClick={() => onWordClick(word)}
            />
          ))}
        </div>
      )}

      {/* Mistake counter */}
      {!isGameOver && (
        <div className="flex justify-center">
          <MistakeCounter mistakes={mistakes} />
        </div>
      )}

      {/* Controls */}
      {!isGameOver && (
        <GameControls
          selectedCount={selectedWords.length}
          canSubmit={canSubmit}
          canShuffle={canShuffle}
          isSubmitting={isSubmitting}
          onSubmit={onSubmit}
          onDeselect={onDeselectAll}
          onShuffle={onShuffle}
        />
      )}
    </div>
  )
}
