import { cn } from '@/lib/utils'
import type { Category } from '@/lib/types'
import { DIFFICULTY_COLORS } from '@/lib/types'

interface CategoryRowProps {
  category: Category
  animateIn?: boolean
}

export default function CategoryRow({ category, animateIn = false }: CategoryRowProps) {
  const colors = DIFFICULTY_COLORS[category.difficulty]

  return (
    <div
      className={cn(
        'w-full rounded-lg py-4 px-6',
        colors.bg,
        colors.text,
        {
          'animate-bounce-in': animateIn,
        }
      )}
    >
      <div className="text-center">
        <h3 className="font-bold text-lg uppercase tracking-wide mb-1">
          {category.name}
        </h3>
        <p className="text-sm opacity-90">
          {category.words.join(', ')}
        </p>
      </div>
    </div>
  )
}
