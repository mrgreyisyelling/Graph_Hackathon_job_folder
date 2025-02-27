"use client";  // ✅ Add this at the top

import { useState } from "react";
import Button from "@/components/ui/Button";  // ✅ Fix: Import the actual Button component


export default function Forms() {
  const [message, setMessage] = useState("");

  const handleSubmit = async (type) => {
    const data = { exampleField: "Sample Data" };

    try {
      const response = await fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, data }),
      });

      const result = await response.json();
      setMessage(result.message);
    } catch (error) {
      console.error("Error submitting form:", error);
      setMessage("Submission failed");
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-6">
      <h2 className="text-xl font-semibold">Forms</h2>

      <form onSubmit={(e) => e.preventDefault()}>
        <h3 className="text-lg font-medium">Add Daycare</h3>
        <Button type="button" onClick={() => handleSubmit("daycare")}>
          Submit Daycare
        </Button>
      </form>

      <form onSubmit={(e) => e.preventDefault()}>
        <h3 className="text-lg font-medium">Add Location</h3>
        <Button type="button" onClick={() => handleSubmit("location")}>
          Submit Location
        </Button>
      </form>

      <form onSubmit={(e) => e.preventDefault()}>
        <h3 className="text-lg font-medium">Create Entity-Attribute-Value</h3>
        <Button type="button" onClick={() => handleSubmit("eav")}>
          Submit Entity-Attribute-Value
        </Button>
      </form>

      <form onSubmit={(e) => e.preventDefault()}>
        <h3 className="text-lg font-medium">Create Entity</h3>
        <Button type="button" onClick={() => handleSubmit("entity")}>
          Submit Entity
        </Button>
      </form>

      {message && <p className="mt-4 text-green-500">{message}</p>}
    </div>
  );
}
