import { useEffect } from 'react';
import { io } from 'socket.io-client';

const socketUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const socket = io(socketUrl, {
    autoConnect: false,
    transports: ['websocket'], // Force WebSocket only to avoid polling 400s
    reconnection: true,
    reconnectionAttempts: 10,
    withCredentials: true,
});

const useSocketListener = (navigate, token, onLogout) => {
    useEffect(() => {
        const userId = sessionStorage.getItem('user_id');
        const appName = sessionStorage.getItem('current_app_name') || 'Portal Dashboard';

        if (userId && token) {
            if (!socket.connected) {
                console.log("Initialize Socket Connection...");
                socket.connect();
            }

            const joinRoom = () => {
                console.log(`Attempting to join room for user: ${userId} as ${appName}`);
                socket.emit('join', { user_id: userId, app_name: appName });
            };

            if (socket.connected) {
                joinRoom();
            }

            const onConnect = () => {
                console.log("Socket connected:", socket.id);
                joinRoom();
            };

            socket.on('connect', onConnect);
            socket.on('connect_error', (err) => {
                console.error("Socket Connection Error:", err.message);
            });

            // Heartbeat Loop (Every 2 minutes)
            const heartbeatInterval = setInterval(() => {
                if (socket.connected) {
                    socket.emit('heartbeat', { user_id: userId });
                }
            }, 120000);

            socket.on('LOGOUT_ALL', (data) => {
                console.warn("Global Logout Signal Received!", data);
                console.log("Expected UserID:", userId, "Received UserID:", data.user_id);
                if (String(data.user_id) === String(userId)) {
                    let msg = `Global Logout Initiated by ${data.initiator || 'System'}.\nReason: ${data.reason}`;
                    socket.disconnect();
                    // Use callback to update App state and navigate
                    if (onLogout) onLogout(msg);
                }
            });

            // Re-Auth Handlers
            socket.on('REQUIRE_REAUTH', (data) => {
                console.warn("🛡️ Security Challenge Received");
                const pwd = prompt(`⚠️ SECURITY CHALLENGE ⚠️\n\nSystem detected unusual activity: ${data.reason}\n\nPlease verify your password to continue:`);
                if (pwd) {
                    socket.emit('verify_password', { user_id: userId, password: pwd });
                }
            });

            socket.on('REAUTH_SUCCESS', () => {
                alert("✅ Verification Successful. Grace Period Active.");
            });

            socket.on('REAUTH_FAILED', () => {
                alert("❌ Verification Failed.");
            });

            return () => {
                clearInterval(heartbeatInterval);
                socket.off('connect', onConnect);
                socket.off('connect_error');
                socket.off('LOGOUT_ALL');
                socket.off('REQUIRE_REAUTH');
                socket.off('REAUTH_SUCCESS');
                socket.off('REAUTH_FAILED');
            };
        } else {
            if (socket.connected) {
                socket.disconnect();
            }
        }
    }, [navigate, token, onLogout]);
};

export { socket };
export default useSocketListener;
