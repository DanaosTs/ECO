# eClass Organizer

  Keep your lectures organized and up-to-date with the help of ECO, without spending time   going through each course, with a click of a button.

  ![](Demo/sample.gif)

## Table of Contents

  - [Usage](#usage)
  - [Features](#features)
  - [How does it work](#how-does-it-work)
    - [Access to eClass](#-1-access-to-eclass)
    - [Registered Courses](#-2-registered-courses)
    - [Structure of Uploaded Documents](#-3-structure-of-uploaded-documents)
    - [Reconstruction of Directories](#-4-reconstruction-of-directories)
  - [I Don't Trust The Application](#i-dont-trust-the-application)
    - [Requirements](#-requirements)
    - [Libraries Used](#-libraries-used-inside-of-ecopy)
    - [Steps To Create The Executable](#-steps-to-create-the-executable)
  - [Roadmap](#roadmap)

## Usage 

  - Navigate to the `Login Information` tab that's located at the top
  - Input the username, password and semester in their corresponding fields and select `Save Login Information`
  - Return to the `Download` tab to initiate the download process

## Features

  - In-app file explorer
  - Previously installed files are skipped
  - Login information is saved for future use
  - Locally encrypted login information

## How does it work?

### <ins> 1. Access to eClass 

  A GET request is sent to the login page to start the session, a POST request follows with the credentials as the payload to login and the active session cookie that's created once the login is successful is stored. Comparing the cookie before the POST request and after is a way to recognize whether the login attempt was successful or not.

### <ins> 2. Registered Courses

  The part of eClass that gets processed first is the one that contains all of the courses the student is registered in. Similarly, the data is obtained with a GET requests to that subpage, parsed with BeautifulSoup and filtered with regular expressions to obtain the information for every registered course.<br> With that we can now store the title and ID of each course, those will be used for the creation of the folders the files from eClass will be stored in, while the ID will be used to visit each course under the eClass platform.

  E.g. with `CS_U_102` as the course ID  `eclass.uth.gr/courses/CS_U_102/` will be visited

### <ins> 3. Structure of Uploaded Documents

  For every visit, the content of the page is processed and filtered with BeautifulSoup and regular expressions just like before, now the elements that will be stored from it are essentially directories and hypertext references. Directories because eClass allows professors to create folders under their courses, which in turn results in a structure similar to how files are stored in operating systems.

  E.g. with a folder named "Examples" under a course with an ID of `CS_U_102` which can be seen as the "root" directory, the structure looks like: `eclass.uth.gr/courses/CS_U_102/Examples/`

### <ins> 4. Reconstruction of Directories

  For every course that was stored in the first stage, a folder is created that's named after the title of the aforementioned course, then a function is called with the title and the url as arguments. <br> First, all the documents under uth.gr/courses/*Course_ID* are downloaded inside of the corresponding folder, next it checks whether there are folders that should be visited inside of that course. If that is the case, the function is called recursively with the modified url and folder structure as arguments, until there are no more folders to visit.

  E.g. Under course `CS_U_102` there are two subdirectories, `Examples` and `Assignments`\
  The process of downloading the files looks like:

  1. `visit("uth.gr/courses/CS_U_102", "Python")`
  2. Files under CS_U_102 are downloaded inside of the Python folder that was created
  3. The two subdirectories are recognized and stored inside of an array
  4. `visit("uth.gr/courses/CS_U_102/Examples", "Python/Examples")`
  5. Files under CS_U_102/Examples are downloaded inside of the Python/Examples directory
  6. Check if there are subdirectories inside of Examples
  7. `visit("uth.gr/courses/CS_U_102/Assignments", "Python/Assignments")`
  8. Files under CS_U_102/Assignments are downloaded inside of the Python/Assignments directory
  9. Check if there are subdirectories inside of Assignments

  This is how the resulting folder structure will look like: 

  ```
  University/
  └── 8ο Εξάμηνο/
      └── Python/
          ├── Lecture1.pdf
          ├── Lecture2.pdf
          ├── ...
          ├── Examples/
          │   ├── Example1.py
          │   ├── Example2.py
          │   └── ...
          └── Assignments/
              ├── Assignment1.doc
              ├── Assignment2.doc
              └── ...
  ```

## "I Don't Trust The Application"

  I understand there are privacy and security concerns when using your academic credentials in a random application, which is why I wrote this segment in the first place. Inside of the source code it's apparent the login credentials are stored **locally** and are **encrypted**. <br>Since it's not possible to verify that the executable has been created based on the source code, below I provide the instructions for the creation of the executable from scratch.

### <ins> Requirements

  The package that was used for the application is pyinstaller, it "bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules." [from the manual of pyinstaller](https://pyinstaller.org/en/stable/) <br>In short, all that is needed to create the executable is: pyinstaller and all the packages that are used inside of ECO.py

#### <ins> Libraries Used:

  `beautifulsoup4`\
  `bs4`\
  `certifi`\
  `cffi`\
  `charset-normalizer`\
  `cryptography`\
  `docutils`\
  `idna`\
  `Kivy`\
  `Kivy-Garden`\
  `pycparser`\
  `Pygments`\
  `requests`\
  `soupsieve`\
  `urllib3`

  To download the packages for the libraries execute
  ```
  pip install beautifulsoup4 bs4 certifi etc...
  ```
  Or alternatively to download all of them at once 
  ```
  pip install -r requirements.txt
  ```

### <ins> Steps To Create The Executable

  1. Navigate to the directory `ECO.py` is located in, either from the terminal inside of your preferred IDE or the command prompt\
  i.e `cd Downloads\ECO`\
  Executing either `dir` or `ls` should display `ECO.py`

  2. To ensure there are no issues, run `ECO.py` after installing the packages

  3. Execute 
      ```
      pyinstaller --onefile --windowed --icon=ECOIcon.ico ECO.py
      ```
      `--onefile` creates a one-file bundled executable\
      `--windowed` restricts the console window from opening when running the   application\
      `--icon` Applies the provided icon to the executable (Note: The icon has to be  placed inside of the folder the executable is in, for it to be displayed when  running the executable)

  4. The executable is stored inside of the "dist" folder that has been created

## Roadmap

  - Add option to set download location of the University folder
  - Add the ability to choose which courses should be downloaded
  - Add comments inside of the source code