import React from 'react';
import { Link } from 'react-router-dom';

const CRMSystem = ({ status, handleLogout, handleGlobalLogout }) => {
    return (
        <div className="card app-card crm-theme">
            <div className="app-header">
                <h1> CRM System</h1>
                <Link to="/dashboard" className="back-link">← Back to Hub</Link>
            </div>
            <p>SSO Verify: <strong>Authenticated ✅</strong></p>
            <div className="mock-content">
                <div className="mock-row"><span>Lead</span><span>Value</span><span>Stage</span></div>
                <div className="mock-row"><span>Acme Corp</span><span>$50,000</span><span>Negotiation</span></div>
                <div className="mock-row"><span>Globex</span><span>$12,000</span><span>Closed Won</span></div>
            </div>

            <div className="actions">
                <button onClick={handleLogout}>Logout (CRM Only)</button>
                <button onClick={handleGlobalLogout} className="btn-danger">Global Logout</button>
            </div>
        </div>
    );
};

export default CRMSystem;
