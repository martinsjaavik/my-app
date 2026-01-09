import { cn } from '@/lib/utils'

interface WordTileProps {
  word: string
  isSelected: boolean
  isDisabled: boolean
  isShaking?: boolean
  onClick: () => void
}

export default function WordTile({
  word,
  isSelected,
  isDisabled,
  isShaking,
  onClick,
}: WordTileProps) {
  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      className={cn(
        'w-full aspect-[2/1] rounded-lg font-bold text-sm sm:text-base uppercase',
        'flex items-center justify-center text-center px-2',
        'transition-all duration-150 ease-out',
        'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400',
        {
          'bg-connections-tile text-black hover:bg-gray-300':
            !isSelected && !isDisabled,
          'bg-connections-tile-selected text-white scale-[0.98]': isSelected,
          'opacity-50 cursor-not-allowed': isDisabled,
          'animate-shake': isShaking,
        }
      )}
    >
      {word}
    </button>
  )
}
