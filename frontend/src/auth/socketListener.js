import { useEffect } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:8000', {
    autoConnect: false,
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionAttempts: 5,
});

const useSocketListener = (navigate, token) => {
    useEffect(() => {
        const userId = sessionStorage.getItem('user_id');
        const appName = sessionStorage.getItem('current_app_name') || 'Portal Dashboard';

        if (userId && token) {
            if (!socket.connected) {
                socket.connect();
                console.log("Socket connecting...");
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

            // Heartbeat Loop (Every 2 minutes)
            const heartbeatInterval = setInterval(() => {
                if (socket.connected) {
                    socket.emit('heartbeat', { user_id: userId });
                    // console.log("💓 Sent Heartbeat");
                }
            }, 120000);

            socket.on('LOGOUT_ALL', (data) => {
                console.warn("Global Logout Signal Received!", data);
                if (data.user_id === userId) {
                    let msg = `Security Alert from Protocol Sentinel:\n\nGlobal Logout Initiated by ${data.initiator || 'System'}.\nReason: ${data.reason}`;
                    alert(msg);
                    sessionStorage.clear();
                    navigate('/login');
                    socket.disconnect();
                }
            });

            // Re-Auth Handlers
            socket.on('REQUIRE_REAUTH', (data) => {
                console.warn("🛡️ Security Challenge Received");
                // In a real app, this would open a Modal.
                // For prototype, we use prompt().
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
    }, [navigate, token]);
};

export { socket };
export default useSocketListener;
