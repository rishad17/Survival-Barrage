# 💥 Survival Barrage

Welcome to **Survival Barrage**, a 3D survival shooting game built entirely using **Python** and **PyOpenGL** (🛠️ OpenGL, GLUT, GLU). The game challenges the player to survive waves of enemies while managing bullets, dodging attacks, and optionally enabling cheat features like auto-aim.

---

## 🎮 Game Features

* 🔄 3D player character with moving limbs and rotating gun.
* 🤠 Multiple enemies continuously pursuing the player.
* 🔫 Shooting mechanic with bullet collision detection.
* 👁 Third-person and first-person camera views.
* 🏛️ Boundary-restricted arena.
* 🎯 Scoring system with lives and game over conditions.
* 🧩 Cheat mode with auto-aim and auto-fire.
* 🔄 Auto camera feature in first-person mode.

---

## 📄 Technologies Used

* 💻 **Python 3**
* 🛠️ **PyOpenGL** (OpenGL.GL, OpenGL.GLU, OpenGL.GLUT)

---

## 🔧 Installation & Running

### 1. Install Python (if not installed)

Make sure you have Python 3 installed. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 2. Install dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

If you're having issues with GLUT, you might need:

```bash
pip install freeglut
```

Or alternatively install freeglut using your system package manager (on Linux):

```bash
sudo apt-get install freeglut3 freeglut3-dev
```

### 3. Run the game

```bash
python "Survival Barrage.py"
```

Make sure your terminal or IDE supports OpenGL windows.

---

## 🕹️ Controls

| 🆙️ Key                  | 🔧 Action                                              |
| ------------------------ | ------------------------------------------------------ |
| **W**                    | Move Forward                                           |
| **S**                    | Move Backward                                          |
| **A / D**                | Rotate Gun (In normal mode)                            |
| **A / D**                | Move Left/Right (In Cheat mode)                        |
| **Left Mouse Click**     | Fire Bullet                                            |
| **Right Mouse Click**    | Toggle Camera Mode (Third-Person / First-Person)       |
| ⬆️⬇️⬅️➡️               | Adjust Camera Height & Angle                           |
| **C**                    | Toggle Cheat Mode                                      |
| **V**                    | Toggle Auto Camera (Only in Cheat Mode + First-Person) |
| **R**                    | Restart Game After Game Over                           |

---

## 🏅 Game Rules

* 💪 **Life**: You start with 5 lives. When enemies touch you, you lose a life.
* 🎯 **Score**: Gain 1 point for every enemy hit.
* ❌ **Missed Bullets**: After 10 missed bullets, the game is over.
* 🧩 **Cheat Mode**: Auto-aim and auto-fire enable targeting enemies automatically.

---

## 🚫 Known Issues

* 🔹 Window resizing may cause issues depending on your OpenGL driver.
* 🔹 Performance depends on your graphics card and GLUT implementation.

---


🌟 **Enjoy the game and feel free to contribute!**
