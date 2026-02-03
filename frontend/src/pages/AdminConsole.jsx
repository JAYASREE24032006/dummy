import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { socket } from '../auth/socketListener';

const AdminConsole = ({ status, handleLogout, handleGlobalLogout }) => {
    const [events, setEvents] = useState([]);
    const [activeSessions, setActiveSessions] = useState({});

    useEffect(() => {
        // Join Admin Room (simulated by just listening and updating app name if needed, but here we just listen)
        // Ideally we should emit 'join_admin' or similar, but our websockets.py checks for "Admin" in app_name
        // So let's make sure our session storage says "Admin Console"
        const currentApp = sessionStorage.getItem('current_app_name');
        if (!currentApp || !currentApp.includes('Admin')) {
            sessionStorage.setItem('current_app_name', 'Admin Console');
            window.location.reload();
        }

        const onRiskUpdate = (data) => {
            // Add to activity log
            const timestamp = new Date().toLocaleTimeString();
            setEvents(prev => [{ ...data, timestamp }, ...prev].slice(0, 50));

            // Update Active Sessions Map
            setActiveSessions(prev => ({
                ...prev,
                [data.user_id]: {
                    ...prev[data.user_id],
                    score: data.score,
                    status: data.status,
                    last_app: data.app_name
                }
            }));
        };

        socket.on('RISK_UPDATE', onRiskUpdate);

        return () => {
            socket.off('RISK_UPDATE', onRiskUpdate);
        };
    }, []);

    return (
        <div className="card dashboard-card admin-theme" style={{ maxWidth: '1200px' }}>
            <div className="app-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1>🛡️ Security Command Center</h1>
                    <p style={{ color: 'var(--accent)' }}>Agentic AI Overwatch: Active</p>
                </div>
                <Link to="/dashboard" className="back-link" style={{ color: 'var(--text-muted)' }}>← Hub</Link>
            </div>

            <div className="gauge-container">
                <div className="gauge">
                    <h3>Active Risks</h3>
                    <div className="risk-score-display" style={{ color: 'var(--danger)' }}>
                        {Object.values(activeSessions).filter(s => s.score > 50).length}
                    </div>
                    <p>Users above threshold</p>
                </div>
                <div className="gauge">
                    <h3>System Status</h3>
                    <div className="risk-score-display" style={{ color: 'var(--success)' }}>
                        OK
                    </div>
                    <p>All Agents Operational</p>
                </div>
                <div className="gauge">
                    <h3>Total Sessions</h3>
                    <div className="risk-score-display" style={{ color: 'var(--primary)' }}>
                        {Object.keys(activeSessions).length || 1}
                    </div>
                    <p>Including simulated</p>
                </div>
            </div>

            <h3 style={{ marginTop: '2rem' }}>Live Session Map</h3>
            <table className="risk-table">
                <thead>
                    <tr>
                        <th>User ID</th>
                        <th>Last App</th>
                        <th>Risk Score</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(activeSessions).length === 0 ? (
                        <tr><td colSpan="5" style={{ textAlign: 'center', color: '#666' }}>Waiting for real-time events...</td></tr>
                    ) : (
                        Object.entries(activeSessions).map(([uid, session]) => (
                            <tr key={uid}>
                                <td>{uid}</td>
                                <td>{session.last_app}</td>
                                <td>
                                    <span style={{
                                        color: session.score > 80 ? 'var(--danger)' : session.score > 50 ? 'var(--warning)' : 'var(--success)',
                                        fontWeight: 'bold'
                                    }}>
                                        {session.score || 0}
                                    </span>
                                </td>
                                <td>{session.status}</td>
                                <td>
                                    <button className="btn-danger" style={{ padding: '0.25rem 0.75rem', fontSize: '0.8rem' }} onClick={handleGlobalLogout}>
                                        KILL
                                    </button>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>

            <h3 style={{ marginTop: '2rem' }}>Agent Activity Feed</h3>
            <div className="activity-feed" style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px', maxHeight: '200px', overflowY: 'auto', fontFamily: 'monospace' }}>
                {events.map((e, i) => (
                    <div key={i} style={{ marginBottom: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.25rem' }}>
                        <span style={{ color: '#666' }}>[{e.timestamp}]</span>
                        <span style={{ color: 'var(--accent)', margin: '0 0.5rem' }}>{e.app_name}</span>
                        Risk: {e.score}
                        {e.reasons && e.reasons.length > 0 && <span style={{ color: 'var(--warning)', marginLeft: '0.5rem' }}> → {e.reasons.join(', ')}</span>}
                        {e.status === 'KILLED' && <span style={{ color: 'var(--danger)', fontWeight: 'bold', marginLeft: '0.5rem' }}> [TERMINATED]</span>}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminConsole;
