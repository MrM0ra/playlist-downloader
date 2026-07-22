# Playlist Downloader

This project automates the download process for a list of songs by searching each title on YouTube, opening the video link in Y2Mate, and starting the conversion/download flow.

## How it works

The script performs the following steps for each item in the playlist:

1. Loads a list of song names from a JSON file.
2. Opens Google Chrome in incognito mode using Selenium.
3. Searches the song on YouTube.
4. Opens the first result and copies its URL.
5. Visits Y2Mate and submits the video URL for conversion.
6. Clicks the download button and confirms the system dialog using PyAutoGUI.
7. Repeats the process for the next song until the list is finished.

## Project files

- `download-playlist.py`: main script that automates the download flow.
- `playlist_sample.json`: example input file with a sample list of songs.

## Dependencies

Install the required Python packages:

```bash
pip install selenium pyautogui
```

You also need:

- Python 3.x
- Google Chrome installed

## Configuration

Edit `playlist_sample.json` and replace the sample song names with the tracks you want to download.

Example format:

```json
{
  "canciones": [
    "Magalenha - Sérgio Mendes audio hq",
    "Hot In Herre - Nelly audio hq",
    "Culo - Pitbull, Lil Jon audio hq",
    "Shape Of My Heart - Sting audio hq"
  ]
}
```

## Execution

Run the script from the project folder:

```bash
python download-playlist.py
```

The script will read the JSON file named `playlist_sample.json` by default.

## Notes

- This project relies on web automation and may be affected by changes in the websites it uses.
- Some download pages may show pop-ups or captchas that require manual intervention.
- Use this tool responsibly and in accordance with the terms of service of the websites involved.

## Tutorial and explanation

- https://youtu.be/HAKzbbWLKx8
