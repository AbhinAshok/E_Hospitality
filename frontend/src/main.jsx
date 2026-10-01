import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import './styles.css'
import { AuthProvider, useAuth } from './auth'
import { ErrorBoundary, Layout, ProtectedRoute } from './components'
import { Login, Signup, Dashboard, Profile, Appointments, BookAppointment, PaymentPage, MedicalRecords, Prescriptions, Patients, Billing, Resources, Admin, NotFound } from './pages'
import Home from './Home'
function AppRoutes() {
  const { user } = useAuth()
  return <Routes>
    <Route path="/" element={user ? <Navigate to="/dashboard" replace/> : <Home/>}/>
    <Route path="/login" element={user ? <Navigate to="/dashboard" replace/> : <Login/>}/>
    <Route path="/signup" element={user ? <Navigate to="/dashboard" replace/> : <Signup/>}/>
    <Route element={<ProtectedRoute><Layout/></ProtectedRoute>}>
      <Route path="/dashboard" element={<Dashboard/>}/>
      <Route path="/profile" element={<Profile/>}/>
      <Route path="/appointments" element={<Appointments/>}/>
      <Route path="/appointments/new" element={<ProtectedRoute roles={['patient']}><BookAppointment/></ProtectedRoute>}/>
      <Route path="/appointments/:id/payment" element={<ProtectedRoute roles={['patient']}><PaymentPage/></ProtectedRoute>}/>
      <Route path="/medical-records" element={<MedicalRecords/>}/>
      <Route path="/patients" element={<ProtectedRoute roles={["doctor","admin"]}><Patients/></ProtectedRoute>}/>
      <Route path="/prescriptions" element={<Prescriptions/>}/>
      <Route path="/billing" element={<Billing/>}/>
      <Route path="/resources" element={<Resources/>}/>
      <Route path="/health-resources" element={<Resources/>}/>
      <Route path="/admin" element={<ProtectedRoute roles={['admin']}><Admin/></ProtectedRoute>}/>
    </Route>
    <Route path="*" element={<NotFound/>}/>
  </Routes>
}
ReactDOM.createRoot(document.getElementById('root')).render(<React.StrictMode><ErrorBoundary><BrowserRouter><AuthProvider><AppRoutes/></AuthProvider></BrowserRouter></ErrorBoundary></React.StrictMode>)
