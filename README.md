# Literature Clock for InkyWHAT

This project implements a "Literature Clock" on a Raspberry Pi Zero with an InkyWHAT display. The clock draws quotes from literature to display the current time in a highlighted context. For times without a corresponding quote, the display repeats the most recent quote until a new one is reached.

---

## Features
- **Dynamic Quotes**: The clock displays quotes where the time is embedded in the text.
- **Time Highlighting**: The time in the quote is highlighted using a bold, monospaced font.
- **Date and Author Display**: Includes the current date in a friendly format and the author or source of the quote.
- **Dynamic Font Scaling**: Adjusts text size dynamically to fit the InkyWHAT display.

---

## How It Works
1. **Data Source**: The quotes are sourced from the `litclock_annotated.csv` file. Not all times have a corresponding quote, so the script will repeat the last displayed quote until a time with a quote is reached.
2. **Rendering**: The script uses Python's `Pillow` library to render text and graphics on the InkyWHAT display.
3. **Hardware Support**: It leverages the `inky` library for communication with the InkyWHAT display.
4. **Schedule**: The script is set to run every minute using `cron`, ensuring the time is updated dynamically.

---

## Installation Guide

### Prerequisites
- **Hardware**: Raspberry Pi Zero (or compatible) with an InkyWHAT display ("black" variant).
- **Software**: Raspberry Pi OS with Python 3.

### Step 1: System Setup
1. Update your system:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Install required system libraries:
   ```bash
   sudo apt install -y python3 python3-pip python3-venv libfreetype6 libfreetype6-dev libjpeg-dev zlib1g-dev fonts-freefont-ttf
   ```

### Step 2: Clone the Repository
1. Clone this repository:
   ```bash
   git clone https://github.com/RFNajera/literature-clock-inkyWHAT.git
   cd literature-clock-inkyWHAT
   ```

### Step 3: Set Up Virtual Environment
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
1.5 I did it without a virtual environment, but I had to give system-wide permissions. A virtual environment is easier and safer for your system, especially if you're new at this.

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Configure the Display
1. Run the Pimoroni setup script to ensure hardware drivers are installed:
   ```bash
   curl https://get.pimoroni.com/inky | bash
   ```

### Step 5: Test the Script
1. Run the script manually to verify:
   ```bash
   python3 pi_clock_what3.py
   ```

---

## Running the Script on Boot

### Step 1: Add a Cron Job
1. Open the `crontab` editor:
   ```bash
   crontab -e
   ```

2. Add the following line to run the script every minute:
   ```bash
   * * * * * /home/pi/litclock-inkywhat/venv/bin/python /home/pi/litclock-inkywhat/pi_clock_what3.py
   ```

3. Save and exit the crontab editor.

---

## Caveats
1. **Quote Coverage**: The `litclock_annotated.csv` file does not include quotes for all times. The script will repeat the last displayed quote until a time with a new quote is reached.
2. **Display Type**: This project is configured for the "black" variant of the InkyWHAT display. Other color variants may require changes in the script's color configuration.
3. **Performance**: The Raspberry Pi Zero's limited processing power may lead to slight delays in rendering large quotes or handling frequent updates.

---

## Customization
- To change fonts, update the paths in the script where `FreeSans.ttf` or `FreeMonoBold.ttf` are referenced.
- You can add more quotes to the `litclock_annotated.csv` file for better coverage.

---

## Credits
- Forked from [docPhil99](https://github.com/docPhil99/literature-clock)
- **Hardware**: [Pimoroni InkyWHAT](https://shop.pimoroni.com/products/inky-what?variant=13590497624147)
- **Libraries**: `Pillow`, `inky`

---

For more details or troubleshooting, please refer to the repository's issues section or contact the maintainers.

