import { cn } from '@/lib/utils'
import { ButtonHTMLAttributes, forwardRef } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', disabled, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-full font-semibold transition-all',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          {
            // Variants
            'bg-black text-white hover:bg-gray-800 focus:ring-gray-500':
              variant === 'primary',
            'bg-gray-200 text-black hover:bg-gray-300 focus:ring-gray-400':
              variant === 'secondary',
            'border-2 border-black text-black hover:bg-gray-100 focus:ring-gray-500':
              variant === 'outline',
            'text-black hover:bg-gray-100 focus:ring-gray-300':
              variant === 'ghost',
            // Sizes
            'px-4 py-1.5 text-sm': size === 'sm',
            'px-6 py-2 text-base': size === 'md',
            'px-8 py-3 text-lg': size === 'lg',
          },
          className
        )}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button
