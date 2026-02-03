import React from 'react';
import { Link } from 'react-router-dom';

const ERPSuite = ({ status, handleLogout, handleGlobalLogout }) => {
    return (
        <div className="card app-card erp-theme">
            <div className="app-header">
                <h1> ERP Suite</h1>
                <Link to="/dashboard" className="back-link">← Back to Hub</Link>
            </div>
            <p>SSO Verify: <strong>Authenticated </strong></p>
            <div className="mock-content">
                <div className="mock-row"><span>SKU</span><span>Stock</span><span>Location</span></div>
                <div className="mock-row"><span>WIDGET-01</span><span>500</span><span>Warehouse A</span></div>
                <div className="mock-row"><span>GADGET-X</span><span>23</span><span>Warehouse B</span></div>
            </div>

            <div className="actions">
                <button onClick={handleLogout}>Logout (ERP Only)</button>
                <button onClick={handleGlobalLogout} className="btn-danger">Global Logout</button>
            </div>
        </div>
    );
};

export default ERPSuite;
