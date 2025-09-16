import React from 'react';

const Sidebar = ({ groups, selectedGroup, onSelectGroup, onCreateGroup, onClose, isMobile }) => {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Groups</h2>
      <ul>
        {groups.map(group => (
          <li
            key={group.id}
            className={`cursor-pointer p-2 rounded ${selectedGroup === group.id ? 'bg-gray-200' : ''}`}
            onClick={() => onSelectGroup(group.id)}
          >
            {group.name}
          </li>
        ))}
      </ul>
      <button
        onClick={onCreateGroup}
        className="mt-4 w-full bg-blue-500 text-white p-2 rounded"
      >
        Create Group
      </button>
      {isMobile && <button onClick={onClose} className="mt-2 w-full">Close</button>}
    </div>
  );
};

export default Sidebar;