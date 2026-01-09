import { useState, useCallback, useEffect, useRef } from 'react'
import type { GameState, Category, Puzzle, Guess } from '@/lib/types'
import { shuffleArray } from '@/lib/utils'
import api from '@/lib/api'

const INITIAL_STATE: GameState = {
  sessionId: null,
  puzzle: null,
  remainingWords: [],
  selectedWords: [],
  solvedCategories: [],
  mistakes: 0,
  guesses: [],
  isLoading: false,
  isComplete: false,
  isWon: false,
  solveTimeMs: null,
  usedAiHint: false,
}

export function useGame() {
  const [state, setState] = useState<GameState>(INITIAL_STATE)
  const [shakingWords, setShakingWords] = useState<string[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const startTimeRef = useRef<number | null>(null)

  // Start a new game
  const startGame = useCallback(async (puzzleId?: string) => {
    setState((prev) => ({ ...prev, isLoading: true }))
    try {
      const response = await api.startGame(puzzleId)
      startTimeRef.current = Date.now()
      setState({
        ...INITIAL_STATE,
        sessionId: response.sessionId,
        puzzle: response.puzzle,
        remainingWords: response.puzzle.words,
        isLoading: false,
      })
    } catch (error) {
      console.error('Failed to start game:', error)
      setState((prev) => ({ ...prev, isLoading: false }))
      throw error
    }
  }, [])

  // Select/deselect a word
  const selectWord = useCallback((word: string) => {
    setState((prev) => {
      if (prev.selectedWords.includes(word)) {
        return {
          ...prev,
          selectedWords: prev.selectedWords.filter((w) => w !== word),
        }
      }
      if (prev.selectedWords.length >= 4) {
        return prev
      }
      return {
        ...prev,
        selectedWords: [...prev.selectedWords, word],
      }
    })
  }, [])

  // Clear selection
  const clearSelection = useCallback(() => {
    setState((prev) => ({ ...prev, selectedWords: [] }))
  }, [])

  // Shuffle remaining words
  const shuffleWords = useCallback(() => {
    setState((prev) => ({
      ...prev,
      remainingWords: shuffleArray(prev.remainingWords),
    }))
  }, [])

  // Submit a guess
  const submitGuess = useCallback(async () => {
    if (state.selectedWords.length !== 4 || !state.sessionId) {
      return
    }

    setIsSubmitting(true)
    try {
      const response = await api.submitGuess(state.sessionId, state.selectedWords)

      if (response.result === 'correct' && response.category) {
        // Correct guess
        setState((prev) => ({
          ...prev,
          remainingWords: prev.remainingWords.filter(
            (w) => !prev.selectedWords.includes(w)
          ),
          selectedWords: [],
          solvedCategories: [...prev.solvedCategories, response.category!],
          guesses: [...prev.guesses, { words: prev.selectedWords, result: 'correct', category: response.category }],
          isComplete: response.gameState.isComplete,
          isWon: response.gameState.isWon,
          solveTimeMs: response.gameState.solveTimeMs,
        }))
      } else {
        // Wrong guess
        setShakingWords(state.selectedWords)
        setTimeout(() => setShakingWords([]), 500)

        setState((prev) => ({
          ...prev,
          selectedWords: [],
          mistakes: prev.mistakes + 1,
          guesses: [...prev.guesses, { words: prev.selectedWords, result: 'wrong', oneAway: response.oneAway }],
          isComplete: prev.mistakes + 1 >= 4,
          isWon: false,
        }))

        // Calculate solve time if game over
        if (state.mistakes + 1 >= 4 && startTimeRef.current) {
          setState((prev) => ({
            ...prev,
            solveTimeMs: Date.now() - startTimeRef.current!,
          }))
        }
      }
    } catch (error) {
      console.error('Failed to submit guess:', error)
    } finally {
      setIsSubmitting(false)
    }
  }, [state.selectedWords, state.sessionId, state.mistakes])

  // Get AI hint
  const getHint = useCallback(async () => {
    if (!state.sessionId) return null

    try {
      const hint = await api.getHint(state.sessionId, state.remainingWords)
      setState((prev) => ({ ...prev, usedAiHint: true }))
      return hint
    } catch (error) {
      console.error('Failed to get hint:', error)
      return null
    }
  }, [state.sessionId, state.remainingWords])

  // Reset game
  const resetGame = useCallback(() => {
    setState(INITIAL_STATE)
    startTimeRef.current = null
  }, [])

  return {
    // State
    ...state,
    shakingWords,
    isSubmitting,

    // Actions
    startGame,
    selectWord,
    clearSelection,
    shuffleWords,
    submitGuess,
    getHint,
    resetGame,
  }
}

export default useGame
