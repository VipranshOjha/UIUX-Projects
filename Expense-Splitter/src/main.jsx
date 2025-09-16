import React from 'react'
import ReactDOM from 'react-dom/client'
import ExpenseSplitterApp from './ExpenseSplitterApp.jsx'
import './index.css'
import { Toaster } from 'react-hot-toast'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ExpenseSplitterApp />
    <Toaster />
  </React.StrictMode>,
)