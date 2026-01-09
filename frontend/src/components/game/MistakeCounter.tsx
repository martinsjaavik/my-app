import { cn } from '@/lib/utils'

interface MistakeCounterProps {
  mistakes: number
  maxMistakes?: number
}

export default function MistakeCounter({
  mistakes,
  maxMistakes = 4,
}: MistakeCounterProps) {
  const remaining = maxMistakes - mistakes

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-600">Mistakes remaining:</span>
      <div className="flex gap-1">
        {Array.from({ length: maxMistakes }).map((_, i) => (
          <div
            key={i}
            className={cn(
              'w-4 h-4 rounded-full transition-all duration-300',
              {
                'bg-gray-800': i < remaining,
                'bg-gray-300': i >= remaining,
              }
            )}
          />
        ))}
      </div>
    </div>
  )
}
