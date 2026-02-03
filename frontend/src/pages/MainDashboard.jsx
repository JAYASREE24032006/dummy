import React from 'react';
import { Link } from 'react-router-dom';

const MainDashboard = ({ status, handleLogout, handleGlobalLogout }) => {
    const currentApp = sessionStorage.getItem('current_app_name') || 'Portal Dashboard';

    const handleAppSwitch = (e) => {
        const newApp = e.target.value;
        sessionStorage.setItem('current_app_name', newApp);
        window.location.reload(); // Reload to reconnect socket with new app name
    };

    return (
        <div className="card dashboard-card">
            <h1>{currentApp}</h1>
            <p className="welcome-text">Connected to Enterprise SSO Hub</p>

            <div className="simulation-controls" style={{ margin: '20px 0', padding: '15px', border: '1px dashed #666', borderRadius: '8px' }}>
                <label style={{ marginRight: '10px' }}> Simulation Mode - Identity:</label>
                <select value={currentApp} onChange={handleAppSwitch} style={{ padding: '5px' }}>
                    <option value="Portal Dashboard">Portal Dashboard</option>
                    <option value="HR Portal">HR Portal</option>
                    <option value="CRM System">CRM System</option>
                    <option value="ERP Suite">ERP Suite</option>
                    <option value="DevOps Console">DevOps Console</option>
                </select>
                <p style={{ fontSize: '0.8rem', color: '#888', marginTop: '5px' }}>
                    (Select functionality to simulate this tab acting as a different application)
                </p>
            </div>

            {status && <span className="status-badge status-success">{status}</span>}

            <div className="grid-menu">
                <Link to="/hr" className="menu-item hr">
                    <h3> HR Portal</h3>
                    <p>Employee Records & Payroll</p>
                </Link>
                <Link to="/crm" className="menu-item crm">
                    <h3> CRM System</h3>
                    <p>Sales & Customer Leads</p>
                </Link>
                <Link to="/erp" className="menu-item erp">
                    <h3> ERP Suite</h3>
                    <p>Inventory & Operations</p>
                </Link>
                <Link to="/admin" className="menu-item admin">
                    <h3> Admin Console</h3>
                    <p>Security Logs & Access</p>
                </Link>
            </div>

            <div className="actions">
                <button onClick={handleLogout} className="btn-secondary">Local Logout ({currentApp})</button>
                <button onClick={handleGlobalLogout} className="btn-danger"> Global Force Logout (Kill All Apps)</button>
            </div>
        </div>
    );
};

export default MainDashboard;
