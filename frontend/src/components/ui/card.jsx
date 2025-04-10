import React from "react";

export const Card = ({ children, className }) => {
  return <div className={`bg-white shadow-lg rounded-xl p-6 ${className}`}>{children}</div>;
};

export const CardContent = ({ children, className }) => {
  return <div className={`p-4 ${className}`}>{children}</div>;
};
