<h1 align="center"><img src="./data/icons/Sparkamek.svg" width="32" align="center" /> Sparkamek: Add Code to NSMBW with Ease</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-blue" />
  </a>
  <a href="https://doc.qt.io/qtforpython/index.html">
    <img alt="PySide 6" src="https://img.shields.io/badge/PySide-6.4.1-brightgreen" />
  </a>
  <a href="https://github.com/Synell/Sparkamek/blob/master/LICENSE">
    <img alt="License: LGPL" src="https://img.shields.io/badge/License-LGPL-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows, Linux and MacOS" src="https://img.shields.io/badge/Platforms-Windows%20|%20Linux%20|%20MacOS-yellow" />
  <a href="https://www.buymeacoffee.com/synell">
    <img alt="Donate: Buy me a coffee" src="https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-orange" target="_blank" />
  </a>
  <a href="https://www.patreon.com/synel">
    <img alt="Donate: Patreon" src="https://img.shields.io/badge/Donate-Patreon-red" target="_blank" />
  </a>
</p>

----------------------------------------------------------------------

Sparkamek is an app for Windows, Linux and MacOS. Kamek is a tool that allows you to add custom code to New Super Mario Bros. Wii. Sparkamek allows you to create, edit and build Kamek projects with ease. Everything is done in a simple and easy to use GUI.


## Requirements

### Windows
- Windows 7 or later
- VC++ 2015 Redistributable

### Linux
- All Linux distributions supported by PySide6

### MacOS
- MacOS 10.14 (Mojave) or later


### Source Code
- Python 3.11 or later
  - Dependencies (use `pip install -r requirements.txt` in the project root folder to install them)


## Installation

### Windows, Linux and MacOS

<a href="https://github.com/Synell/Sparkamek/releases/latest">
  <img alt="Release: Latest" src="https://img.shields.io/badge/Release-Latest-00B4BE?style=for-the-badge" target="_blank" />
</a>

- Download the latest release from the [releases page](https://github.com/Synell/Sparkamek/releases) and extract it to a folder of your choice.


## Customization

### Language

- You can customize the language of the app by adding a new file into the `/data/lang/` folder. The language must be a valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) code. If the language is not supported, the app will default to English. Then, you can change the language in the settings menu.

  *See [this file](https://github.com/Synell/Sparkamek/blob/main/data/lang/english.json) for an example.*

### Theme

- You can customize the theme of the app by adding new files into the `/data/themes/` folder. The theme must be contain valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) codes and valid [QSS](https://doc.qt.io/qt-6/stylesheet-reference.html) codes. If the theme is not supported, the app will default to the default theme. Then, you can change the theme in the settings menu.

  *See [this file](https://github.com/Synell/Sparkamek/blob/main/data/themes/neutron.json) and [this folder](https://github.com/Synell/Sparkamek/tree/main/data/themes/neutron) for an example.*


## Why Sparkamek?

### Kamek is a great tool, but...

Doing a lot of NSMBW modding, I found myself using Kamek a lot as it is used to compile the code. However, I found it very annoying to use as it for debugging for multiple reasons:
- No colors, so it's hard to read
- When using the fasthack option, it doesn't show the correct line number of the errors / warnings (it shows the line number of the fasthack instead, which is about 50 000 lines so good luck scrolling to the correct line, even with the search function)
- It doesn't show the file name of the errors / warnings
- No spacing, everything is cramped together
- When you have an error, it generates so much garbage that it's hard to find the error itself, because it's at the very top of the log

Okay, so if this didn't convince you, let me tell you a short story.

So one day I just wanted to test how much garbage the compiler gives, so I just remove a single `;` from a file called `boss.h`, and the rest of the code had no error. Now, if I compile this, we should in theory have a single error.

You know what, it threw me **1041 errors, in 24 different files**.
Like wtf, just for a single missing `;` ? And the worst part is that this represents 4 243 lines of garbage, and the correct error is at the very top of the log, under a lot of warnings, so good luck finding it on the command line with no color.

By the way, if you want to check the output for yourself, here it is, with all the warnings and the top of the log removed for your mental health: [error.log](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/files/error.log).

And here is the output of Sparkamek for the same error:
![Small output from Sparkamek](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/error-very-small.png)

Much better, right?


### So, what does Sparkamek do?

Sparkamek is a GUI for Kamek, so it does the same thing as Kamek, but with a lot of improvements. It also allows you to compile a custom loader for your game with improved features, like with the Kamek one.

You can also create and edit the Reggie Next (the level editor app) spritedata file with ease, which is use to create patches for the it.

And finally, you can also create and edit the Riivolution file with ease, which is used to create patches for the game.


## Usage

### First Start

When you start the app for the first time, you'll see this screen:
![No project opened screen](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/first-time.png)

Click on the `Open Project` button and follow the instructions to create a new project.

Once you have created a project, you'll have 1 to 4 tabs.

### Loader Tab

todo


### Kamek Tab

#### Sprites and actors

Here you can check the sprites and actors that are in the game.

*Note that the the sprites of this list are to take with a grain of salt, as they are not 100% accurate (because it requires putting the sprites replacement comment and using good profile names).*

![Sprites and actors](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-sprites-and-actors.png)

#### Compilers

Here you can compile the code for the game. The compiler has 2 modes: simple and complete.

The complete mode is the same as the Kamek one, but with colors, spacing and the correct line number for the errors / warnings whereas the simple mode is a lot more compact and only shows essential information.

![Simple compiler](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-compiler-simple.png)

![Complete compiler](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-compiler-complete.png)

#### Symbols

Here you can check the symbols that are compiled, for debugging purposes.

![Sprites and actors](https://raw.githubusercontent.com/Synell/Assets/main/Sparkamek/readme/kamek-symbols.png)


### Reggie Next Tab

todo


### Riivolution / Game Tab

todo
