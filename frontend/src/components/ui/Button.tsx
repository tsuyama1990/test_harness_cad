import React from 'react';

type ButtonProps = {
  variant?: 'primary' | 'secondary' | 'outline';
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  className = '',
  children,
  ...props
}) => {
  const baseStyles = 'px-4 py-2 font-pixel font-bold uppercase tracking-wide border-2 border-pixel-border shadow-pixel active:shadow-none active:translate-x-[4px] active:translate-y-[4px] transition-all focus:outline-none';

  const variantStyles = {
    primary: 'bg-primary text-white hover:bg-primary-dark',
    secondary: 'bg-white text-black hover:bg-gray-100',
    outline: 'bg-transparent text-primary hover:bg-blue-50',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
