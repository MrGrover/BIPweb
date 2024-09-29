'use client';

import React, { useState } from 'react';

interface RegisterButtonProps {
  text: string;
  className?: string;
}

const RegisterButton: React.FC<RegisterButtonProps> = ({ text, className }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    second_name: '',
    last_name: '',
    age: 18,
    gender: 'M',
    blood_type: 'I',
    email: '',
    password: ''
  });
  const [message, setMessage] = useState('');

  const handleOpenModal = () => {
    setIsModalOpen(true);
    // Отключить прокрутку страницы при открытом модальном окне
    document.body.style.overflow = 'hidden';
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setMessage('');
    // Включить прокрутку страницы при закрытии модального окна
    document.body.style.overflow = 'unset';
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
        const response = await fetch('http://localhost:8000/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (response.ok) {
            setMessage('Registration successful!');
            // Закрытие окна с небольшой задержкой
            setTimeout(() => {
                handleCloseModal();
            }, 1000); // Задержка в 1 секунду (1000 миллисекунд)
        } else {
            // Если data.message является объектом, распарсим его вручную
            if (typeof data.message === 'object') {
                let errorMessages = '';

                for (const key in data.message) {
                    if (data.message.hasOwnProperty(key)) {
                        // Присоединяем все сообщения, разделяя их точкой с пробелом
                        errorMessages += `${data.message[key].join(' ')} `;
                    }
                }

                setMessage(errorMessages.trim() || 'Registration failed');
            } else {
                setMessage(data.message || 'Registration failed');
            }
        }
    } catch (error) {
        console.error(error);
        setMessage('An error occurred.');
    }
};


  return (
    <>
      <button onClick={handleOpenModal} className={className}>
        {text}
      </button>

      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-gray-800 text-white p-8 rounded-lg shadow-lg max-w-sm w-11/12 relative overflow-hidden">
            <h2 className="text-3xl mb-6 text-center font-bold">
              Get started with <span className="text-blue-400">HealthForm</span> today
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <input
                type="text"
                name="second_name"
                placeholder="Second Name"
                value={formData.second_name}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <input
                type="number"
                name="age"
                placeholder="Age"
                value={formData.age}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              />
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              >
                <option value="M">Male</option>
                <option value="F">Female</option>
              </select>
              <select
                name="blood_type"
                value={formData.blood_type}
                onChange={handleChange}
                className="w-full p-3 rounded bg-gray-700 text-white placeholder-gray-400 border border-gray-600 focus:outline-none focus:border-blue-500"
              >
                <option value="I">First</option>
                <option value="II">Second</option>
                <option value="III">Third</option>
                <option value="IV">Fourth</option>
              </select>
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
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                >
                  Close
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Register
                </button>
              </div>
            </form>
            {message && <p className="mt-4 text-center text-red-400">{message}</p>}
          </div>
        </div>
      )}
    </>
  );
};

export default RegisterButton;
