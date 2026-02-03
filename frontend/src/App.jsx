import { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import useAuthInterceptor, { api } from './auth/useAuthInterceptor';
import useSocketListener, { socket } from './auth/socketListener';
import './App.css'; // Import Component Styles


// Import Pages
import MainDashboard from './pages/MainDashboard';
import HRPortal from './pages/HRPortal';
import CRMSystem from './pages/CRMSystem';
import ERPSuite from './pages/ERPSuite';
import AdminConsole from './pages/AdminConsole';
import LoginPage from './pages/LoginPage';

function AppContent() {
    const [token, setToken] = useState(sessionStorage.getItem('token'));
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const navigate = useNavigate();

    // Session Storage Sync - Only for current tab focus/reload
    // We removed cross-tab localStorage sync to ensure "every time" login requirement

    const handleLocalLogout = useCallback((reason = null) => {
        sessionStorage.clear();
        setToken(null);
        setStatus(reason || "Logged out");
        navigate('/login', { state: { globalLogoutMessage: reason } });
    }, [navigate]);

    useAuthInterceptor(navigate);
    useSocketListener(navigate, token, handleLocalLogout);

    const [socketId, setSocketId] = useState(socket.id);

    useEffect(() => {
        const onConnect = () => setSocketId(socket.id);
        const onDisconnect = () => setSocketId('Disconnected');

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);

        return () => {
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
        };
    }, []);

    const handleLogin = async (username, password) => {
        console.log("Attempting Login:", username);
        try {
            // Use URLSearchParams for application/x-www-form-urlencoded
            const params = new URLSearchParams();
            params.append('username', username);
            params.append('password', password);

            const res = await api.post('/auth/login', params, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            console.log("Login Success:", res.data);
            sessionStorage.setItem('token', res.data.access_token);
            sessionStorage.setItem('user_id', 'user_123');

            // Force state update and navigate
            setToken(res.data.access_token);
            setStatus("Login Successful - Redirecting...");

            // Short delay to ensure state propagates, though not strictly necessary
            setTimeout(() => {
                navigate('/dashboard');
            }, 100);

        } catch (err) {
            console.error("Login Error:", err);
            const errorMsg = err.response?.data?.detail || "Connection Error";
            setStatus("Login Failed: " + errorMsg);
            alert("Login Failed: " + errorMsg); // Explicitly notify user
        }
    };

    const handleGlobalLogout = () => {
        const appName = sessionStorage.getItem('current_app_name') || 'Portal Dashboard';
        const userId = sessionStorage.getItem('user_id');

        if (socket && socket.connected) {
            socket.emit('force_global_logout', {
                user_id: userId,
                reason: 'Manual Global Logout via Dashboard',
                initiator: appName
            });
            setStatus(`Global Logout Signal Sent from ${appName}...`);
        } else {
            console.error("Socket not connected");
            setStatus("Error: Cannot send Kill Signal (Socket Disconnected)");
        }
    };

    // Redirect to login if no token and not already on login page
    // Note: React Router Verify will handle protection, but here we handle the "Not Logged In" UI return

    // We now use Routes for everything


    // Authenticated Routes
    return (
        <div className="App">
            <div className="socket-status">
                <span className="status-dot"></span> Agentic OS | Socket: {socketId || 'Connecting...'}
            </div>

            <Routes>
                <Route path="/login" element={
                    !token ? (
                        <LoginPage onLogin={handleLogin} status={status} />
                    ) : (
                        <Navigate to="/dashboard" replace />
                    )
                } />

                {/* Protected Routes */}
                <Route path="/dashboard" element={token ? <MainDashboard status={status} handleLogout={handleLocalLogout} handleGlobalLogout={handleGlobalLogout} /> : <Navigate to="/login" />} />
                <Route path="/hr" element={token ? <HRPortal status={status} handleLogout={handleLocalLogout} handleGlobalLogout={handleGlobalLogout} /> : <Navigate to="/login" />} />
                <Route path="/crm" element={token ? <CRMSystem status={status} handleLogout={handleLocalLogout} handleGlobalLogout={handleGlobalLogout} /> : <Navigate to="/login" />} />
                <Route path="/erp" element={token ? <ERPSuite status={status} handleLogout={handleLocalLogout} handleGlobalLogout={handleGlobalLogout} /> : <Navigate to="/login" />} />
                <Route path="/admin" element={token ? <AdminConsole status={status} handleLogout={handleLocalLogout} handleGlobalLogout={handleGlobalLogout} /> : <Navigate to="/login" />} />

                <Route path="*" element={<Navigate to={token ? "/dashboard" : "/login"} replace />} />
            </Routes>
            <footer className="app-footer-text">
                Product from Clowns in Clouds
            </footer>
        </div >
    );
}

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    );
}

export default App;
