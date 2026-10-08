# Alternate Tuning Assistant Reference

## Note notation
Enter strings from lowest pitch to highest pitch.
Each note must include an octave number, such as E2, F#2, or Bb2.
The assistant supports six, seven, or eight strings.
C4 is middle C. Each octave contains twelve semitones.

## Common six-string tunings
Standard: E2 A2 D3 G3 B3 E4
D standard: D2 G2 C3 F3 A3 D4
C standard: C2 F2 Bb2 Eb3 G3 C4
Drop D: D2 A2 D3 G3 B3 E4

## Intervals
0 semitones: unison
1: minor second
2: major second
3: minor third
4: major third
5: perfect fourth
6: tritone
7: perfect fifth
8: minor sixth
9: major sixth
10: minor seventh
11: major seventh
12: octave

## Creative profiles
Dissonant patterns use close upper-string intervals.
Atmospheric patterns use wider spacing.
Heavy patterns emphasize fifths and octaves.
These are creative starting points; musical effect also depends
on rhythm, articulation, amplification, and the notes played.

## Calculation rules
Python validates notes and calculates intervals and transpositions.
Transposing every string equally preserves the intervals.
The model explains results and suggests playing ideas.

## Instrument setup
A calculated tuning is not a guarantee of physical safety.
String tension depends on pitch, string gauge, and scale length.
Large changes may require different strings and a setup.
The app conservatively refuses changes greater than two semitones
up or twelve semitones down per string in a single operation.
Those limits are project rules, not universal safety thresholds.
Ask a guitar technician about tension, setup, or modifications.
The assistant does not listen to audio or measure actual tension.
