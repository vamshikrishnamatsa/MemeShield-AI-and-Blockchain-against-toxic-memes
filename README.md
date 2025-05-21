# 🛡️ MemeShield: AI + Blockchain Powered Cyberbullying Detection in Memes

![Streamlit](https://img.shields.io/badge/Streamlit-AI%20WebApp-red?style=flat&logo=streamlit)
![Ethereum](https://img.shields.io/badge/Ethereum-Blockchain-blue?style=flat&logo=ethereum)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 Overview

**MemeShield** is an innovative AI-powered web application that detects **cyberbullying in memes** using advanced **multimodal analysis** (image + text). Leveraging **MoonDream**, **OCR**, and **blockchain (Ethereum + IPFS)**, the system not only identifies offensive memes but also stores detection results in a **tamper-proof and decentralized** way for transparency.

Memes today are often used to subtly spread harmful or derogatory content that bypasses traditional moderation tools. This project bridges the gap by analyzing both image and text content simultaneously and ensuring secure storage of detection data using blockchain technology.

---

## 🚀 Features

- 🔍 **Multimodal Analysis** using MoonDream AI (image + text)
- 📥 **Meme Input**: Upload your own or fetch from **Reddit**
- 🧠 **Real-Time Detection**: Detects and explains cyberbullying in memes
- 🔐 **Blockchain Logging**:
  - Stores flagged memes on **IPFS**
  - Records hash and detection on **Ethereum**
- 🌐 **Streamlit Frontend**: Clean, interactive UI

---

## 🧠 Tech Stack

| Category        | Tools Used                                         |
|----------------|----------------------------------------------------|
| 💡 AI/ML       | MoonDream, Tesseract OCR                           |
| 🌐 Frontend    | Streamlit                                          |
| 🔗 Blockchain  | Ethereum, IPFS, web3.py / ethers.js                |
| 🔍 Others      | Reddit API, Pillow, NumPy                          |
| 🐍 Language     | Python 3.8+                                        |

---

## ⚙️ How It Works

1. **Input Meme**: User uploads or fetches meme from Reddit.
2. **OCR**: Extracts text from the meme image.
3. **Multimodal Model**: MoonDream evaluates image + text together.
4. **Classification**:
   - If offensive: generate explanation.
   - Upload image to **IPFS**, log detection to **Ethereum**.
5. **Display**: Results + reasoning shown to the user in real-time.

---

## outputs

