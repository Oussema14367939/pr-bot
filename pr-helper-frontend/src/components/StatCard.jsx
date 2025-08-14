// src/components/StatCard.jsx
import React from "react";

const StatCard = ({ title, value, icon, color }) => {
  return (
    <div
      className={`flex items-center p-4 rounded-2xl shadow-md text-white ${color}`}
    >
      <div className="text-3xl mr-4">{icon}</div>
      <div>
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
};

export default StatCard;
