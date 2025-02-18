import React from 'react';
import './SplashPage.css'; // We'll create this file next
import UserTable from './UserTable';

const SplashPage: React.FC = () => {
  return (
    <div className="splash-container">
        <h1>User Table</h1>
        <UserTable />
    </div>
  );
};

export default SplashPage;