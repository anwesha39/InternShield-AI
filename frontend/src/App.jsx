
import { useState } from 'react'
import './App.css'

function App() {
  // =====================================
  // 1. REACT STATES
  // =====================================

  const [jobText, setJobText] = useState('')
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  // =====================================
  // 2. CONNECT TO PYTHON BACKEND
  // =====================================

  const handleCheck = async () => {

    if (!jobText.trim()) {
      setStatus('Please enter a job description first.')
      setResult(null)
      return
    }

    setLoading(true)
    setResult(null)
    setStatus('Connecting to InternShield AI server...')

    try {

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/analyze`,
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            description: jobText
          })
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to analyse this opportunity.'
        )
      }

      setResult(data)
      setStatus(data.message || 'Analysis completed successfully!')

    } catch (error) {

      console.error('Analysis error:', error)

      setResult(null)

      setStatus(
        error.message.includes('fetch')
          ? 'Unable to connect to the Python server. Please check whether it is running.'
          : error.message
      )

    } finally {

      setLoading(false)

    }
  }

  // =====================================
  // 3. RESET ANALYSIS
  // =====================================

  const handleReset = () => {
    setJobText('')
    setFile(null)
    setStatus('')
    setResult(null)

    const fileInput = document.getElementById('offer-file')

    if (fileInput) {
      fileInput.value = ''
    }
  }

  // =====================================
  // 4. RISK BADGE CLASS
  // =====================================

  const getRiskClass = (risk) => {

    if (risk === 'High Risk') {
      return 'high-risk'
    }

    if (risk === 'Suspicious') {
      return 'suspicious-risk'
    }

    return 'lower-risk'
  }

  // =====================================
  // 5. WEBSITE UI
  // =====================================

  return (

    <div className="app">

      {/* =================================
          NAVIGATION
      ================================= */}

      <nav className="navbar">

        <a href="#home" className="brand">
          <span className="brand-icon">🛡️</span>
          InternShield<span> AI</span>
        </a>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </div>

        <a href="#checker" className="nav-button">
          Check Opportunity
        </a>

      </nav>


      {/* =================================
          HERO SECTION
      ================================= */}

      <section className="hero-section" id="home">

        <div className="hero-content">

          <div className="hero-badge">
            ✨ AI-Powered Recruitment Safety
          </div>

          <h1>
            Don't Let Fake Jobs
            <br />
            <span>Steal Your Future.</span>
          </h1>

          <p>
            Your smart internship and job safety assistant.
            Analyse suspicious job offers, recruitment messages
            and offer letters before making your next move.
          </p>

          <div className="hero-buttons">

            <a href="#checker" className="primary-button">
              Check an Opportunity →
            </a>

            <a href="#how-it-works" className="secondary-button">
              Learn More
            </a>

          </div>

          <div className="hero-note">
            🔒 Your safety starts with verification.
          </div>

        </div>


        <div className="hero-visual">

          <div className="shield-circle">
            <span>🛡️</span>
          </div>

          <div className="floating-card card-one">
            <span>🔍</span>

            <div>
              <strong>Smart Analysis</strong>
              <small>AI-powered screening</small>
            </div>
          </div>

          <div className="floating-card card-two">
            <span>🔐</span>

            <div>
              <strong>Stay Protected</strong>
              <small>Identify warning signs</small>
            </div>
          </div>

        </div>

      </section>


      {/* =================================
          OPPORTUNITY CHECKER
      ================================= */}

      <section className="checker-section" id="checker">

        <div className="section-heading">

          <span className="section-tag">
            START HERE
          </span>

          <h2>Check Before You Trust.</h2>

          <p>
            Paste a job description or select an offer
            document for future scanning support.
          </p>

        </div>


        <div className="checker-card">

          <label htmlFor="job-description">
            Paste Job / Internship Description
          </label>

          <textarea
            id="job-description"
            placeholder="Paste your job description, internship advertisement or recruitment email here..."
            value={jobText}
            onChange={(e) => {
              setJobText(e.target.value)
              setStatus('')
              setResult(null)
            }}
          />


          {/* FILE UPLOAD */}

          <div className="upload-area">

            <span className="upload-icon">📄</span>

            <h3>Upload Your Offer Letter</h3>

            <p>Choose a PDF or image file</p>

            <input
              id="offer-file"
              type="file"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={(e) => {
                setFile(e.target.files[0] || null)
                setStatus('')
                setResult(null)
              }}
            />

            {file && (

              <p className="file-name">
                Selected: {file.name}
              </p>

            )}

            <small>
              Document extraction is coming soon.
              Paste the document text above for analysis.
            </small>

          </div>


          {/* ANALYZE BUTTON */}

          <button
            className="analyze-button"
            onClick={handleCheck}
            disabled={loading}
          >

            {loading
              ? '⏳ Analysing...'
              : '🔍 Analyse Opportunity'
            }

          </button>


          {/* STATUS MESSAGE */}

          {status && (

            <p className="status-message" role="status">
              {status}
            </p>

          )}


          {/* =================================
              AI ANALYSIS RESULT DASHBOARD
          ================================= */}

          
{result && (
  <div className="analysis-result">

    {/* REPORT HEADER */}
    <div className="result-header">
      <div className="report-brand">
        <span className="report-shield">🛡️</span>
        <div>
          <strong>INTERNSHIELD AI</strong>
          <small>SECURITY ANALYSIS REPORT</small>
        </div>
      </div>

      <span className={`risk-badge ${getRiskClass(result.risk_level)}`}>
        {result.risk_level}
      </span>
    </div>

    {/* MAIN RESULT */}
    <div className="result-intro">
      <span className="result-eyebrow">RECRUITMENT RISK ASSESSMENT</span>
      <h2>Analysis Results</h2>
      <p>
        Your submitted job opportunity has been evaluated
        using machine learning and rule-based indicators.
      </p>
    </div>

    {/* PREDICTION CARD */}
    <div className="prediction-box">
      <div className="prediction-top">
        <span className="prediction-icon">🤖</span>
        <div>
          <small>MACHINE LEARNING PREDICTION</small>
          <h3>{result.prediction}</h3>
        </div>
      </div>

      <div className="prediction-model">
        <span>Model used</span>
        <strong>{result.model_used}</strong>
      </div>
    </div>

    {/* WARNING INDICATORS */}
    <div className="warning-section">
      <div className="dashboard-section-heading">
        <div>
          <span className="result-eyebrow">RISK INDICATORS</span>
          <h3>⚠️ Detected Warning Signs</h3>
        </div>

        <span className="warning-total">
          {result.warning_count ?? 0} Detected
        </span>
      </div>

      {result.warning_signs && result.warning_signs.length > 0 ? (
        <ul className="warning-list">
          {result.warning_signs.map((warning, index) => (
            <li key={index}>
              <span className="warning-number">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span>{warning}</span>
            </li>
          ))}
        </ul>
      ) : (
        <div className="no-warning">
          <span>✓</span>
          No warning patterns were detected by the
          rule-based screening.
        </div>
      )}
    </div>

    {/* SAFETY RECOMMENDATION */}
    <div className="recommendation-section">
      <div className="recommendation-title">
        <span>🔐</span>
        <h3>Safety Recommendation</h3>
      </div>

      <p>{result.recommendation}</p>
    </div>

    {/* MODEL INFORMATION */}
    <div className="model-information">
      <span className="result-eyebrow">TECHNICAL DETAILS</span>
      <h3>Analysis Information</h3>

      <div className="model-info-grid">
        <div>
          <small>ML Model</small>
          <strong>{result.model_used}</strong>
        </div>

        <div>
          <small>Prediction Label</small>
          <strong>{result.prediction_label}</strong>
        </div>

        <div>
          <small>Warning Count</small>
          <strong>{result.warning_count ?? 0}</strong>
        </div>

        <div>
          <small>Analysis Type</small>
          <strong>ML + Rule-based</strong>
        </div>
      </div>
    </div>

    {/* DISCLAIMER */}
    <div className="disclaimer">
      <div className="disclaimer-heading">
        <span>ⓘ</span>
        <strong>Important Disclaimer</strong>
      </div>

      <p>
        This automated screening result is not proof of fraud
        and does not guarantee that an opportunity is genuine.
        Always independently verify the employer, recruiter
        and job offer before proceeding.
      </p>
    </div>

    {/* RESET BUTTON */}
    <button
      className="reset-button"
      onClick={handleReset}
    >
      ↻ Analyse Another Opportunity
    </button>

  </div>
)}



          {/* PRIVACY NOTE */}

          <p className="privacy-note">
            🔒 Your submitted text is processed by the
            InternShield AI backend for analysis.
          </p>

        </div>

      </section>


      {/* =================================
          FEATURES SECTION
      ================================= */}

      <section className="features-section" id="features">

        <div className="section-heading">

          <span className="section-tag">
            OUR FEATURES
          </span>

          <h2>
            Your Recruitment Safety Toolkit
          </h2>

          <p>
            Multiple tools to help you evaluate suspicious
            recruitment opportunities.
          </p>

        </div>


        <div className="features-grid">

          <div className="feature-card">
            <span>💼</span>

            <h3>Job Scam Detection</h3>

            <p>
              Analyse job and internship descriptions
              for suspicious patterns.
            </p>
          </div>


          <div className="feature-card">
            <span>📧</span>

            <h3>Email Analysis</h3>

            <p>
              Check recruitment emails for potential
              warning signs.
            </p>
          </div>


          <div className="feature-card">
            <span>📑</span>

            <h3>Offer Letter Scanner</h3>

            <p>
              Prepare to extract and analyse uploaded
              offer letters and screenshots.
            </p>
          </div>


          <div className="feature-card">
            <span>🏢</span>

            <h3>Company Verification</h3>

            <p>
              Future support for checking available
              company and recruiter information.
            </p>
          </div>

        </div>

      </section>


      {/* =================================
          HOW IT WORKS
      ================================= */}

      <section className="how-section" id="how-it-works">

        <div className="section-heading">

          <span className="section-tag">
            SIMPLE PROCESS
          </span>

          <h2>
            How InternShield AI Works
          </h2>

        </div>


        <div className="steps-grid">

          <div className="step-card">

            <span>01</span>

            <h3>Submit</h3>

            <p>
              Paste a job description or recruitment message.
            </p>

          </div>


          <div className="step-card">

            <span>02</span>

            <h3>Analyse</h3>

            <p>
              The trained Machine Learning model evaluates
              the submitted text.
            </p>

          </div>


          <div className="step-card">

            <span>03</span>

            <h3>Understand</h3>

            <p>
              Review the prediction, warning indicators
              and safety recommendations.
            </p>

          </div>

        </div>

      </section>


      {/* =================================
          FOOTER
      ================================= */}

      <footer className="footer">

        <a href="#home" className="brand">
          🛡️ InternShield <span>AI</span>
        </a>

        <p>
          Helping students make safer career decisions.
        </p>

        <small>
          © 2026 InternShield AI. All rights reserved.
        </small>

      </footer>

    </div>

  )
}

export default App
