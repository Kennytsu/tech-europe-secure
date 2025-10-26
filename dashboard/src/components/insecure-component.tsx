'use client'

/**
 * SECURITY ISSUE: This component intentionally contains XSS vulnerabilities
 * DO NOT USE IN PRODUCTION!
 * 
 * This is for the Aikido Security Challenge demonstration.
 */

import { useState } from 'react'
import { apiClient } from '@/lib/api'

export function InsecureComponent() {
  const [userInput, setUserInput] = useState('')
  const [comments, setComments] = useState<string[]>([])
  const [apiKey, setApiKey] = useState('')

  // SECURITY ISSUE: No input validation or sanitization
  const handleSubmit = () => {
    setComments([...comments, userInput])
    setUserInput('')
  }

  // SECURITY ISSUE: No authentication or authorization
  const handleGetSecrets = async () => {
    try {
      const response = await fetch('http://localhost:8000/secrets')
      const data = await response.json()
      setApiKey(JSON.stringify(data))
    } catch (error) {
      console.error(error)
    }
  }

  // SECURITY ISSUE: Directly injecting user input into HTML (XSS vulnerability)
  const renderComment = (comment: string, index: number) => {
    return (
      <div key={index}>
        {/* INSECURE - dangerouslySetInnerHTML allows XSS */}
        <div dangerouslySetInnerHTML={{ __html: comment }} />
      </div>
    )
  }

  // SECURITY ISSUE: Using eval() - EXTREMELY DANGEROUS
  const executeCode = (code: string) => {
    try {
      // INSECURE - eval() can execute arbitrary JavaScript
      const result = eval(code)
      alert(`Result: ${result}`)
    } catch (error) {
      alert(`Error: ${error}`)
    }
  }

  // SECURITY ISSUE: Insecure localStorage access
  const saveToLocalStorage = (key: string, value: string) => {
    // INSECURE - No validation, can store sensitive data
    localStorage.setItem(key, value)
  }

  // SECURITY ISSUE: Exposing sensitive data
  const getLocalStorageData = () => {
    // INSECURE - Exposing all localStorage data
    const allData: Record<string, string> = {}
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key) {
        allData[key] = localStorage.getItem(key) || ''
      }
    }
    return allData
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-red-600">
        ⚠️ SECURITY ISSUE: Insecure Component
      </h2>
      
      {/* XSS Vulnerability */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">XSS Vulnerability Test</h3>
        <p className="text-sm text-gray-600 mb-2">
          Try injecting: {'<'}script{'>'}alert('XSS'){'{'}{'</'}script{'>'}
        </p>
        <textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Enter your comment (or XSS payload)..."
          className="w-full p-2 border"
        />
        <button
          onClick={handleSubmit}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Submit Comment
        </button>
        <div className="mt-4">
          <h4>Comments (with XSS vulnerability):</h4>
          {comments.map((comment, index) => renderComment(comment, index))}
        </div>
      </div>

      {/* Exposed API Keys */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">Exposed Secrets</h3>
        <button
          onClick={handleGetSecrets}
          className="px-4 py-2 bg-red-500 text-white rounded mb-2"
        >
          Get API Secrets
        </button>
        {apiKey && (
          <pre className="bg-gray-100 p-2 text-xs overflow-auto">
            {apiKey}
          </pre>
        )}
      </div>

      {/* Code Execution (eval) */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">Code Execution (eval)</h3>
        <p className="text-sm text-gray-600 mb-2">
          INSECURE: Try: alert('Hacked!')
        </p>
        <input
          type="text"
          placeholder="Enter JavaScript code..."
          className="w-full p-2 border"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              executeCode((e.target as HTMLInputElement).value)
            }
          }}
        />
      </div>

      {/* localStorage Exposure */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">localStorage Exposure</h3>
        <button
          onClick={() => {
            alert(JSON.stringify(getLocalStorageData(), null, 2))
          }}
          className="px-4 py-2 bg-yellow-500 text-white rounded"
        >
          Show All LocalStorage Data
        </button>
        <button
          onClick={() => saveToLocalStorage('password', 'admin123')}
          className="ml-2 px-4 py-2 bg-yellow-500 text-white rounded"
        >
          Store Password in LocalStorage
        </button>
      </div>

      {/* Insecure Redirect */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">Insecure Redirect (Open Redirect)</h3>
        <input
          type="text"
          placeholder="Enter URL to redirect to..."
          className="w-full p-2 border"
          id="redirect-url"
        />
        <button
          onClick={() => {
            const url = (document.getElementById('redirect-url') as HTMLInputElement).value
            // INSECURE - No URL validation, open redirect vulnerability
            window.location.href = url
          }}
          className="mt-2 px-4 py-2 bg-purple-500 text-white rounded"
        >
          Redirect
        </button>
      </div>

      {/* Insecure Authentication */}
      <div className="mb-6 p-4 border-2 border-red-500">
        <h3 className="font-bold mb-2">Insecure Authentication</h3>
        <input
          type="text"
          placeholder="Username"
          className="w-full p-2 border mb-2"
          id="username"
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border mb-2"
          id="password"
        />
        <button
          onClick={() => {
            const username = (document.getElementById('username') as HTMLInputElement).value
            const password = (document.getElementById('password') as HTMLInputElement).value
            // INSECURE - No authentication, just checks hardcoded credentials
            if (username === 'admin' && password === 'admin123') {
              alert('Logged in!')
              // INSECURE - Password in localStorage
              localStorage.setItem('user', JSON.stringify({ username, password }))
            } else {
              alert('Invalid credentials')
            }
          }}
          className="px-4 py-2 bg-green-500 text-white rounded"
        >
          Login
        </button>
      </div>

      <div className="mt-8 p-4 bg-red-100 border-2 border-red-500 rounded">
        <p className="text-sm font-bold text-red-800">
          ⚠️ WARNING: This component contains intentional security vulnerabilities
          for educational purposes and the Aikido Security Challenge.
          DO NOT USE ANY OF THIS CODE IN PRODUCTION!
        </p>
      </div>
    </div>
  )
}
