# sw_mc_lib
Stormworks Microcontroller library

This is a library aimed at simplifying parsing, manipulating and formatting
Stormworks Microcontrollers (Microprocessors). It includes a custom XML parser,
that allows for the games quirks, and is tailored to the needs.
It may be used without the Microcontroller parser, if you want to parse i.e.  Vehicles.

## Goals

 - Make Microprocessor parsing great again
 - Accurate emulation of the games behaviour
 - In case of a conflict, use the design from the GUI rather than the XML
   - For composite read/write, this means that properties like `start_channel` are one based like in the gui rather than zero based.
   - Several names have been changed towards the GUI language.
 - Try to parse reasonably ill-formed Microcontrollers and use defaults where necessary
 - Don't use RegEx (it has other uses, but not this one)

In case you see any violation of those rules, feel free to open an issue.
