import {
  Activity,
  ArrowRight,
  CalendarDays,
  CreditCard,
  FileText,
  HeartPulse,
  LogIn,
  Menu,
  Stethoscope,
  Users,
  X,
  Clock3,
  BookOpen,
  Info,
  Mail,
} from "lucide-react";

import { Link } from "react-router-dom";
import { useState } from "react";

import "./home.css";

const features = [
  {
    title: "Appointments",
    description: "Schedule and manage doctor visits.",
    icon: CalendarDays,
    image: "/images/ehos_doctor1.jpg",
  },
  {
    title: "Medical records",
    description: "Keep treatment history accessible.",
    icon: Users,
    image: "/images/ehos_patientcare.jpg",
  },
  {
    title: "Prescriptions",
    description: "Review medication instructions securely.",
    icon: FileText,
    image: "/images/ehos_service.jpg",
  },
  {
    title: "Billing",
    description: "Track outstanding and paid bills.",
    icon: CreditCard,
    image: "/images/billing.jpg",
  },
];

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="home-page">

      {/* ================= NAVBAR ================= */}
      <header className="home-navbar">
        <div className="navbar-inner">

          {/* Logo */}
          <Link to="/" className="brand">
            <span className="brand-icon">
              <HeartPulse size={27} />
            </span>

            <span>
              E-<strong>Hospitality</strong>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className={`home-nav ${menuOpen ? "mobile-open" : ""}`}>

            <Link
              to="/"
              className="nav-link active"
              onClick={() => setMenuOpen(false)}
            >
              <Activity size={18} />
              Home
            </Link>

            <a href="#services" className="nav-link">
              <Stethoscope size={18} />
              Services
            </a>

            <a href="#doctors" className="nav-link">
              <Users size={18} />
              Doctors
            </a>

            <a href="#resources" className="nav-link">
              <BookOpen size={18} />
              Resources
            </a>

            <a href="#about" className="nav-link">
              <Info size={18} />
              About
            </a>

            <a href="#contact" className="nav-link">
              <Mail size={18} />
              Contact
            </a>

            <div className="mobile-actions">
              <Link to="/login" className="nav-login">
                <LogIn size={17} />
                Login
              </Link>

              <Link to="/dashboard" className="nav-start">
                Get Started
                <ArrowRight size={17} />
              </Link>
            </div>
          </nav>

          {/* Desktop Actions */}
          <div className="navbar-actions">

            <Link to="/login" className="nav-login">
              <LogIn size={17} />
              Login
            </Link>

            <Link to="/dashboard" className="nav-start">
              Get Started
              <ArrowRight size={17} />
            </Link>

          </div>

          {/* Mobile menu */}
          <button
            className="menu-button"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            {menuOpen ? <X size={25} /> : <Menu size={25} />}
          </button>

        </div>
      </header>


      {/* ================= HERO ================= */}
      <main>

        <section className="hero-section">

          {/* ECG background */}
          <div className="ecg-background">
            <svg
              className="ecg-svg"
              viewBox="0 0 1600 300"
              preserveAspectRatio="none"
            >
              <path
                className="ecg-glow"
                d="
                  M0 160
                  L120 160
                  L145 160
                  L165 125
                  L185 195
                  L215 160
                  L290 160
                  L320 160
                  L350 55
                  L380 260
                  L420 160
                  L500 160
                  L530 160
                  L555 125
                  L575 195
                  L605 160
                  L690 160
                  L720 160
                  L750 85
                  L775 230
                  L810 160
                  L900 160
                  L930 160
                  L960 120
                  L980 200
                  L1010 160
                  L1110 160
                  L1140 160
                  L1170 55
                  L1200 260
                  L1240 160
                  L1340 160
                  L1370 160
                  L1400 120
                  L1420 200
                  L1450 160
                  L1600 160
                "
              />

              <path
                className="ecg-line"
                d="
                  M0 160
                  L120 160
                  L145 160
                  L165 125
                  L185 195
                  L215 160
                  L290 160
                  L320 160
                  L350 55
                  L380 260
                  L420 160
                  L500 160
                  L530 160
                  L555 125
                  L575 195
                  L605 160
                  L690 160
                  L720 160
                  L750 85
                  L775 230
                  L810 160
                  L900 160
                  L930 160
                  L960 120
                  L980 200
                  L1010 160
                  L1110 160
                  L1140 160
                  L1170 55
                  L1200 260
                  L1240 160
                  L1340 160
                  L1370 160
                  L1400 120
                  L1420 200
                  L1450 160
                  L1600 160
                "
              />
            </svg>
          </div>


          {/* Medical crosses */}
          <div className="medical-cross cross-one">+</div>
          <div className="medical-cross cross-two">+</div>
          <div className="medical-cross cross-three">+</div>


          <div className="hero-container">

            {/* LEFT */}
            <div className="hero-content">

              <div className="eyebrow">
                <span className="eyebrow-dot"></span>
                DIGITAL HEALTHCARE PLATFORM
              </div>

              <h1>
                Healthcare management,
                <span> connected.</span>
              </h1>

              <p className="hero-description">
                Book appointments, manage clinical records,
                prescriptions and billing from one secure workspace.
              </p>

              <div className="hero-buttons">

                <Link to="/dashboard" className="primary-button">
                  Get Started
                  <ArrowRight size={20} />
                </Link>

                <Link to="/login" className="secondary-button">
                  Sign in
                </Link>

              </div>

            </div>


            {/* RIGHT INFO CARD */}
            <div className="care-card">

              <div className="care-icon">
                <HeartPulse size={40} />
              </div>

              <h2>One place for care</h2>

              <p>
                Patients, doctors and administrators can work
                from the same platform.
              </p>

              <div className="care-line"></div>

            </div>

          </div>


          {/* Doctor image */}
          <div className="doctor-image-wrapper">
            <img
              src="/images/doctor-heart.png"
              alt="Healthcare professional"
              className="doctor-image"
            />
          </div>


          {/* ================= FEATURES ================= */}
          <div className="features-container" id="services">

            {features.map((feature) => {
              const Icon = feature.icon;

              return (
                <Link
                  to={
                    feature.title === "Appointments"
                      ? "/appointments"
                      : feature.title === "Medical records"
                      ? "/medical-records"
                      : feature.title === "Prescriptions"
                      ? "/prescriptions"
                      : "/billing"
                  }
                  className="feature-card"
                  key={feature.title}
                >

                  <div className="feature-image-wrapper">
                    <img
                      src={feature.image}
                      alt={feature.title}
                      className="feature-image"
                    />
                  </div>

                  <div className="feature-content">

                    <div className="feature-icon">
                      <Icon size={22} />
                    </div>

                    <div>
                      <h3>{feature.title}</h3>

                      <div className="feature-line"></div>

                      <p>{feature.description}</p>
                    </div>

                  </div>

                </Link>
              );
            })}

          </div>


          {/* ================= STATS ================= */}
          <div className="stats-container">

            <Stat
              icon={<Users />}
              number="100+"
              label="Expert Doctors"
            />

            <Stat
              icon={<CalendarDays />}
              number="5000+"
              label="Appointments"
            />

            <Stat
              icon={<HeartPulse />}
              number="3000+"
              label="Happy Patients"
            />

            <Stat
              icon={<Clock3 />}
              number="24/7"
              label="Online Support"
            />

          </div>

        </section>


        {/* ================= ABOUT ================= */}
        <section className="simple-section" id="about">

          <div>
            <span className="section-label">
              ABOUT E-HOSPITALITY
            </span>

            <h2>
              Healthcare management,
              <span> made simple.</span>
            </h2>

            <p>
              E-Hospitality connects patients, doctors and
              administrators through one secure healthcare platform.
            </p>
          </div>

        </section>


        {/* ================= CONTACT ================= */}
        <section className="simple-section contact-section" id="contact">

          <div>
            <span className="section-label">
              GET IN TOUCH
            </span>

            <h2>
              We're here to help.
            </h2>

            <p>
              Have questions about appointments, medical records
              or our healthcare platform?
            </p>

            <Link to="/dashboard" className="primary-button">
              Get Started
              <ArrowRight size={19} />
            </Link>
          </div>

        </section>

      </main>

    </div>
  );
}


/* ================= STAT COMPONENT ================= */

function Stat({ icon, number, label }) {
  return (
    <div className="stat-item">

      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-text">
        <strong>{number}</strong>
        <span>{label}</span>
      </div>

    </div>
  );
}