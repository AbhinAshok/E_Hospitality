import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { Activity, CalendarDays, CheckCircle2, ClipboardList, Clock3, FileText, HeartPulse, Hospital, Plus, ShieldCheck, Stethoscope, Trash2, Users, WalletCards, CreditCard } from 'lucide-react'
import { Elements, CardElement, useElements, useStripe } from '@stripe/react-stripe-js'
import { loadStripe } from '@stripe/stripe-js'
import api from './api'
import { useAuth } from './auth'
import { Card, Empty, ErrorMessage, PageHeader, Stat } from './components'
import Home from './Home'

function listData(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.data)) return data.data
  return []
}


    


export function Login() {
  const { login } = useAuth(); const nav = useNavigate()
  const [form,setForm]=useState({username:'',password:''}); const [error,setError]=useState(null); const [busy,setBusy]=useState(false)
  const submit=async e=>{e.preventDefault();setBusy(true);setError(null);try{const u=await login(form.username,form.password);nav('/dashboard',{replace:true})}catch(err){setError(err)}finally{setBusy(false)}}
  return <AuthCard title="Welcome back" subtitle="Sign in to your E-Hospitality account"><ErrorMessage error={error}/><form onSubmit={submit}><Field label="Username" value={form.username} onChange={v=>setForm({...form,username:v})}/><Field label="Password" type="password" value={form.password} onChange={v=>setForm({...form,password:v})}/><button className="btn primary full" disabled={busy}>{busy?'Signing in…':'Login'}</button></form><p className="form-foot">New here? <Link to="/signup">Create an account</Link></p></AuthCard>
}

export function Signup() {
  const { register }=useAuth(); const nav=useNavigate()
  const [form,setForm]=useState({username:'',email:'',password:'',password2:'',first_name:'',last_name:'',user_type:'patient'}); const [error,setError]=useState(null);const[busy,setBusy]=useState(false)
  const submit=async e=>{e.preventDefault();setBusy(true);setError(null);try{await register(form);nav('/dashboard',{replace:true})}catch(err){setError(err)}finally{setBusy(false)}}
  return <AuthCard title="Create account" subtitle="Start using E-Hospitality"><ErrorMessage error={error}/><form onSubmit={submit} className="form-grid"><Field label="First name" value={form.first_name} onChange={v=>setForm({...form,first_name:v})}/><Field label="Last name" value={form.last_name} onChange={v=>setForm({...form,last_name:v})}/><Field label="Username" value={form.username} onChange={v=>setForm({...form,username:v})}/><Field label="Email" type="email" value={form.email} onChange={v=>setForm({...form,email:v})}/><Field label="Password" type="password" value={form.password} onChange={v=>setForm({...form,password:v})}/><Field label="Confirm password" type="password" value={form.password2} onChange={v=>setForm({...form,password2:v})}/><label>Account type<select value={form.user_type} onChange={e=>setForm({...form,user_type:e.target.value})}><option value="patient">Patient</option><option value="doctor">Doctor</option></select></label><button className="btn primary full span-2" disabled={busy}>{busy?'Creating…':'Create account'}</button></form><p className="form-foot">Already registered? <Link to="/login">Login</Link></p></AuthCard>
}

function AuthCard({title,subtitle,children}) { return <div className="auth-page"><div className="auth-brand"><HeartPulse size={30}/><span>E-Hospitality</span></div><Card className="auth-card"><h1>{title}</h1><p>{subtitle}</p>{children}</Card></div> }
function Field({label,type='text',value,onChange,placeholder=''}) { return <label>{label}<input type={type} value={value} placeholder={placeholder} onChange={e=>onChange(e.target.value)} required/></label> }

export function Dashboard() {
  const {user}=useAuth(); const [stats,setStats]=useState(null)
  useEffect(()=>{api.get('/dashboard/').then(r=>setStats(r.data))},[])
  const isPatient=user.user_type==='patient', isDoctor=user.user_type==='doctor'
  return <><PageHeader title={`${isPatient?'Patient':isDoctor?'Doctor':'Admin'} Dashboard`} subtitle={`Welcome back, ${user.full_name || user.username}.`}/>
    <div className="stats-grid">{isPatient ? <><Stat label="Appointments" value={stats?.appointments} icon={CalendarDays}/><Stat label="Prescriptions" value={stats?.prescriptions} icon={ClipboardList}/><Stat label="Medical records" value={stats?.medical_records} icon={FileText}/><Stat label="Pending bills" value={stats?.pending_bills} icon={WalletCards}/></> : isDoctor ? <><Stat label="Appointments" value={stats?.appointments} icon={CalendarDays}/><Stat label="Patients" value={stats?.patients} icon={Users}/><Stat label="Prescriptions" value={stats?.prescriptions} icon={ClipboardList}/><Stat label="Medical records" value={stats?.medical_records} icon={FileText}/></> : <><Stat label="Users" value={stats?.users} icon={Users}/><Stat label="Doctors" value={stats?.doctors} icon={Stethoscope}/><Stat label="Appointments" value={stats?.appointments} icon={CalendarDays}/><Stat label="Facilities" value={stats?.facilities} icon={Hospital}/></>}</div>
    <div className="quick-grid">{isPatient && <><Quick to="/appointments/new" title="Book appointment" text="Schedule a visit with an available doctor." icon={CalendarDays}/><Quick to="/profile" title="Complete profile" text="Keep your contact and medical details up to date." icon={HeartPulse}/></>}{isDoctor && <><Quick to="/appointments" title="Manage appointments" text="Review your scheduled patient visits." icon={CalendarDays}/><Quick to="/patients" title="Patients" text="Review patient records connected to your appointments." icon={Users}/></>}{user.user_type==='admin'&&<><Quick to="/admin" title="Administration" text="Manage users, doctors, facilities and resources." icon={ShieldCheck}/><Quick to="/appointments" title="All appointments" text="Review appointments across the system." icon={CalendarDays}/></>}</div>
  </>
}
function Quick({to,title,text,icon:Icon}) {return <Link to={to} className="quick card"><span><Icon/></span><div><h3>{title}</h3><p>{text}</p></div></Link>}

export function Profile() {
  const {user}=useAuth(); const endpoint=`/profile/${user.user_type}/`; const [data,setData]=useState({});const[error,setError]=useState(null);const[saved,setSaved]=useState(false)
  useEffect(()=>{api.get(endpoint).then(r=>setData(r.data)).catch(setError)},[])
  const fields=user.user_type==='patient'?['name','age','phone','address','medications','medical_history','treatment_plans']:user.user_type==='doctor'?['name','email','phone_no','phone','specialization','availability']:['department','name','position','employee_id','address','state','postal_code','country']
  const save=async e=>{e.preventDefault();try{const {data:d}=await api.patch(endpoint,data);setData(d);setSaved(true);setTimeout(()=>setSaved(false),2000)}catch(err){setError(err)}}
  return <><PageHeader title="My Profile" subtitle="Update your account information."/><Card><ErrorMessage error={error}/>{saved&&<div className="alert success">Profile updated successfully.</div>}<form className="form-grid" onSubmit={save}>{fields.map(f=><label key={f}>{f.replaceAll('_',' ')}<textarea rows={f.includes('history')||f==='address'||f==='medications'||f==='treatment_plans'||f==='availability'?3:1} value={data[f]??''} onChange={e=>setData({...data,[f]:e.target.value})}/></label>)}<button className="btn primary">Save changes</button></form></Card></>
}

export function Appointments() {
  const { user } = useAuth()
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    try {
      setLoading(true)
      setError(null)
      const { data } = await api.get('/appointments/')
      setItems(listData(data))
    } catch (err) {
      setError(err)
      setItems([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const remove = async (id) => {
    if (!window.confirm('Delete this appointment?')) return
    try {
      await api.delete(`/appointments/${id}/`)
      load()
    } catch (err) {
      setError(err)
    }
  }

  const confirmAppointment = async (id) => {
    try {
      await api.post(`/appointments/${id}/confirm/`)
      await load()
    } catch (err) {
      setError(err)
    }
  }

  return <>
    <PageHeader
      title="Appointments"
      subtitle={user.user_type === 'patient' ? 'Your upcoming and previous appointments.' : 'Appointments assigned to you.'}
      action={user.user_type === 'patient' && <Link className="btn primary" to="/appointments/new"><Plus size={17}/> Book appointment</Link>}
    />
    <ErrorMessage error={error}/>
    {loading ? <Card><div className="screen-center compact"><div className="spinner"/><p>Loading appointments...</p></div></Card> :
      <Card>
        <Table
          headers={['Patient','Doctor','Date','Time','Fee','Payment','Status','Actions']}
          rows={items.map(a => [
            a.patient?.full_name || a.patient?.username || '—',
            a.doctor_name || '—',
            a.date || '—',
            a.time || '—',
            `₹${Number(a.fee || 0).toFixed(2)}`,
            a.payment_status || 'NotStarted',
            a.status || '—',
            <div className="actions" key={`actions-${a.id}`}>
              {user.user_type === 'patient' && a.payment_status !== 'Paid' && a.status !== 'Canceled' && (
                <Link className="btn small primary" to={`/appointments/${a.id}/payment`}>
                  <CreditCard size={15}/> Pay
                </Link>
              )}
              {user.user_type === 'patient' && a.status === 'Scheduled' && a.payment_status === 'Paid' && (
                <button className="btn small success" onClick={() => confirmAppointment(a.id)}>Confirm</button>
              )}
              {user.user_type === 'admin' && <button className="icon-btn danger" onClick={() => remove(a.id)}><Trash2 size={16}/></button>}
              {user.user_type === 'doctor' && <Link className="btn small" to={`/prescriptions?patient=${a.patient?.id || ''}`}>Prescribe</Link>}
            </div>
          ])}
        />
        {!items.length && <Empty>No appointments found.</Empty>}
      </Card>}
  </>
}

export function BookAppointment() {
  const [doctors, setDoctors] = useState([])
  const [form, setForm] = useState({doctor:'', date:'', time:'', appointment_notes:'', duration_minutes:30, is_virtual:false, location:''})
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)
  const nav = useNavigate()

  useEffect(() => {
    api.get('/doctors/').then(r => setDoctors(listData(r.data))).catch(setError)
  }, [])

  const selectedDoctor = doctors.find(d => String(d.id) === String(form.doctor))
  const consultationFee = Number(selectedDoctor?.consultation_fee || 0)

  const submit = async e => {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const { data } = await api.post('/appointments/', {
        ...form,
        doctor: Number(form.doctor),
        duration_minutes: Number(form.duration_minutes),
      })
      nav(`/appointments/${data.id}/payment`)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return <>
    <PageHeader title="Book an Appointment" subtitle="Choose a doctor and a convenient time. Payment is required before confirmation."/>
    <Card>
      <ErrorMessage error={error}/>
      <form className="form-grid" onSubmit={submit}>
        <label>
          Doctor
          <select required value={form.doctor} onChange={e => setForm({...form, doctor:e.target.value})}>
            <option value="">Select doctor</option>
            {doctors.map(d => <option key={d.id} value={d.id}>
              {d.name || d.user?.full_name || d.user?.username} · {d.specialization || 'General'}
            </option>)}
          </select>
        </label>

        <Field label="Date" type="date" value={form.date} onChange={v => setForm({...form,date:v})}/>
        <Field label="Time" type="time" value={form.time} onChange={v => setForm({...form,time:v})}/>
        <Field label="Duration (minutes)" type="number" value={form.duration_minutes} onChange={v => setForm({...form,duration_minutes:v})}/>

        <div className="payment-summary span-2">
          <span>
            <b>Consultation fee</b>
            <small>The fee is set by the selected doctor.</small>
          </span>
          <strong>{selectedDoctor ? `₹${consultationFee.toFixed(2)}` : 'Select a doctor'}</strong>
        </div>

        <label className="span-2">Notes<textarea value={form.appointment_notes} onChange={e=>setForm({...form,appointment_notes:e.target.value})}/></label>
        <label className="check"><input type="checkbox" checked={form.is_virtual} onChange={e=>setForm({...form,is_virtual:e.target.checked})}/> Virtual appointment</label>
        <Field label="Location" value={form.location} onChange={v=>setForm({...form,location:v})}/>

        <button className="btn primary" disabled={busy || !selectedDoctor}>
          {busy ? 'Creating appointment…' : 'Continue to payment'}
        </button>
      </form>
    </Card>
  </>
}

function PaymentForm({ appointment, onPaid }) {
  const stripe = useStripe()
  const elements = useElements()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  const submit = async e => {
    e.preventDefault()
    if (!stripe || !elements) return

    setBusy(true)
    setError(null)

    try {
      const card = elements.getElement(CardElement)
      if (!card) throw new Error('Payment card form is not ready.')

      const result = await stripe.createToken(card)
      if (result.error) {
        setError({response:{data:{detail:result.error.message}}})
        return
      }

      const { data } = await api.post(`/appointments/${appointment.id}/pay/`, {
        stripeToken: result.token.id,
      })

      const paymentStatus = data.payment_status || data.status || data.payment?.status
      if (paymentStatus === 'Paid' || data.success === true || data.paid === true) {
        onPaid(data)
        return
      }

      if (data.checkout_url || data.payment_url || data.url) {
        window.location.href = data.checkout_url || data.payment_url || data.url
        return
      }

      throw new Error(data.detail || 'Payment was not completed.')
    } catch (err) {
      setError(err instanceof Error ? {response:{data:{detail:err.message}}} : err)
    } finally {
      setBusy(false)
    }
  }

  return <form onSubmit={submit}>
    <div className="stripe-card-element">
      <CardElement options={{hidePostalCode: false}} />
    </div>
    <ErrorMessage error={error}/>
    <button className="btn primary full payment-submit" disabled={!stripe || busy}>
      {busy ? 'Processing payment…' : `Pay ₹${Number(appointment.fee || 0).toFixed(2)}`}
    </button>
  </form>
}

export function PaymentPage() {
  const { id } = useParams()
  const [appointment, setAppointment] = useState(null)
  const [publishableKey] = useState(import.meta.env.VITE_STRIPE_PUBLIC_KEY || '')
  const [stripeInstance, setStripeInstance] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const nav = useNavigate()

  useEffect(() => {
    let mounted = true
    const init = async () => {
      try {
        const { data } = await api.get(`/appointments/${id}/`)
        if (!mounted) return
        setAppointment(data)
        if (data.payment_status === 'Paid') {
          setLoading(false)
          return
        }
        if (publishableKey) {
          const instance = await loadStripe(publishableKey)
          if (mounted) setStripeInstance(instance)
        }
      } catch (err) {
        if (mounted) setError(err)
      } finally {
        if (mounted) setLoading(false)
      }
    }
    init()
    return () => { mounted = false }
  }, [id, publishableKey])

  const handlePaid = async () => {
    try {
      const { data } = await api.get(`/appointments/${id}/`)
      if (data.payment_status === 'Paid') {
        setAppointment(data)
      } else {
        setAppointment(prev => ({...prev, ...data, payment_status:'Paid'}))
      }
    } catch {
      setAppointment(prev => ({...prev, payment_status:'Paid'}))
    }
  }

  if (loading) return <><PageHeader title="Appointment Payment" subtitle="Preparing your secure payment."/><Card><div className="screen-center compact"><div className="spinner"/><p>Preparing payment…</p></div></Card></>

  if (error) return <><PageHeader title="Appointment Payment" subtitle="We could not load the appointment."/><Card><ErrorMessage error={error}/><Link className="btn ghost" to="/appointments">Back to appointments</Link></Card></>

  if (!appointment) return <><PageHeader title="Appointment Payment" subtitle="Appointment not found."/><Card><p>The appointment could not be loaded.</p><Link className="btn ghost" to="/appointments">Back to appointments</Link></Card></>

  if (appointment.payment_status === 'Paid') return <><PageHeader title="Payment complete" subtitle="Your appointment payment has been completed."/><Card><div className="payment-success"><CheckCircle2 size={48}/><h2>Payment successful</h2><p>Your appointment is paid. The appointment can now be confirmed.</p><Link className="btn primary" to="/appointments">View appointments</Link></div></Card></>

  if (appointment.status === 'Canceled') return <><PageHeader title="Appointment canceled" subtitle="This appointment cannot be paid."/><Card><p>Please return to appointments and choose another appointment.</p><Link className="btn ghost" to="/appointments">Back to appointments</Link></Card></>

  if (!publishableKey || !stripeInstance) return <><PageHeader title="Appointment Payment" subtitle={`Pay ₹${Number(appointment.fee || 0).toFixed(2)} for your appointment.`}/><Card><ErrorMessage error={{response:{data:{detail:'Stripe is not configured. Add VITE_STRIPE_PUBLIC_KEY to frontend/.env and restart Vite.'}}}}/><Link className="btn ghost" to="/appointments">Back to appointments</Link></Card></>

  return <>
    <PageHeader title="Secure Payment" subtitle={`Pay ₹${Number(appointment.fee || 0).toFixed(2)} for your appointment with ${appointment.doctor_name || 'your doctor'}.`}/>
    <Card>
      <div className="payment-card">
        <div className="payment-summary">
          <span><b>Appointment fee</b><small>{appointment.date} at {appointment.time}</small></span>
          <strong>₹{Number(appointment.fee || 0).toFixed(2)}</strong>
        </div>
        <Elements stripe={stripeInstance} options={{appearance:{theme:'stripe'}}}>
          <PaymentForm appointment={appointment} onPaid={handlePaid}/>
        </Elements>
      </div>
    </Card>
  </>
}

export function Patients() {
  const [items,setItems]=useState([]); const [error,setError]=useState(null)
  useEffect(()=>{api.get('/patients/').then(r=>setItems(listData(r.data))).catch(setError)},[])
  return <><PageHeader title="Patients" subtitle="Patients associated with your care."/><ErrorMessage error={error}/><Card><Table headers={['Patient','Email','Role']} rows={items.map(p=>[p.full_name||p.username,p.email||'—',p.user_type])}/></Card></>
}

export function MedicalRecords() {
  const {user}=useAuth();const [items,setItems]=useState([]);const[error,setError]=useState(null);const[show,setShow]=useState(false);const[patients,setPatients]=useState([]);const[form,setForm]=useState({patient_id:'',diagnosis:'',treatment_plan:'',medications:'',allergies:''})
  const load=()=>api.get('/medical-records/').then(r=>setItems(listData(r.data))).catch(setError);useEffect(()=>{load();if(user.user_type==='doctor')api.get('/patients/').then(r=>setPatients(listData(r.data)))},[])
  const save=async e=>{e.preventDefault();try{await api.post('/medical-records/',form);setShow(false);load()}catch(err){setError(err)}}
  return <><PageHeader title="Medical Records" subtitle="Clinical history and treatment records." action={user.user_type==='doctor'&&<button className="btn primary" onClick={()=>setShow(!show)}><Plus size={17}/> Add record</button>}/>{show&&<Card><form className="form-grid" onSubmit={save}><label>Patient<select required value={form.patient_id} onChange={e=>setForm({...form,patient_id:e.target.value})}><option value="">Select patient</option>{patients.map(p=><option key={p.id} value={p.id}>{p.full_name||p.username}</option>)}</select></label><Field label="Diagnosis" value={form.diagnosis} onChange={v=>setForm({...form,diagnosis:v})}/><label>Treatment plan<textarea required value={form.treatment_plan} onChange={e=>setForm({...form,treatment_plan:e.target.value})}/></label><Field label="Medications" value={form.medications} onChange={v=>setForm({...form,medications:v})}/><Field label="Allergies" value={form.allergies} onChange={v=>setForm({...form,allergies:v})}/><button className="btn primary">Save record</button></form></Card>}<ErrorMessage error={error}/><Card><Table headers={['Patient','Doctor','Diagnosis','Treatment','Created']} rows={items.map(r=>[r.patient?.full_name||r.patient?.username,r.doctor_name,r.diagnosis,r.treatment_plan,new Date(r.created_at).toLocaleDateString()])}/></Card></>
}

export function Prescriptions() {
  const {user}=useAuth(); const [searchParams]=useSearchParams();const [items,setItems]=useState([]);const[error,setError]=useState(null);const[patients,setPatients]=useState([]);const[show,setShow]=useState(false);const[form,setForm]=useState({patient_id:'',medication_name:'',dosage_instructions:'',medicines:''})
  const load=()=>api.get('/prescriptions/').then(r=>setItems(listData(r.data))).catch(setError);useEffect(()=>{load();if(user.user_type==='doctor')api.get('/patients/').then(r=>{const ps=listData(r.data);setPatients(ps);setForm(f=>({...f,patient_id:searchParams.get('patient')||f.patient_id}))})},[])
  const save=async e=>{e.preventDefault();try{await api.post('/prescriptions/',form);setShow(false);load()}catch(err){setError(err)}}
  return <><PageHeader title="Prescriptions" subtitle="Medication and dosage instructions." action={user.user_type==='doctor'&&<button className="btn primary" onClick={()=>setShow(!show)}><Plus size={17}/> Prescribe</button>}/>{show&&<Card><form className="form-grid" onSubmit={save}><label>Patient<select required value={form.patient_id} onChange={e=>setForm({...form,patient_id:e.target.value})}><option value="">Select patient</option>{patients.map(p=><option key={p.id} value={p.id}>{p.full_name||p.username}</option>)}</select></label><Field label="Medication" value={form.medication_name} onChange={v=>setForm({...form,medication_name:v})}/><label>Dosage instructions<textarea required value={form.dosage_instructions} onChange={e=>setForm({...form,dosage_instructions:e.target.value})}/></label><label>Medicines<textarea value={form.medicines} onChange={e=>setForm({...form,medicines:e.target.value})}/></label><button className="btn primary">Save prescription</button></form></Card>}<ErrorMessage error={error}/><div className="record-grid">{items.map(p=><Card key={p.id}><span className="eyebrow">PRESCRIPTION</span><h3>{p.medication_name}</h3><p><b>Patient:</b> {p.patient?.full_name||p.patient?.username}</p><p><b>Doctor:</b> {p.doctor_name}</p><p>{p.dosage_instructions}</p>{p.medicines&&<p>{p.medicines}</p>}</Card>)}{!items.length&&<Empty/>}</div></>
}

export function Billing() {
  const [items,setItems]=useState([]);const[error,setError]=useState(null);useEffect(()=>{api.get('/billing/').then(r=>setItems(listData(r.data))).catch(setError)},[])
  return <><PageHeader title="Billing" subtitle="View your healthcare billing history."/><ErrorMessage error={error}/><Card><Table headers={['Issued','Amount','Status','Payment date']} rows={items.map(b=>[new Date(b.date_issued).toLocaleDateString(),`₹${Number(b.total_amount || 0).toFixed(2)}`,b.payment_status,b.payment_date?new Date(b.payment_date).toLocaleDateString():'—'])}/></Card></>
}

export function Resources() {
  const { user } = useAuth()
  const [items, setItems] = useState([])
  const [form, setForm] = useState({ title: '', description: '', link: '' })
  const [show, setShow] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const load = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.get('/resources/')
      setItems(listData(response.data))
    } catch (err) {
      console.error('Health resources API error:', err)
      setItems([])
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const resetForm = () => {
    setForm({ title: '', description: '', link: '' })
    setEditingId(null)
    setShow(false)
  }

  const save = async (e) => {
    e.preventDefault()
    try {
      setSaving(true)
      setError(null)
      const payload = { ...form, link: form.link.trim() || null }
      if (editingId) {
        await api.patch(`/resources/${editingId}/`, payload)
      } else {
        await api.post('/resources/', payload)
      }
      resetForm()
      await load()
    } catch (err) {
      console.error('Save resource error:', err)
      setError(err)
    } finally {
      setSaving(false)
    }
  }

  const editResource = (resource) => {
    setEditingId(resource.id)
    setForm({
      title: resource.title || '',
      description: resource.description || '',
      link: resource.link || ''
    })
    setShow(true)
  }

  const deleteResource = async (id) => {
    if (!window.confirm('Delete this health resource?')) return
    try {
      await api.delete(`/resources/${id}/`)
      await load()
    } catch (err) {
      console.error('Delete resource error:', err)
      setError(err)
    }
  }

  return <>
    <PageHeader
      title="Health Resources"
      subtitle="Educational content for healthier decisions."
      action={user.user_type === 'admin' && <button className="btn primary" onClick={() => { resetForm(); setShow(true) }}><Plus size={17}/> Add resource</button>}
    />

    <ErrorMessage error={error}/>

    {show && user.user_type === 'admin' && <Card>
      <div className="page-header inner-header">
        <div><h2>{editingId ? 'Edit Resource' : 'Add Health Resource'}</h2><p>Provide a useful educational resource for users.</p></div>
        <button type="button" className="btn ghost" onClick={resetForm}>Cancel</button>
      </div>
      <form className="form-grid" onSubmit={save}>
        <Field label="Title" value={form.title} onChange={v => setForm({...form, title: v})}/>
        <Field label="Link" type="url" value={form.link} onChange={v => setForm({...form, link: v})} placeholder="https://example.com/article"/>
        <label className="span-2">Description<textarea required rows="5" value={form.description} onChange={e => setForm({...form, description: e.target.value})}/></label>
        <div className="actions span-2"><button className="btn primary" disabled={saving}>{saving ? 'Saving...' : editingId ? 'Update resource' : 'Add resource'}</button></div>
      </form>
    </Card>}

    {loading ? <Card><div className="screen-center compact"><div className="spinner"/><p>Loading health resources...</p></div></Card> :
      items.length ? <div className="record-grid">{items.map(resource => <Card key={resource.id}>
        <span className="eyebrow">HEALTH RESOURCE</span>
        <h3>{resource.title}</h3>
        <p>{resource.description}</p>
        {resource.link && <a href={resource.link} target="_blank" rel="noreferrer">Read resource →</a>}
        {user.user_type === 'admin' && <div className="actions resource-actions">
          <button className="btn small" onClick={() => editResource(resource)}>Edit</button>
          <button className="btn small danger-btn" onClick={() => deleteResource(resource.id)}>Delete</button>
        </div>}
      </Card>)}</div> : <Card><Empty>No health resources have been added yet.</Empty></Card>}
  </>
}

export function Admin() {
  const [data,setData]=useState(null);const[users,setUsers]=useState([]);const[doctors,setDoctors]=useState([]);const[facilities,setFacilities]=useState([]);const[error,setError]=useState(null)
  const load=async()=>{try{const [d,u,dr,f]=await Promise.all([api.get('/admin/dashboard/'),api.get('/users/'),api.get('/admin/doctors/'),api.get('/facilities/')]);setData(d.data);setUsers(u.data.results||u.data);setDoctors(dr.data.results||dr.data);setFacilities(f.data.results||f.data)}catch(e){setError(e)}};useEffect(()=>{load()},[])
  const delDoctor=async id=>{if(confirm('Remove this doctor?')){await api.delete(`/admin/doctors/${id}/`);load()}}
  return <><PageHeader title="Administration" subtitle="Manage the platform's operational data."/><ErrorMessage error={error}/><div className="stats-grid"><Stat label="Users" value={data?.users} icon={Users}/><Stat label="Patients" value={data?.patients} icon={Users}/><Stat label="Doctors" value={data?.doctors} icon={Stethoscope}/><Stat label="Pending bills" value={data?.pending_bills} icon={WalletCards}/></div><div className="admin-grid"><Card><h2>Users</h2><Table headers={['Username','Email','Role']} rows={users.map(u=>[u.username,u.email||'—',u.user_type])}/></Card><Card><h2>Doctors</h2><Table headers={['Name','Specialization','Action']} rows={doctors.map(d=>[d.name||d.user?.username,d.specialization||'—',<button className="icon-btn danger" onClick={()=>delDoctor(d.id)}><Trash2 size={16}/></button>])}/></Card><Card><h2>Facilities</h2><Table headers={['Name','Department','Available']} rows={facilities.map(f=>[f.name,f.department,f.resource_available?'Yes':'No'])}/></Card></div></>
}

export function NotFound(){return <div className="screen-center"><div><h1>404</h1><p>Page not found.</p><Link to="/dashboard" className="btn primary">Go to dashboard</Link></div></div>}
function Table({headers,rows}){return <div className="table-wrap"><table><thead><tr>{headers.map(h=><th key={h}>{h}</th>)}</tr></thead><tbody>{rows.length?rows.map((row,i)=><tr key={i}>{row.map((c,j)=><td key={j}>{c}</td>)}</tr>):<tr><td colSpan={headers.length}><Empty/></td></tr>}</tbody></table></div>}
