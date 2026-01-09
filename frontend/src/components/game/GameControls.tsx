import Button from '@/components/ui/Button'
import { cn } from '@/lib/utils'

interface GameControlsProps {
  selectedCount: number
  canSubmit: boolean
  canShuffle: boolean
  isSubmitting: boolean
  onSubmit: () => void
  onDeselect: () => void
  onShuffle: () => void
}

export default function GameControls({
  selectedCount,
  canSubmit,
  canShuffle,
  isSubmitting,
  onSubmit,
  onDeselect,
  onShuffle,
}: GameControlsProps) {
  return (
    <div className="flex flex-wrap justify-center gap-3">
      <Button
        variant="outline"
        onClick={onShuffle}
        disabled={!canShuffle || isSubmitting}
      >
        Shuffle
      </Button>
      <Button
        variant="outline"
        onClick={onDeselect}
        disabled={selectedCount === 0 || isSubmitting}
      >
        Deselect All
      </Button>
      <Button
        variant="primary"
        onClick={onSubmit}
        disabled={!canSubmit || isSubmitting}
        className={cn({
          'opacity-50': !canSubmit,
        })}
      >
        {isSubmitting ? 'Checking...' : 'Submit'}
      </Button>
    </div>
  )
}
