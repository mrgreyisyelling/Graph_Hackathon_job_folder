"use client";  // Ensures this is a client component

export default function Button({ children, onClick, type = "button" }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
    >
      {children}
    </button>
  );
}
