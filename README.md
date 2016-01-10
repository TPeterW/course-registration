Course Registration
===================

Cross platform program for registering for classes for Middlebury College Bannerweb system.


Modification
----
* Packed into executables, easier for non Python lovers to use

* Allowed user to type in their information

* Added cache function, user can save their configuration for a future registration and come back later. Configuration saved in 'reg.ini' file, not visible on OS X.

Usage
-----
__Windows__

To be added...

__OS X__

Decompress (unzip) the .zip file, and double click on the executable.
_Note_: before first launch, if your security setting only allows apps made by "Mac App Store and identified developers", you wll receive a security warning. To disable it and run the program, go to "System Preferences" then "Security & Privacy", and click on "Open Anyway".

__Linux__

Decompress the tar.gz file

    tar -xzvf Course_Registration_Linux.tar.gz

Enter extracted folder, and execute in terminal.



Known Limitation
----
* Does not handle exceptions that happen during the part where emulated browser opens the registration page

* Only checks the format of term_string, but does not check validity 

* Source code all in one file, will change soon. Sorry to other contributor (if any) ╮(╯▽╰)╭ .
