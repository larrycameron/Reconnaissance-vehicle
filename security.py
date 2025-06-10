"""
Vehicle Security Module
Handles all security-related functionality for the autonomous vehicle system.
"""

import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import hashlib
import ssl
import socket
import threading
import time

class VehicleSecurity:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._access_tokens: Dict[str, dict] = {}
        self._failed_attempts: Dict[str, int] = {}
        self._blocked_ips: List[str] = []
        self._last_cleanup = time.time()
        self._security_lock = threading.Lock()
        
        # Security configuration
        self.MAX_FAILED_ATTEMPTS = 5
        self.BLOCK_DURATION = 3600  # 1 hour in seconds
        self.TOKEN_EXPIRY = 3600  # 1 hour in seconds
        self.CLEANUP_INTERVAL = 300  # 5 minutes in seconds
        
        # Initialize security monitoring
        self._start_security_monitor()

    def _start_security_monitor(self):
        """Start the security monitoring thread."""
        monitor_thread = threading.Thread(target=self._monitor_security, daemon=True)
        monitor_thread.start()

    def _monitor_security(self):
        """Continuously monitor security status."""
        while True:
            try:
                self._cleanup_expired_data()
                self._check_system_integrity()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Security monitor error: {str(e)}")

    def authenticate_user(self, username: str, password: str, ip_address: str) -> Optional[str]:
        """
        Authenticate a user and generate an access token.
        
        Args:
            username: User's username
            password: User's password
            ip_address: IP address of the request
            
        Returns:
            JWT token if authentication successful, None otherwise
        """
        if ip_address in self._blocked_ips:
            self.logger.warning(f"Blocked IP attempt: {ip_address}")
            return None

        if self._failed_attempts.get(ip_address, 0) >= self.MAX_FAILED_ATTEMPTS:
            self._block_ip(ip_address)
            return None

        # In a real system, verify against a secure database
        # This is a simplified example
        if not self._verify_credentials(username, password):
            self._failed_attempts[ip_address] = self._failed_attempts.get(ip_address, 0) + 1
            return None

        # Generate JWT token
        token = self._generate_token(username)
        self._access_tokens[token] = {
            'username': username,
            'ip_address': ip_address,
            'created_at': datetime.utcnow()
        }
        
        return token

    def verify_token(self, token: str, ip_address: str) -> bool:
        """
        Verify if a token is valid and not expired.
        
        Args:
            token: JWT token to verify
            ip_address: IP address of the request
            
        Returns:
            True if token is valid, False otherwise
        """
        try:
            if token not in self._access_tokens:
                return False

            token_data = self._access_tokens[token]
            if token_data['ip_address'] != ip_address:
                self.logger.warning(f"IP mismatch for token: {ip_address}")
                return False

            # Check token expiration
            created_at = token_data['created_at']
            if datetime.utcnow() - created_at > timedelta(seconds=self.TOKEN_EXPIRY):
                del self._access_tokens[token]
                return False

            return True
        except Exception as e:
            self.logger.error(f"Token verification error: {str(e)}")
            return False

    def _verify_credentials(self, username: str, password: str) -> bool:
        """
        Verify user credentials.
        In a real system, this would check against a secure database.
        """
        # This is a placeholder - replace with actual credential verification
        return True

    def _generate_token(self, username: str) -> str:
        """Generate a JWT token for the user."""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=self.TOKEN_EXPIRY)
        }
        # In a real system, use a secure secret key
        return jwt.encode(payload, 'your-secret-key', algorithm='HS256')

    def _block_ip(self, ip_address: str):
        """Block an IP address for the specified duration."""
        with self._security_lock:
            self._blocked_ips.append(ip_address)
            self.logger.warning(f"IP blocked: {ip_address}")

    def _cleanup_expired_data(self):
        """Clean up expired tokens and unblock IPs."""
        current_time = time.time()
        if current_time - self._last_cleanup < self.CLEANUP_INTERVAL:
            return

        with self._security_lock:
            # Clean up expired tokens
            expired_tokens = [
                token for token, data in self._access_tokens.items()
                if datetime.utcnow() - data['created_at'] > timedelta(seconds=self.TOKEN_EXPIRY)
            ]
            for token in expired_tokens:
                del self._access_tokens[token]

            # Reset failed attempts
            self._failed_attempts.clear()

            # Unblock IPs after block duration
            self._blocked_ips = [
                ip for ip in self._blocked_ips
                if current_time - self._blocked_ips.index(ip) < self.BLOCK_DURATION
            ]

        self._last_cleanup = current_time

    def _check_system_integrity(self):
        """Check system integrity and log any anomalies."""
        try:
            # Check for suspicious patterns in access attempts
            for ip, attempts in self._failed_attempts.items():
                if attempts > self.MAX_FAILED_ATTEMPTS / 2:
                    self.logger.warning(f"Suspicious activity detected from IP: {ip}")

            # Check for token anomalies
            for token, data in self._access_tokens.items():
                if data['created_at'] > datetime.utcnow():
                    self.logger.error(f"Invalid token timestamp detected: {token}")
                    del self._access_tokens[token]

        except Exception as e:
            self.logger.error(f"System integrity check error: {str(e)}")

    def secure_communication(self, host: str, port: int) -> ssl.SSLSocket:
        """
        Establish a secure SSL connection.
        
        Args:
            host: Host to connect to
            port: Port to connect to
            
        Returns:
            SSL socket for secure communication
        """
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        sock = socket.create_connection((host, port))
        return context.wrap_socket(sock, server_hostname=host)

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypt sensitive data.
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data
        """
        # In a real system, use proper encryption
        return hashlib.sha256(data.encode()).digest()

    def verify_data_integrity(self, data: str, hash_value: bytes) -> bool:
        """
        Verify data integrity using hash.
        
        Args:
            data: Data to verify
            hash_value: Expected hash value
            
        Returns:
            True if data integrity is verified, False otherwise
        """
        return hashlib.sha256(data.encode()).digest() == hash_value

    def emergency_shutdown(self):
        """Execute emergency shutdown procedures."""
        try:
            # Log emergency shutdown
            self.logger.critical("EMERGENCY SHUTDOWN INITIATED")
            
            # Clear all access tokens
            self._access_tokens.clear()
            
            # Block all IPs
            self._blocked_ips.extend(self._failed_attempts.keys())
            
            # Log shutdown completion
            self.logger.critical("EMERGENCY SHUTDOWN COMPLETED")
            
        except Exception as e:
            self.logger.error(f"Emergency shutdown error: {str(e)}")

    def get_security_status(self) -> dict:
        """
        Get current security status.
        
        Returns:
            Dictionary containing security status information
        """
        return {
            'active_tokens': len(self._access_tokens),
            'blocked_ips': len(self._blocked_ips),
            'failed_attempts': sum(self._failed_attempts.values()),
            'last_cleanup': self._last_cleanup
        } 