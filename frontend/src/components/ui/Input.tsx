import React from 'react';

type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={`w-full px-3 py-2 font-pixel border-2 border-pixel-border shadow-pixel-sm focus:outline-none focus:shadow-pixel focus:translate-x-[-2px] focus:translate-y-[-2px] transition-all bg-white text-black placeholder-gray-500 ${className}`}
        {...props}
      />
    );
  }
);

Input.displayName = 'Input';

export default Input;
