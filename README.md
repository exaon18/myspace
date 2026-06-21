# My Space

**My Space** is an immersive, real-time social experience designed as a Telegram Mini App. It brings people together around a virtual campfire, combining 3D spatial environments with seamless voice and text communication—all powered directly within the browser with no backend server required for the demo.

As shown in `image_32861e.jpg`, this project provides a cozy, gamified, and interactive hangout spot.

### 🚀 Overview
My Space leverages cutting-edge web technologies to create a "no-hassle" social experience. Whether you want to catch up with friends or meet new people, this app provides an engaging environment that runs entirely in the front end.

### ✨ Key Features
*   **Immersive 3D Environment:** Built with **Three.js** to provide a visually engaging, campfire-themed space.
*   **Real-Time Voice Chat:** Utilizes **WebRTC** for high-quality, peer-to-peer voice communication.
*   **Integrated Text Chat:** Localized chat functionality to keep the conversation going alongside voice.
*   **Zero Backend Required (Demo Mode):** Uses `LocalStorage` and `BroadcastChannel` for signaling, making it incredibly easy to deploy and test.
*   **Telegram-Ready:** Optimized for integration as a Telegram Mini App, allowing users to join rooms directly through your Telegram bot.
*   **Lightweight:** Entirely self-contained in a single HTML file—no complex build steps or heavy dependencies.

### 🛠 Tech Stack
*   **Frontend:** HTML5, CSS3, JavaScript
*   **3D Engine:** Three.js
*   **Communication:** WebRTC (Peer-to-Peer)
*   **Signaling:** Browser `BroadcastChannel` API (Demo)

### 📋 How to Get Started
1.  **Clone the Repository:**
```bash
    git clone [https://github.com/exaon18/myspace.git](https://github.com/exaon18/myspace.git)
    ```
2.  **Run the Demo:** Simply open `campfire.html` in any modern web browser (Google Chrome recommended).
3.  **Host a Room:** Click "Join Campfire," allow microphone access, and share your unique **Room ID** with friends.

### 🔮 Roadmap & Customization
My Space is highly modular. Future updates and custom forks can easily integrate:
*   **Backend Signaling:** Replace the demo signaling with a robust WebSocket server (like Socket.io) for production-grade persistent chat and room management.
*   **Custom Avatars:** Swap the base models for unique, stylized 3D assets.
*   **Expanded Animations:** Add interactive emotes or campfire interactions.

---
*Built as an interactive, social-first experience for the Telegram ecosystem.*
