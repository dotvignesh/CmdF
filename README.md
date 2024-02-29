# CmdF

CmdF is a terminal app that allows you to search and seek through YouTube videos using the power of whisper.cpp and fuzzy string matching.

## Demo


https://github.com/dotvignesh/CmdF/assets/19832025/edee34ed-9e24-4bcf-8e4e-7630efd85667



## Installation

To install and run the application, follow the instructions below:

1. Clone the repository using Git:

   ```bash
   git clone https://github.com/dotvignesh/CmdF.git
   ```

2. Change into the repository directory:

   ```bash
   cd CmdF
   ```

3. Create a conda environment:

   ```bash
   conda create --name cmdf
   ```
   
4. Activate the new conda environment:

   ```bash
   conda activate cmdf
   ```
   
5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Install whisper.cpp (if not already installed):
   - Go to [whisper.cpp repo](https://github.com/ggerganov/whisper.cpp)
   - Follow the instructions to set up and install whisper.cpp

7. Set `whisper_path` in `main.py` to your whisper.cpp installation location

8. Run the application from your terminal:

   ```bash
   python main.py
   ```

The application should now be running in the background.


## Usage

Once the app is running, go to the video you want to search through, and hit `F9` 
(NOTE: the video will be downloaded and transcribed in the background - time varies depending on video length)

After the video has been processed, hit `Cmd + F`, type in your query, and press `F10`
Voila, the exact location in the video will be opened in a new tab!!

Enjoy searching and skimming through your videos!

