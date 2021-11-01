# Music Framework
<p align="center"><img src="https://jasonhallen.com/images/images/music_generator1.jpg" title="Listen to an album composed by the music generator." alt="Album composed by the music generator" height="200">

Generative music framework which composes music in Python and renders it electronically in Csound.

## Core Components
* **classes.py** - Defines the classes and methods which form the building blocks of the musical compositions, including `Piece`, `Mode`, `Voice`, `Line`, and `Note`. Upon initialization, these classes randomly select the instrumentation and generate the beginning melodies of each instrument.
* **rules.py** - Defines the `RuleEngine` and `Rule` classes, which are responsible for transforming the melodies of the instruments throught the piece.  `Rules` are constructed using `@classmethods` decorators so that `Rules` can perform a variety of transformations. Examples of transformations include `Chord Change`, `Evolve`, `Mimic`, and `Mute`.
* **orchestra.orc** - Contains the Csound orchestra code that defines the instruments available for random selection by `classes.py`.  Instruments include plucked string, organ, Rhodes piano, marimba, bass, and many different drum kits.
* **elements.py** - Static lists of data used by `classes.py` for selecting scales, chord voicings, and instrumentation.
* **main.py** - 
