import { Link, NavLink, Navigate, Outlet, useLocation } from 'react-router-dom'
import { Activity, CalendarDays, ClipboardList, FileText, HeartPulse, Home, LogOut, Menu, Stethoscope, UserRound, X } from 'lucide-react'
import React, { useState } from 'react'
import { useAuth } from './auth'

export function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="screen-center"><div className="spinner" /></div>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.user_type)) return <Navigate to="/dashboard" replace />
  return children
}

export function Layout() {
  const { user, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const nav = [
    ['/dashboard', 'Dashboard', Home],
    ['/appointments', 'Appointments', CalendarDays],
    ['/profile', 'Profile', UserRound],
    ['/medical-records', 'Medical Records', FileText],
    ['/prescriptions', 'Prescriptions', ClipboardList],
    ['/billing', 'Billing', Activity],
    ['/resources', 'Health Resources', HeartPulse],
  ]
  if (user?.user_type === 'admin') nav.push(['/admin', 'Administration', Stethoscope])
  return (
    <div className="app-shell">
      <header className="topbar">
        <Link className="brand" to="/dashboard"><span className="brand-mark"><HeartPulse size={20}/></span>E-Hospitality</Link>
        <button className="menu-btn" onClick={() => setOpen(!open)}>{open ? <X/> : <Menu/>}</button>
        <nav className={open ? 'nav open' : 'nav'}>
          {nav.map(([to,label,Icon]) => <NavLink key={to} to={to} onClick={() => setOpen(false)}><Icon size={17}/>{label}</NavLink>)}
          <button className="logout-btn" onClick={logout}><LogOut size={17}/> Logout</button>
        </nav>
      </header>
      <main className="page"><Outlet/></main>
      <footer>E-Hospitality · Healthcare management made simpler</footer>
    </div>
  )
}

export function PageHeader({ title, subtitle, action }) {
  return <div className="page-header"><div><h1>{title}</h1>{subtitle && <p>{subtitle}</p>}</div>{action}</div>
}

export function Card({ children, className='' }) { return <div className={`card ${className}`}>{children}</div> }
export function Stat({ label, value, icon: Icon }) { return <Card className="stat"><span className="stat-icon"><Icon size={21}/></span><div><strong>{value ?? '—'}</strong><small>{label}</small></div></Card> }
export function Empty({ children='No records found.' }) { return <div className="empty">{children}</div> }
export function ErrorMessage({ error }) {
  if (!error) return null
  const msg = error.response?.data?.detail || Object.values(error.response?.data || {}).flat().join(' ') || 'Something went wrong.'
  return <div className="alert error">{msg}</div>
}


export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return <div className="screen-center app-error"><div><h1>Something went wrong</h1><p>The page could not be rendered. Open the browser console for details.</p><button className="btn primary" onClick={() => window.location.reload()}>Reload application</button></div></div>
    }
    return this.props.children
  }
}
