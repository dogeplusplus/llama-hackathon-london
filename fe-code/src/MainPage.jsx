import React from 'react';
import PdfJs from './PDF/PDF';
import { useState } from 'react'
import AI_features from './AI_scripts/AI_features';
 

export default function MainPage() {
  return (
    <div>
      {/* Full Screen Header */}
      <header
        style={{
          width: '100%',
          height: '10vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: '#000000',
          color: 'white',
          textAlign: 'center',
          padding: '8px',
        }}
      >
        <h1 style={{ fontSize: '2rem' }}> Better understand what you read with an AI-assistant </h1>
        {/* <p style={{ fontSize: '1.rem' }}>
          CHAT with your PDF document
        </p> */}
      </header>

      {/* Full Screen Row with 2 Columns */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '50px 20px',
        }}
      >
        <div
          style={{
            width: '48%',
            padding: '20px',
            backgroundColor: '#f4f4f4',
            borderRadius: '8px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          }}
        >
         <AI_features/>
        </div>

        <div
          style={{
            width: '48%',
            padding: '20px',
            backgroundColor: '#f4f4f4',
            borderRadius: '8px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          }}
        >
        <PdfJs/>
        </div>
      </div>
    </div>
  );
}
