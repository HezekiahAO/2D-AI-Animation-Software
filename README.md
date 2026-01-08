🎬 TweenCraft

AI-Assisted 2D Animation Tool for Clean-Up & In-Betweening

TweenCraft is a Python-based desktop application designed to assist traditional 2D animators by reducing the most repetitive and time-consuming parts of the animation workflow specifically clean-up (lineart refinement) and in-between frame generation.

Rather than replacing animators, TweenCraft augments the classical animation process, allowing artists to focus more on creativity, motion, allowing artists to focus on creativity and storytelling while AI reduces repetitive, labor-intensive work.

Project Goals

1 Reduce manual animation workload by up to 50%

2 Assist (not replace) traditional 2D animation workflows

3 Provide a simple, animator-friendly interface

4 Build an understandable and extendable prototype for learning and iteration



Problem Statement

Traditional 2D animation requires animators to repeatedly redraw similar frames for clean-up and in-betweening. This repetitive manual work leads to:

Artist fatigue and burnout

Slower production timelines

Reduced creative focus

TweenCraft addresses this by introducing AI-assisted tools that automate repetitive steps while keeping the animator in full creative control.



Key Features

    Drawing & Frame Management

Hand-drawn frame creation using mouse or tablet

Frame-by-frame navigation (Prev / Next)

Undo & redo per frame

Basic animation playback

Onion skinning showing previous & next frame visualization



AI-Assisted Tools (Prototype Stage)

AI Clean-Up (Lineart Generation)
Converts rough sketches into cleaner visual output using image processing using OpenCV-based as placeholder logic.

AI In-Betweening (Conceptual)
Designed to generate intermediate frames between keyframes to smooth motion.
(Currently implemented as a structured placeholder for future AI models.)

Note: AI features are intentionally lightweight and modular in this prototype. Deep learning models (PyTorch/TensorFlow) are planned for future versions.



User Interface

The UI is inspired by existing animation software and focuses on:

Minimal visual clutter

Clear labeling

Button-driven actions

Familiar animation concepts (frames, onion skin, playback)

The goal is to feel like an animation tool first — not a technical AI application.



Tech Stack
Core Technologies used are:

Python 3

PySide6 (Qt for Python) — Desktop UI

OpenCV (cv2) — Image processing

NumPy — Numerical & image array handling

Planned / Optional

PyTorch — Deep learning models for advanced clean-up & interpolation

OpenCV advanced pipelines Edge detection, skeletonization, refinement 

Installation:
1. Clone the repo:

git clone https://github.com/HezekiahAO/2D-AI-Animation-Software.git
then cd tweencraft

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the app:
python ai_app.py


    Project Structure:

tweencraft/
│
├── ai_app.py              # Main application file
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── assets/                # (Optional) Saved images / exports


Architecture Overview

    DrawingCanvas

Handles drawing input

Stores frame data

Renders onion skin & current frame

Converts frames to images


    MainWindow

Manages UI controls

Handles frame navigation

Triggers AI actions

Controls playback

    AI Logic (Prototype)

Image-based processing using OpenCV

Modular design for future ML models


    Performance & Scalability

Fast application startup

Lightweight frame storage for prototypes

AI processing designed to be on-demand, not always running

Architecture allows future batching, caching, and GPU acceleration

The long-term goal is to scale from small animation tests to full scenes without compromising usability.


    Diversity & Inclusion Considerations

TweenCraft is designed to be accessible to animators regardless of technical background. The interface minimizes complexity, avoids jargon, and respects established animation workflows. By reducing repetitive labor, the tool supports healthier creative practices and makes animation more accessible to independent artists, students, and creators with limited resources.


    Team

Developer:
This project is currently developed by a single creator with a background in:

Software development

Engineering

Creative arts

TweenCraft was born from firsthand awareness of both technical problem-solving and creative burnout in production workflows.


    Current Limitations

AI features are prototype-level

No deep learning models trained yet

No export pipeline (image sequence / video) implemented

Designed for learning and iteration, not production deployment (yet)



    Future Enhancements

Deep learning-based lineart extraction

AI-driven frame interpolation

Export to PNG image sequences

Timeline UI improvements

Style consistency per project

Plugin or pipeline integrations


    License

This project is developed for educational, research, and hackathon demonstration purposes.
The code is released under the MIT License.



    Note

TweenCraft is intentionally built to be understandable, hackable, and expandable.
The focus is not perfection, but learning, iteration, and real creative impact.