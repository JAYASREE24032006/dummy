import React from 'react';
import { motion } from 'framer-motion';
import shieldImg from '../assets/shield-logo.jpg';

const ShieldLogo = () => {
    return (
        <motion.div
            className="shield-logo-container"
            style={{
                width: '140px',
                height: '140px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'relative',
                margin: '0 auto'
            }}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{
                opacity: 1,
                scale: 1,
                y: [0, -12, 0] // Floating animation
            }}
            transition={{
                opacity: { duration: 1 },
                scale: { duration: 0.8, ease: "easeOut" },
                y: {
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut"
                }
            }}
        >
            <img
                src={shieldImg}
                alt="Shield Logo"
                style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain',
                    borderRadius: '50%', // Assuming it looks better rounded given the shield shape usually fits well
                    boxShadow: '0 0 20px rgba(6, 182, 212, 0.3)' // Cyan glow
                }}
            />
        </motion.div>
    );
};

export default ShieldLogo;
