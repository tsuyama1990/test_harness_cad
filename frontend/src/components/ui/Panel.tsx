import React from 'react';

type PanelProps = {
  children: React.ReactNode;
  className?: string;
} & React.HTMLAttributes<HTMLDivElement>;

const Panel: React.FC<PanelProps> = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`bg-surface shadow-md rounded-lg p-4 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Panel;
