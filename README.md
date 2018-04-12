# Blackbox™
#### Dropbox for Blackboard

___

## **Description**

Blackbox™, an amalgamation of Blackboard and Dropbox, magically albeit hackily syncs your NTUlearn files (well, most of them) just like how Dropbox seamlessly does so.

___

## **Mechanics**

For the uninitiated, Blackbox™ is written in Python and uses Selenium to automate a special Chrome browser (called the Chrome web driver) that is built for web testing.

It logs you into Blackboard, iterates through all your courses and then downloads all uploaded documents for you.

___

## **How to Use**

#### Step 1 - Input Your Username, Password and Directory Path

Open ```blackbox.py``` and look for the following:

```
BLACKBOARD_USERNAME = "REPLACE_ME"
BLACKBOARD_PASSWORD = "REPLACE_ME"
CHROMEDRIVER_PATH = "REPLACE_ME"
```

Edit the above with your information accordingly.

#### Step 2 - Install Dependencies

Windows:

```
$ pip install selenium
$ cd path/to/working/directory
$ python blackbox.py
```

Mac:

```
$ sudo pip3 install selenium
$ cd path/to/working/directory
$ python3 blackbox.py
```

___

## **Screenshots**

#### 1. Executing the Script

![1.JPG](images/1.JPG?raw=true)

#### 2. Initializing Chrome Web Driver

![2.JPG](images/2.JPG?raw=true)

#### 3. Automating Downloads on Chrome Web Driver

![3.JPG](images/3.JPG?raw=true)

#### 4. Course Directory on Local Machine

![4.JPG](images/5.JPG?raw=true)

#### 5. Course File Downloads on Local Machine

![5.JPG](images/4.JPG?raw=true)

___

## **Limitations**

Blackbox™ kills all unfinished downloads per module within 15 seconds.

___

## **Potential Improvements**

- Analyzing file size to determine whether a (large) file should be downloaded or not.

- Preventing duplicate downloads for  previously-downloaded files.

- Notifies you when new files have been synced.

- Run as an compiled executable on all platforms.

___

## **Disclaimer**

This is a code snippet used in a workshop and is not meant to be production-ready.

It is only meant to demonstrate how Selenium works; using a headless web driver is definitely a more elegant solution.

The author is not liable for any damages suffered by your machine in your course of using Blackbox™.
