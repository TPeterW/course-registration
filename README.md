Course Registration
===================

Cross platform program for registering for classes for Middlebury College Bannerweb system. Based on the [script](https://github.com/danielhtrauner/course-registration "script") by [@danielhtrauner](https://github.com/danielhtrauner "Daniel").


Modifications
----
* Packed into executables, easier for non Python lovers to use

* Allowed user to type in their information

* Added cache function, user can save their configuration for a future registration and come back later. Configuration saved in 'reg.ini' file.

Installation
-----
__Windows__

Decompress (unzip) downloaded .zip file, and double click on the __.exe__ executable.

Configuration file is at "C:\\Users\\YOUR_USER_NAME\\AppData\\Local\\CourseRegistration\\reg.ini"

__OS X__

Decompress (unzip) downloaded .zip file, and double click on the executable.

Configuration file is at "/Library/Caches/Course\ Registration/reg.ini"

_Note_: before first launch, if your security setting only allows apps made by "Mac App Store and identified developers", you wll receive a security warning. To disable it and run the program, go to "System Preferences" then "Security & Privacy", and click on "Open Anyway".

__Linux__

Decompress the tar.gz file

    tar -xzvf Course_Registration_Linux.tar.gz

Execute program in extracted folder from terminal

    ./course_registration/course_registration

Configuration file is at program directory

Usage
-----
Instructions are clear inside the program, one thing to note is that the program memorises your registration date and registration plan including CRNs and alternate PIN.
You can simply enter your specifications and exit the program by clicking the "x" button or ctrl+c. You will be able to recover your records next time the program is run.
To secure more sleep, you can simply leave your laptop on over night, make sure it doesn't go to sleep, and the program will execute at 7:00am sharp.

If you have any questions, please don't hesitate to contact me via taow@middlebury.edu.
有问题发我明德邮箱，专业抓虫20年。

Known Limitations
----
* Does not handle exceptions that happen during the part where emulated browser opens the registration page

* Only checks the format of term_string, but does not check validity

* Source code all in one file, will change soon. Sorry to other contributor (if any) ╮(╯▽╰)╭ .


Goals
----
* Graphical Interface

* Multithreading, enable separation of class, allow users to enter a group of CRNs that are for one class, and try them together on one thread.
