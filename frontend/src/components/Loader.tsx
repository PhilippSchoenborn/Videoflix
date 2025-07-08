import React from 'react';

const Loader: React.FC = () => (
  <div className="min-h-screen bg-videoflix-black flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-videoflix-red"></div>
  </div>
);

export default Loader;
