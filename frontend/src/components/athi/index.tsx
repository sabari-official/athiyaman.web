/* Athiyaman Platform UI Components */

export const Button = ({ 
  children, 
  onClick, 
  variant = 'primary',
  disabled = false,
  type = 'button',
  className = '',
  isLoading = false,
  ...props 
}: any) => {
  const variants: Record<string, string> = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
  };

  const isBtnDisabled = disabled || isLoading;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={isBtnDisabled}
      className={`px-4 py-2 rounded font-medium transition-colors ${variants[variant]} ${isBtnDisabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      {...props}
    >
      {isLoading ? 'Loading' : children}
    </button>
  );
};

export const Input = ({ 
  label, 
  error, 
  className = '',
  ...props 
}: any) => (
  <div className={`mb-4 ${error ? 'border-red-500' : ''}`}>
    {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
    <input
      className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${error ? 'border-red-500' : ''} ${className}`}
      {...props}
    />
    {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
  </div>
);

export const Card = ({ children, className = '', ...props }: any) => (
  <div className={`bg-white rounded-lg shadow-md p-6 ${className}`} {...props}>
    {children}
  </div>
);

Card.Header = ({ children, className = '', ...props }: any) => (
  <div className={`border-b border-gray-200 pb-4 mb-4 ${className}`} {...props}>
    {children}
  </div>
);

Card.Title = ({ children, className = '', ...props }: any) => (
  <h3 className={`text-lg font-bold ${className}`} {...props}>
    {children}
  </h3>
);

Card.Body = ({ children, className = '', ...props }: any) => (
  <div className={`${className}`} {...props}>
    {children}
  </div>
);

Card.Footer = ({ children, className = '', ...props }: any) => (
  <div className={`border-t border-gray-200 pt-4 mt-4 ${className}`} {...props}>
    {children}
  </div>
);

export const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children,
  size = 'md',
  actions
}: any) => {
  if (!isOpen) return null;

  const sizes: Record<string, string> = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card role="dialog" className={`${sizes[size]} w-full mx-4`}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">{title}</h2>
          <button
            aria-label="Close"
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>
        {children}
        {actions && actions.length > 0 && (
          <div className="flex justify-end gap-2 mt-6">
            {actions.map((act: any, idx: number) => (
              <Button key={idx} variant={act.variant} onClick={act.onClick}>
                {act.label}
              </Button>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export const Alert = ({ 
  type = 'info', 
  title, 
  children, 
  message, 
  dismissible, 
  onClose 
}: any) => {
  const colors: Record<string, string> = {
    info: 'bg-blue-50 text-blue-800',
    success: 'bg-green-50 text-green-800',
    warning: 'bg-yellow-50 text-yellow-800',
    error: 'bg-red-50 text-red-800',
  };

  return (
    <div className={`p-4 rounded-md ${colors[type]} relative flex flex-col gap-1`}>
      {title && <span className="font-bold">{title}</span>}
      <span>{children || message}</span>
      {dismissible && onClose && (
        <button
          aria-label="Close"
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
          role="button"
        >
          ✕
        </button>
      )}
    </div>
  );
};

export const Badge = ({ 
  children, 
  variant = 'default', 
  className = '' 
}: any) => {
  const variants: Record<string, string> = {
    default: 'bg-gray-200 text-gray-800',
    success: 'bg-green-200 text-green-800',
    warning: 'bg-yellow-200 text-yellow-800',
    danger: 'bg-red-200 text-red-800',
  };

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

export const Loading = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

export const Navbar = ({ user, onLogout }: any) => (
  <nav className="bg-white shadow-md">
    <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-blue-600">Athiyaman</h1>
      <div className="flex items-center gap-4">
        {user ? (
          <>
            <span className="text-gray-600">{user.username}</span>
            <Button variant="secondary" onClick={onLogout}>
              Logout
            </Button>
          </>
        ) : (
          <>
            <a href="/login" className="text-blue-600 hover:text-blue-700">Login</a>
            <Button variant="primary">Sign Up</Button>
          </>
        )}
      </div>
    </div>
  </nav>
);

export const Table = ({ columns, data, actions }: any) => (
  <div className="overflow-x-auto">
    <table className="w-full border-collapse border border-gray-300">
      <thead className="bg-gray-100">
        <tr>
          {columns.map((col: any) => (
            <th key={col.key} className="border border-gray-300 p-2 text-left">
              {col.label}
            </th>
          ))}
          {actions && <th className="border border-gray-300 p-2">Actions</th>}
        </tr>
      </thead>
      <tbody>
        {data.map((row: any, idx: number) => (
          <tr key={idx} className="hover:bg-gray-50">
            {columns.map((col: any) => (
              <td key={col.key} className="border border-gray-300 p-2">
                {row[col.key]}
              </td>
            ))}
            {actions && (
              <td className="border border-gray-300 p-2">
                {actions(row)}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export const ProfileGuard = ({ children }: any) => {
  // Placeholder - actual implementation in App.tsx
  return children;
};
