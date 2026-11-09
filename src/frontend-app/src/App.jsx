import { useEffect, useState } from 'react'

// Calls the API on the page's own origin: Vite forwards /api in development and nginx does in
// production, so there are no addresses here and no CORS. Replace this page with your app.
export default function App() {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/status')
      .then((response) => {
        if (!response.ok) throw new Error(`The API answered ${response.status}.`)
        return response.json()
      })
      .then(setStatus)
      .catch((e) => setError(e.message))
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 640, margin: '4rem auto' }}>
      <h1>MLOps App</h1>
      {error && <p>Couldn&apos;t reach the API: {error}</p>}
      {!error && !status && <p>Asking the API...</p>}
      {status && (
        <>
          <p>The API is up. GET /api/status answered:</p>
          <pre>{JSON.stringify(status, null, 2)}</pre>
        </>
      )}
      <p>
        <a href="/api/docs">API docs</a>
      </p>
    </main>
  )
}
