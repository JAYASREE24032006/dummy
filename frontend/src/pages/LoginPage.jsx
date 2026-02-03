import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import ShieldLogo from '../components/ShieldLogo';

const LoginPage = ({ onLogin, status }) => {
    const location = useLocation();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    // Prioritize message passed via redirect, else default status (Removing global logout message as requested)
    const [localStatus, setLocalStatus] = useState(status || '');

    // Reset status on new login attempt
    const handleSubmit = (e) => {
        e.preventDefault();
        setLocalStatus('');
        onLogin(username, password);
    };

    // Animation Variants
    const containerVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.8,
                ease: [0.6, -0.05, 0.01, 0.99] // Custom easing
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 10 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
    };

    return (
        <div className="App login-theme" style={{
            position: 'relative',
            overflow: 'hidden',
            background: 'linear-gradient(to bottom, #020617, #0f172a)', // Static gradient match
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <motion.div
                className="card"
                style={{ zIndex: 1, backdropFilter: 'blur(10px)', backgroundColor: 'rgba(15, 23, 42, 0.6)' }}
                variants={containerVariants}
                initial="hidden"
                animate="visible"
            >
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.1 }}
                    style={{ marginBottom: '1.5rem' }}
                >
                    <ShieldLogo />
                </motion.div>

                <motion.h1
                    variants={itemVariants}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                >
                    SHIELD
                </motion.h1>
                <motion.p
                    className="text-muted"
                    style={{ textAlign: 'center', marginBottom: '2rem' }}
                    variants={itemVariants}
                    transition={{ delay: 0.3 }}
                >
                    Agentic Security Protocol
                </motion.p>

                <form onSubmit={handleSubmit} autoComplete="off">
                    {/* Fake fields to trick browser heuristics */}
                    <input type="text" style={{ display: 'none' }} />
                    <input type="password" style={{ display: 'none' }} />

                    <motion.div
                        className="input-group"
                        variants={itemVariants}
                        transition={{ delay: 0.4 }}
                    >
                        <input
                            type="text"
                            name="agent_user_id_x9"
                            id="field_user_rnd"
                            placeholder="Identity ID"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            autoComplete="off"
                            list="autocompleteOff"
                        />
                    </motion.div>

                    <motion.div
                        className="password-container"
                        variants={itemVariants}
                        transition={{ delay: 0.5 }}
                    >
                        <input
                            type={showPassword ? "text" : "password"}
                            name="agent_pass_code_v2"
                            id="field_pass_rnd"
                            placeholder="Access Code"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            autoComplete="new-password"
                            readOnly={true}
                            onFocus={(e) => e.target.removeAttribute('readonly')}
                        />
                        <button
                            type="button"
                            className="password-toggle-btn"
                            onClick={() => setShowPassword(!showPassword)}
                            title={showPassword ? "Hide password" : "Show password"}
                        >
                            {showPassword ? (
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                                    <line x1="1" y1="1" x2="23" y2="23"></line>
                                </svg>
                            ) : (
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                    <circle cx="12" cy="12" r="3"></circle>
                                </svg>
                            )}
                        </button>
                    </motion.div>

                    <motion.button
                        type="submit"
                        variants={itemVariants}
                        transition={{ delay: 0.6 }}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        Initialize Session
                    </motion.button>

                    <motion.div
                        style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.8rem', color: 'rgba(255,255,255,0.4)' }}
                        className="system-status"
                        variants={itemVariants}
                        transition={{ delay: 0.7 }}
                    >
                        Product from Clowns in Clouds
                    </motion.div>
                </form>

                {localStatus && (
                    <motion.p
                        className={`status-badge ${localStatus.includes('Failed') ? 'status-error' : 'status-success'}`}
                        style={{ marginTop: '1.5rem', textAlign: 'center' }}
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                    >
                        {localStatus}
                    </motion.p>
                )}
            </motion.div>
        </div>
    );
};

export default LoginPage;
