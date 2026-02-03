import React from 'react';
import { motion } from 'framer-motion';

const ShieldLogo = () => {
    return (
        <motion.div
            className="shield-logo-container"
            style={{
                width: '120px',
                height: '120px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'relative',
                margin: '0 auto'
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
        >
            <svg
                width="100"
                height="100"
                viewBox="0 0 100 100"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                style={{ overflow: 'visible' }}
            >
                {/* Defs for gradients and filters */}
                <defs>
                    <linearGradient id="shieldGradient" x1="50" y1="0" x2="50" y2="100" gradientUnits="userSpaceOnUse">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="100%" stopColor="#1e40af" />
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="3.5" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {/* Outer Shield Outline - Pulsing */}
                <motion.path
                    d="M50 5 L90 20 V50 C90 75 50 95 50 95 C50 95 10 75 10 50 V20 L50 5 Z"
                    stroke="#60a5fa"
                    strokeWidth="2"
                    fill="none"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{
                        pathLength: 1,
                        opacity: [0.5, 1, 0.5],
                        strokeWidth: [2, 3, 2]
                    }}
                    transition={{
                        pathLength: { duration: 2, ease: "easeInOut" },
                        opacity: { duration: 3, repeat: Infinity, ease: "easeInOut" },
                        strokeWidth: { duration: 2, repeat: Infinity, ease: "easeInOut" }
                    }}
                />

                {/* Inner Shield - Filled */}
                <motion.path
                    d="M50 12 L82 24 V50 C82 70 50 88 50 88 C50 88 18 70 18 50 V24 L50 12 Z"
                    fill="url(#shieldGradient)"
                    fillOpacity="0.2"
                    stroke="#3b82f6"
                    strokeWidth="1"
                    style={{ filter: 'url(#glow)' }}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                />

                {/* Central Core - The "Eye" or Chip */}
                <motion.circle
                    cx="50"
                    cy="45"
                    r="8"
                    fill="#eff6ff"
                    initial={{ scale: 0 }}
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{
                        delay: 1,
                        duration: 2,
                        repeat: Infinity,
                        repeatType: "reverse"
                    }}
                />

                {/* Scanner Line */}
                <motion.line
                    x1="15"
                    y1="25"
                    x2="85"
                    y2="25"
                    stroke="#93c5fd"
                    strokeWidth="2"
                    strokeOpacity="0.8"
                    animate={{
                        y1: [25, 75, 25],
                        y2: [25, 75, 25],
                        opacity: [0, 1, 0]
                    }}
                    transition={{
                        duration: 3,
                        ease: "linear",
                        repeat: Infinity
                    }}
                />

                {/* Data Particles caused by glitch */}
                {[...Array(3)].map((_, i) => (
                    <motion.circle
                        key={i}
                        r="1.5"
                        fill="#60a5fa"
                        initial={{ x: 50, y: 45, opacity: 0 }}
                        animate={{
                            x: 50 + (Math.random() * 40 - 20),
                            y: 45 + (Math.random() * 40 - 20),
                            opacity: [1, 0]
                        }}
                        transition={{
                            duration: 1.5,
                            repeat: Infinity,
                            delay: i * 0.5,
                            repeatDelay: 0.5
                        }}
                    />
                ))}

            </svg>
        </motion.div>
    );
};

export default ShieldLogo;
