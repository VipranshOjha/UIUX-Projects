import React, { useState, useEffect } from 'react';

const ExpenseModal = ({ groupData, setGroups, expense, onClose }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [paidBy, setPaidBy] = useState(groupData.members[0]);
  const [split, setSplit] = useState({});

  useEffect(() => {
    if (expense) {
      setDescription(expense.description);
      setAmount(expense.amount);
      setPaidBy(expense.paidBy);
      setSplit(expense.split);
    } else {
      // Default to split equally
      const defaultSplit = groupData.members.reduce((acc, member) => ({ ...acc, [member]: (amount || 0) / groupData.members.length }), {});
      setSplit(defaultSplit);
    }
  }, [expense, amount, groupData]);

  const handleSplitChange = (member, value) => {
    setSplit(prev => ({ ...prev, [member]: parseFloat(value) || 0 }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newExpense = {
      id: expense ? expense.id : Date.now(),
      description,
      amount: parseFloat(amount),
      paidBy,
      split,
      isSettlement: false,
    };

    setGroups(prevGroups => {
      return prevGroups.map(g => {
        if (g.id === groupData.id) {
          const updatedExpenses = expense
            ? g.expenses.map(ex => ex.id === expense.id ? newExpense : ex)
            : [...g.expenses, newExpense];
          return { ...g, expenses: updatedExpenses };
        }
        return g;
      });
    });

    onClose();
  };


  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">{expense ? 'Edit Expense' : 'Add Expense'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-1">Description</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Amount</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Paid By</label>
            <select
              value={paidBy}
              onChange={(e) => setPaidBy(e.target.value)}
              className="w-full p-2 border rounded"
            >
              {groupData.members.map(member => (
                <option key={member} value={member}>{member}</option>
              ))}
            </select>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Split</h3>
            {groupData.members.map(member => (
              <div key={member} className="flex justify-between items-center mb-2">
                <span>{member}</span>
                <input
                  type="number"
                  value={split[member] || ''}
                  onChange={(e) => handleSplitChange(member, e.target.value)}
                  className="w-1/3 p-2 border rounded"
                />
              </div>
            ))}
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 rounded">Cancel</button>
            <button type="submit" className="px-4 py-2 bg-green-500 text-white rounded">Save</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ExpenseModal;