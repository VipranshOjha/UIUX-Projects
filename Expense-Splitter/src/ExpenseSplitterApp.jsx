import React, { useState, useEffect, useMemo } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MainDashboard from './components/MainDashboard';
import CreateGroupModal from './components/CreateGroupModal';
import ExpenseModal from './components/ExpenseModal';

const ExpenseSplitterApp = () => {
    const [loading, setLoading] = useState(true);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [groupData, setGroupData] = useState(null);
    const [showCreateGroup, setShowCreateGroup] = useState(false);
    const [showAddExpense, setShowAddExpense] = useState(false);
    const [editingExpense, setEditingExpense] = useState(null);
    const [sidebarOpen, setSidebarOpen] = useState(false);

    useEffect(() => {
        const initApp = async () => {
            await new Promise(resolve => setTimeout(resolve, 1500));
            setLoading(false);
        };
        initApp();
    }, []);

    useEffect(() => {
        if (!selectedGroup) {
            setGroupData(null);
            return;
        }
        const currentGroupData = groups.find(g => g.id === selectedGroup);
        if (currentGroupData) {
            setGroupData(currentGroupData);
        }
    }, [selectedGroup, groups]);

    const simplifiedDebts = useMemo(() => {
        if (!groupData || !groupData.expenses || !groupData.members) return [];
        const balances = groupData.members.reduce((acc, member) => ({ ...acc, [member]: 0 }), {});
        groupData.expenses.forEach(expense => {
            const { amount, paidBy, split } = expense;
            if (balances[paidBy] !== undefined) {
                balances[paidBy] += amount;
            }
            Object.entries(split).forEach(([member, owedAmount]) => {
                if (balances[member] !== undefined) {
                    balances[member] -= owedAmount;
                }
            });
        });
        const creditors = [];
        const debtors = [];
        Object.entries(balances).forEach(([member, balance]) => {
            if (balance > 0.01) creditors.push({ member, amount: balance });
            else if (balance < -0.01) debtors.push({ member, amount: -balance });
        });
        creditors.sort((a, b) => b.amount - a.amount);
        debtors.sort((a, b) => b.amount - a.amount);
        const transfers = [];
        let i = 0, j = 0;
        while (i < creditors.length && j < debtors.length) {
            const transferAmount = Math.min(creditors[i].amount, debtors[j].amount);
            if (transferAmount > 0.01) {
                transfers.push({
                    from: debtors[j].member,
                    to: creditors[i].member,
                    amount: transferAmount
                });
            }
            creditors[i].amount -= transferAmount;
            debtors[j].amount -= transferAmount;
            if (creditors[i].amount < 0.01) i++;
            if (debtors[j].amount < 0.01) j++;
        }
        return transfers;
    }, [groupData]);

    const dashboardStats = useMemo(() => {
        if (!groupData || !simplifiedDebts) return { totalOwedToYou: 0, totalYouOwe: 0, totalGroupSpending: 0 };
        const currentUser = groupData.members[0];
        const totalOwedToYou = simplifiedDebts.filter(t => t.to === currentUser).reduce((sum, t) => sum + t.amount, 0);
        const totalYouOwe = simplifiedDebts.filter(t => t.from === currentUser).reduce((sum, t) => sum + t.amount, 0);
        const totalGroupSpending = groupData.expenses.filter(e => !e.isSettlement).reduce((sum, e) => sum + e.amount, 0);
        return { totalOwedToYou, totalYouOwe, totalGroupSpending };
    }, [groupData, simplifiedDebts]);

    useEffect(() => {
        if (!loading && groups.length === 0) {
            setShowCreateGroup(true);
        }
    }, [loading, groups]);

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-stone-50 to-amber-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="relative">
                        <div className="w-20 h-20 rounded-full border-4 border-stone-200 border-t-amber-400 animate-spin"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <span className="h-8 w-8 text-amber-600">💰</span>
                        </div>
                    </div>
                    <p className="mt-6 text-stone-600 font-medium">Setting up your workspace...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-stone-50">
            {sidebarOpen && (
                <div className="fixed inset-0 z-40 lg:hidden">
                    <div className="fixed inset-0 bg-black/30" onClick={() => setSidebarOpen(false)} />
                    <div className="fixed left-0 top-0 bottom-0 w-80 bg-white shadow-2xl">
                        <Sidebar
                            groups={groups}
                            selectedGroup={selectedGroup}
                            onSelectGroup={setSelectedGroup}
                            onCreateGroup={() => { setShowCreateGroup(true); setSidebarOpen(false); }}
                            onClose={() => setSidebarOpen(false)}
                            isMobile={true}
                        />
                    </div>
                </div>
            )}
            <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-80 lg:flex-col">
                <Sidebar
                    groups={groups}
                    selectedGroup={selectedGroup}
                    onSelectGroup={setSelectedGroup}
                    onCreateGroup={() => setShowCreateGroup(true)}
                />
            </div>
            <div className="lg:pl-80">
                <Header 
                    groupData={groupData}
                    onMenuClick={() => setSidebarOpen(true)}
                    onAddExpense={() => setShowAddExpense(true)}
                />
                {groupData ? (
                    <MainDashboard
                        groupData={groupData}
                        simplifiedDebts={simplifiedDebts}
                        dashboardStats={dashboardStats}
                        onAddExpense={() => setShowAddExpense(true)}
                        onEditExpense={setEditingExpense}
                    />
                ) : (
                    <div className="flex items-center justify-center h-96">
                        <div className="text-center">
                            <span className="h-16 w-16 text-stone-400 mx-auto mb-4">👥</span>
                            <p className="text-stone-500 text-lg">Select or create a group to get started</p>
                        </div>
                    </div>
                )}
            </div>
            {showCreateGroup && (
                <CreateGroupModal
                    onClose={() => setShowCreateGroup(false)}
                    onSuccess={(newGroup) => {
                        setGroups(prevGroups => [newGroup, ...prevGroups]);
                        setSelectedGroup(newGroup.id);
                        setShowCreateGroup(false);
                    }}
                />
            )}
            {(showAddExpense || editingExpense) && groupData && (
                <ExpenseModal
                    groupData={groupData}
                    setGroups={setGroups}
                    expense={editingExpense}
                    onClose={() => {
                        setShowAddExpense(false);
                        setEditingExpense(null);
                    }}
                />
            )}
        </div>
    );
};

export default ExpenseSplitterApp;
