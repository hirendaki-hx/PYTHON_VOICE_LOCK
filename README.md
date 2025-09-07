## Mission Log System v1.0
A secure voice-authenticated mission log application that allows authorized agents to record and review mission reports using voice authentication. 🎤🔐

## ✨ Features
- 🎤 Voice Authentication: Secure access using a voice passphrase
- 📝 Mission Logging: Record timestamped mission reports
- 📊 Log Review: View all previous mission logs in a scrollable interface
- 🔒 Secure Access: Application remains locked until proper authentication
- 👤 User-Friendly Interface: Simple Tkinter-based GUI for easy operation

## 📋 Requirements
- Python 3.6+
- Required packages:
  - speechrecognition
  - pyaudio (for microphone access)
  - tkinter (usually included with Python)

## 🚀 Installation

### 1. Clone or download this repository
```bash
# Clone the repository
git clone https://github.com/hirendaki-hx/voice-lock-diary.git
cd voice-lock-diary

# Run the application
python Voic_Lock_App.py
```
### 2. Install required dependencies:
```bash
pip install speechrecognition pyaudio
```
### 3. Run
```bash
python Mission_Log_Voic_Lock_App.py
```

## 📁 File Structure
```
PYTHON_VOICE_LOCK/
├── Voic_Lock_App.py    # 🐍 Main application file
├── agent_logs.txt      # 📄 Mission logs (created after first entry)
└── README.md           # 📖 This file
```
## 📝 License
- This project is licensed under the MIT License - see the 'LICENSE' file for details.



