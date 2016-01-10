Course Registration
===================

Cross platform program for registering for classes for Middlebury College Bannerweb system. Based on the [script](https://github.com/danielhtrauner/course-registration "script") by [@danielhtrauner](https://github.com/danielhtrauner "Daniel").


Modifications
----
* Packed into executables, easier for non Python lovers to use

* Allowed user to type in their information

* Added cache function, user can save their configuration for a future registration and come back later. Configuration saved in 'reg.ini' file, not visible on OS X.

Usage
-----
__Windows__

Decompress (unzip) downloaded .zip file, and double click on the __.exe__ executable.

__OS X__

Decompress (unzip) downloaded .zip file, and double click on the executable.
_Note_: before first launch, if your security setting only allows apps made by "Mac App Store and identified developers", you wll receive a security warning. To disable it and run the program, go to "System Preferences" then "Security & Privacy", and click on "Open Anyway".

__Linux__

Decompress the tar.gz file

    tar -xzvf Course_Registration_Linux.tar.gz

Execute extracted program in terminal

    ./course_registration



Known Limitations
----
* Does not handle exceptions that happen during the part where emulated browser opens the registration page

* Only checks the format of term_string, but does not check validity 

* Source code all in one file, will change soon. Sorry to other contributor (if any) ╮(╯▽╰)╭ .


Goals
----
* Graphical Interface

* Multithreading, enable separation of class, allow users to enter a group of CRNs that are for one class, and try them together on one thread.