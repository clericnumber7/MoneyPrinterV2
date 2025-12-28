"""
Utility Functions for MoneyPrinter V2

This module provides utility functions for file operations, network requests,
and system management used throughout the application.

All functions include proper error handling and cross-platform support.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import os
import random
import zipfile
import requests
from typing import Optional

from status import *
from config import *
from platform_utils import ProcessManager, PlatformDetector


def close_running_selenium_instances() -> bool:
    """
    Closes any running Selenium/Firefox instances to prevent conflicts.

    This function is cross-platform and will use the appropriate method
    for the current operating system (Windows, Linux, or macOS).

    Returns:
        bool: True if successfully closed instances, False otherwise

    Example:
        >>> close_running_selenium_instances()
        True
    """
    try:
        info(" => Closing running Selenium instances...")

        # Use cross-platform process manager
        success_status = ProcessManager.kill_firefox_instances()

        if success_status:
            success(" => Closed running Selenium instances.")
        else:
            warning(" => Some Firefox instances may still be running.")

        return success_status

    except Exception as e:
        error(f"Error occurred while closing running Selenium instances: {str(e)}")
        return False


def build_url(youtube_video_id: str) -> str:
    """
    Builds the full URL to a YouTube video from its video ID.

    Args:
        youtube_video_id (str): The YouTube video ID (11 characters)

    Returns:
        str: The full YouTube video URL

    Example:
        >>> build_url("dQw4w9WgXcQ")
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    """
    if not youtube_video_id:
        raise ValueError("YouTube video ID cannot be empty")

    return f"https://www.youtube.com/watch?v={youtube_video_id}"


def rem_temp_files() -> int:
    """
    Removes temporary files in the `.mp` directory.

    Only removes non-JSON files, preserving cache and configuration files.
    This helps prevent disk space issues from accumulated temporary content.

    Returns:
        int: Number of files successfully removed

    Example:
        >>> rem_temp_files()
        5  # Removed 5 temporary files
    """
    try:
        # Path to the `.mp` directory
        mp_dir = os.path.join(ROOT_DIR, ".mp")

        # Ensure directory exists
        if not os.path.exists(mp_dir):
            if get_verbose():
                warning(f" => Temp directory {mp_dir} does not exist yet.")
            return 0

        files = os.listdir(mp_dir)
        removed_count = 0

        for file in files:
            # Skip JSON files (they contain cache data)
            if not file.endswith(".json"):
                file_path = os.path.join(mp_dir, file)

                # Only remove files, not directories
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        removed_count += 1
                        if get_verbose():
                            info(f" => Removed temp file: {file}")
                    except Exception as e:
                        if get_verbose():
                            warning(f" => Could not remove {file}: {e}")

        if get_verbose() and removed_count > 0:
            success(f" => Removed {removed_count} temporary files.")

        return removed_count

    except Exception as e:
        error(f"Error occurred while removing temp files: {str(e)}")
        return 0


def fetch_songs() -> bool:
    """
    Downloads background music into the Songs/ directory for use with generated videos.

    This function:
    1. Creates the Songs directory if it doesn't exist
    2. Downloads a ZIP file containing royalty-free music
    3. Extracts the ZIP contents
    4. Cleans up the ZIP file

    If songs are already downloaded, this function skips the download.

    Returns:
        bool: True if songs were successfully fetched or already exist, False on error

    Example:
        >>> fetch_songs()
        True  # Songs downloaded successfully
    """
    try:
        info(f" => Fetching songs...")

        files_dir = os.path.join(ROOT_DIR, "Songs")

        # Create Songs directory if it doesn't exist
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
            if get_verbose():
                info(f" => Created directory: {files_dir}")
        else:
            # Check if songs already exist
            existing_files = [f for f in os.listdir(files_dir) if f.endswith(('.mp3', '.wav'))]
            if len(existing_files) > 0:
                if get_verbose():
                    success(f" => Songs already exist ({len(existing_files)} files). Skipping download.")
                return True

        # Get ZIP URL from config or use default
        zip_url = get_zip_url()
        if not zip_url:
            zip_url = "https://filebin.net/bb9ewdtckolsf3sg/drive-download-20240209T180019Z-001.zip"

        if get_verbose():
            info(f" => Downloading songs from: {zip_url}")

        # Download songs with timeout
        try:
            response = requests.get(zip_url, timeout=60)
            response.raise_for_status()  # Raise exception for bad status codes
        except requests.exceptions.RequestException as e:
            error(f"Failed to download songs: {e}")
            return False

        # Save the zip file
        zip_path = os.path.join(files_dir, "songs.zip")
        with open(zip_path, "wb") as file:
            file.write(response.content)

        if get_verbose():
            info(f" => Downloaded {len(response.content)} bytes")

        # Unzip the file
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall(files_dir)
            if get_verbose():
                info(f" => Extracted songs to {files_dir}")
        except zipfile.BadZipFile:
            error("Downloaded file is not a valid ZIP archive")
            os.remove(zip_path)
            return False

        # Remove the zip file
        os.remove(zip_path)

        success(" => Downloaded Songs to ../Songs.")
        return True

    except Exception as e:
        error(f"Error occurred while fetching songs: {str(e)}")
        return False


def choose_random_song() -> Optional[str]:
    """
    Chooses a random song from the Songs/ directory for use as background music.

    Returns:
        Optional[str]: Path to the chosen song file, or None if no songs available

    Raises:
        FileNotFoundError: If Songs directory doesn't exist

    Example:
        >>> song_path = choose_random_song()
        >>> print(song_path)
        '/path/to/project/Songs/background_music_1.mp3'
    """
    try:
        songs_dir = os.path.join(ROOT_DIR, "Songs")

        # Verify directory exists
        if not os.path.exists(songs_dir):
            error(f"Songs directory not found: {songs_dir}")
            error("Please run fetch_songs() first.")
            return None

        # Get list of audio files
        all_files = os.listdir(songs_dir)
        songs = [f for f in all_files if f.endswith(('.mp3', '.wav', '.ogg', '.m4a'))]

        if len(songs) == 0:
            error("No songs found in Songs directory")
            error("Please run fetch_songs() to download background music.")
            return None

        # Choose random song
        song = random.choice(songs)
        song_path = os.path.join(songs_dir, song)

        if get_verbose():
            success(f" => Chose song: {song}")

        return song_path

    except Exception as e:
        error(f"Error occurred while choosing random song: {str(e)}")
        return None


def validate_file_exists(file_path: str, description: str = "File") -> bool:
    """
    Validates that a file exists and provides clear error messaging.

    Args:
        file_path (str): Path to the file to validate
        description (str): Human-readable description of the file (for error messages)

    Returns:
        bool: True if file exists, False otherwise

    Example:
        >>> validate_file_exists("/path/to/config.json", "Configuration file")
        True
    """
    if not os.path.exists(file_path):
        error(f"{description} not found: {file_path}")
        return False

    if not os.path.isfile(file_path):
        error(f"{description} is not a file: {file_path}")
        return False

    return True


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensures a directory exists, creating it if necessary.

    Args:
        directory_path (str): Path to the directory

    Returns:
        bool: True if directory exists or was created, False on error

    Example:
        >>> ensure_directory_exists("/path/to/output")
        True
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            if get_verbose():
                success(f" => Created directory: {directory_path}")
        return True
    except Exception as e:
        error(f"Failed to create directory {directory_path}: {e}")
        return False
