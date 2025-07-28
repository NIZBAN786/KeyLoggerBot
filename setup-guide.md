# Educational Keylogger Project Setup Guide
## Cybersecurity Internship Project #3: "Keylogger with Encrypted Data Exfiltration"

### Quick Start (Due July 28, 2025)

#### 1. Install Dependencies
```bash
pip install pynput cryptography flask
```

#### 2. Run the Educational Keylogger
```bash
python educational-keylogger.py
```

#### 3. Features Demonstrated

**✅ All Project Requirements Met:**
- ✅ Cross-platform keylogger (Windows/Linux) using pynput
- ✅ Fernet encryption for all keystroke data
- ✅ Local storage with timestamps
- ✅ Flask server simulation for data exfiltration
- ✅ Startup persistence mechanisms (demonstrated safely)
- ✅ Kill switch implementation (ESC key)
- ✅ Ethical constraints and user consent

#### 4. How to Use

1. **Run the program**: `python educational-keylogger.py`
2. **Provide ethical consent** when prompted
3. **View the dashboard** at http://localhost:5000
4. **Start typing** to see keystroke logging in action
5. **Press ESC** to activate the kill switch
6. **View encrypted logs** on the web dashboard

#### 5. Server Alternatives

**Flask Server (Default):**
- Local web interface at http://localhost:5000
- Encrypted log viewing with decryption key
- Educational dashboard with warnings

**Telegram Bot Alternative:**
Run with: `python educational-keylogger.py --telegram-demo`
This shows how to implement a Telegram bot as an alternative to the Flask server.

#### 6. Project Structure Generated
```
~/.educational_keylogger/
├── encryption.key          # Fernet encryption key
├── encrypted_logs.dat      # Encrypted keystroke logs
└── config.json            # Configuration settings
```

#### 7. Educational Features

**Ethical Safeguards:**
- Mandatory consent dialog
- Clear educational warnings
- Audit trail logging
- Safe persistence demonstration (not actually implemented)

**Learning Demonstrations:**
- Cross-platform compatibility
- Encryption/decryption processes
- Client-server communication
- Web-based log viewing
- Kill switch mechanisms

#### 8. For Your Internship Report

**Tools Used:**
- Python 3.x
- pynput (cross-platform keyboard monitoring)
- cryptography.fernet (symmetric encryption)
- Flask (web server for data exfiltration simulation)
- JSON (data serialization)
- Threading (concurrent execution)

**Key Concepts Demonstrated:**
1. **Keystroke Logging**: Using pynput for cross-platform input capture
2. **Encryption**: Fernet symmetric encryption for data security
3. **Data Exfiltration**: Flask server simulation with web interface
4. **Persistence**: Registry (Windows) and cron (Linux) demonstrations
5. **Kill Switches**: Multiple termination methods for security
6. **Ethical Computing**: Consent mechanisms and educational warnings

#### 9. Security Features Implemented

- **Encryption**: All logs encrypted with Fernet before storage
- **Timestamps**: All activities logged with ISO format timestamps
- **Kill Switch**: ESC key and Ctrl+C termination methods
- **Audit Trail**: Complete logging of all educational activities
- **Safe Demos**: Persistence mechanisms shown conceptually only

#### 10. Troubleshooting

**Common Issues:**
- **Import errors**: Run `pip install pynput cryptography flask`
- **Permission issues**: On Linux, may need to run in X11 environment
- **Port conflicts**: Change Flask port if 5000 is in use

**Platform-Specific Notes:**
- **Windows**: Works with standard Python installation
- **Linux**: Requires X11 environment, may need `DISPLAY=:0` for SSH
- **macOS**: May require accessibility permissions

#### 11. Extension Ideas (Bonus)

If you have extra time, consider adding:
- Screenshot capture functionality
- Network packet logging
- Advanced persistence techniques
- Database storage instead of files
- Mobile device simulation

---

**Important Reminder**: This is for educational purposes only. Use responsibly and only on systems you own or have explicit permission to monitor. This demonstrates cybersecurity concepts for learning and should never be used maliciously.

**Good luck with your internship project presentation!**