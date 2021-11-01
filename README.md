# Music Framework
Generative music framework which composes music in Python and renders it electronically in Csound.

## Core Components
* **classes.py** - Defines the classes and methods which form the building blocks of the musical compositions, including `Piece`, `Mode`, `Voice`, `Line`, and `Note`. Upon initialization, these classes randomly select the instrumentation and generate the beginning melodies of each instrument.
* **rules.py** - Defines the `RuleEngine` and `Rule` classes, which are responsible for transforming the melodies of the instruments throught the piece.  `Rules` are constructed using `@classmethods` decorators so that `Rules` can perform a variety of transformations. Examples of transformations include `Chord Change`, `Evolve`, `Mimic`, and `Mute`.
* **orchestra.orc** - 
* **elements.py** - 
* **main.py** - 
