import React from 'react';

const MainDashboard = ({ groupData, simplifiedDebts, dashboardStats, onAddExpense, onEditExpense }) => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard for {groupData.name}</h1>
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg">Total Owed to You</h3>
          <p className="text-2xl font-bold">${dashboardStats.totalOwedToYou.toFixed(2)}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg">Total You Owe</h3>
          <p className="text-2xl font-bold">${dashboardStats.totalYouOwe.toFixed(2)}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg">Total Group Spending</h3>
          <p className="text-2xl font-bold">${dashboardStats.totalGroupSpending.toFixed(2)}</p>
        </div>
      </div>
      <div>
        <h2 className="text-xl font-bold mb-2">Debts</h2>
        <ul>
          {simplifiedDebts.map((debt, index) => (
            <li key={index} className="mb-2 p-2 bg-gray-100 rounded">
              {debt.from} owes {debt.to} ${debt.amount.toFixed(2)}
            </li>
          ))}
        </ul>
      </div>
      <button onClick={onAddExpense} className="mt-4 bg-green-500 text-white p-2 rounded">
        Add Expense
      </button>
    </div>
  );
};

export default MainDashboard;