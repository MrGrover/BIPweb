'use client';

import React, { useState } from 'react';

import { Button } from './ui/button';
import { useAuth } from '../context/AuthContext';

interface SignInButtonProps {
  text: string;
}

const SignInButton: React.FC<SignInButtonProps> = ({ text }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [message, setMessage] = useState<string>('');
  const { login } = useAuth();

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setMessage('');
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Login successful');
        login({
          firstName: data.firstname,
          lastName: data.lastname,
          email: data.email,
          token: data.token,
          image: ''
        });
        setTimeout(() => {
          handleCloseModal();
        }, 300);
      } else {
        setMessage(data.message || 'Login failed');
      }
    } catch (error) {
      console.error(error);
      setMessage('An error occurred.');
    }
    
    
  };

  return (
    <>
      <Button onClick={handleOpenModal} variant="default" size="default">
        {text}
      </Button>

      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-gray-800 text-white p-8 rounded-lg shadow-lg max-w-md w-full">
            <h2 className="text-3xl mb-6 text-center font-bold">Log in to your account</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <div className="flex justify-between items-center space-x-4">
                <Button
                  type="button"
                  onClick={handleCloseModal}
                  variant="secondary"
                  size="default"
                  className="bg-red-600 text-white hover:bg-red-700"
                >
                  Close
                </Button>
                <Button type="submit" variant="default" size="default">
                  Login
                </Button>
              </div>
            </form>
            {message && <p className="mt-6 text-center text-red-400">{message}</p>}
          </div>
        </div>
      )}
    </>
  );
};

export default SignInButton;
