import React from 'react';
import { Link } from 'react-router-dom';

const HRPortal = ({ status, handleLogout, handleGlobalLogout }) => {
    return (
        <div className="card app-card hr-theme">
            <div className="app-header">
                <h1> HR Portal</h1>
                <Link to="/dashboard" className="back-link">← Back to Hub</Link>
            </div>
            <p>SSO Verify: <strong>Authenticated </strong></p>
            <div className="mock-content">
                <div className="mock-row"><span>Employe ID</span><span>Name</span><span>Status</span></div>
                <div className="mock-row"><span>#1001</span><span>John Doe</span><span>Active</span></div>
                <div className="mock-row"><span>#1002</span><span>Jane Smith</span><span>On Leave</span></div>
            </div>

            <div className="actions">
                <button onClick={handleLogout}>Logout (HR Only)</button>
                <button onClick={handleGlobalLogout} className="btn-danger">Global Logout</button>
            </div>
        </div>
    );
};

export default HRPortal;
