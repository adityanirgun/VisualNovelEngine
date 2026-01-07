
# Aes Grave + Visual Novel Engine 2.1 Alpha
The first episode of Aes Grave presented at the Capital Creative Showcase 2025 running on an original-design, open-source game creation engine. Visit my [itch.io page](https://sundaynothing.itch.io/) for a link to the prelude episode.

Runs on virtually any specs. Max res 1920x1080

From itch.io page:

"A free game. A visual novel experience that presents the motion picture, sound, and literature in a new way. Tell your friends. More to be released, this is an early preview. This is only the first part of the first sequence of the first chapter. The visual novel engine is a custom built tool that can be used to create experiences of ones own. Documentation pending.

Game engine github: https://github.com/adityanirgun/VisualNovelEngine.git

__Published__	 Jun 14, 2025

__Status__	In development

__Author__	SundayNothing

__Genre__	Visual Novel

__Tags__	Horror, Indie, Psychological Horror"






## Controls
How to play:
* __spacebar__ or __click__ to continue
* __F__ to toggle fullscreen
* __L__ to toggle log
* __m__ at menu to cycle releases
* __ctrl__ to skip
* __f1__ to save at chapter checkpoints
* __f2__ to load
* __esc__ to menu and __esc__ again to exit from menu
* __scroll wheel__ to go back within the chapter 
 
## Installation

unpack zip

navigate to VisualNovelEngine/main.py

run main.py

edit save_data.json to skip

edit timeline.json to write your own story

nagivate to VisualNovelEngine/resources to upload:

/frames - images, animation frames 

/media - audio, sfx

## Run Locally

Clone the project

```bash
  git clone https://github.com/adityanirgun/VisualNovelEngine.git
```

Go to the project directory

```bash
  cd VisualNovelEngine
```

Install dependencies

```bash
   pip install -r requirements.txt
```

Start the server

```bash
  python3 main.py
```

