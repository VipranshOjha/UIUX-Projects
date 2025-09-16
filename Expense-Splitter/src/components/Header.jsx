import React from 'react';

const Header = ({ groupData, onMenuClick, onAddExpense }) => {
  return (
    <header className="flex justify-between items-center p-4 bg-white shadow-md">
      <button onClick={onMenuClick} className="lg:hidden">Menu</button>
      <div>{groupData ? groupData.name : 'Dashboard'}</div>
      {groupData && (
        <button onClick={onAddExpense} className="bg-green-500 text-white p-2 rounded">
          Add Expense
        </button>
      )}
    </header>
  );
};

export default Header;