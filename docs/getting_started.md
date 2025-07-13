# Getting Started with Karoloke

Follow these steps to use the `Karoloke` Karaoke application locally:

## **Running the Application Locally**
  - Ensure you have [Poetry](https://python-poetry.org/) installed for dependency management.
  - Install dependencies:
    ```bash
    poetry install
    ```
  - Start the application using the defined task:
    ```bash
    poetry run task start
    ```
  - The main window will open in your default web browser.

## **Application Structure**
  - The main window allows you to select a music number for playback.
  - A settings page lets you configure essential options, such as the directory path for your video files.
  - The playlist page provides an easy-to-read list to help you find and select your desired song quickly.

## **Score Panel and Internet Requirement**
  - After a video finishes playing, the score panel is displayed.
  - **Note:** The score panel is the only part of the application that requires an internet connection, used solely to fetch GIF files for display.

## **Music/Video Files**
  - The project does **not** include any music or video files.
  - You must have your own compatible video files available before using the application.

## **Video Player Compatibility**
  - The video player is embedded in your web browser.
  - The application has been tested on Chrome, Firefox, and Safari for optimal compatibility.

For more details, see the [README.md](../README.md) and the [CONTRIBUTING.md](../CONTRIBUTING.md).
