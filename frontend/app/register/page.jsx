"use client";
import RegisterForm from "../components/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-4">
      <div className="py-8">
        <RegisterForm />
      </div>
    </main>
  );
}