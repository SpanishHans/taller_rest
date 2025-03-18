'use client';

import React, { useState } from "react";
import axios from "axios";

// Define the type for a single libro
type Libro = {
  url_m: string;
  titulo: string;
  autor: string;
  publicado_en: string;
  publicado_por: string;
  isbn: string;
};

export default function LibrosPage() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [libros, setLibros] = useState<Libro[]>([]); // Typed state

  const fetchLibros = async () => {
    try {
      const res = await axios.get<Libro[]>(`http://127.0.0.1:10332/libros`, {
        params: {
          start_date: startDate,
          end_date: endDate,
          limit: 10,
          offset: 0,
        },
      });
      setLibros(res.data);
    } catch (err) {
      console.error("Error fetching libros:", err);
    }
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Libros</h1>

      <div className="space-x-2">
        <input
          type="text"
          placeholder="Start Date (e.g., 1990)"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border p-1 rounded"
        />
        <input
          type="text"
          placeholder="End Date (e.g., 2000)"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border p-1 rounded"
        />
        <button
          onClick={fetchLibros}
          className="bg-blue-500 text-white px-2 py-1 rounded"
        >
          Fetch Libros
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 mt-4">
        {libros.map((libro, index) => (
          <div key={index} className="border p-4 rounded shadow">
            <img src={libro.url_m} alt={libro.titulo} className="mb-2" />
            <h2 className="font-bold">{libro.titulo}</h2>
            <p>{libro.autor}</p>
            <p>Publicado en: {libro.publicado_en}</p>
            <p>Editorial: {libro.publicado_por}</p>
            <p>ISBN: {libro.isbn}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
