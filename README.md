# Boli CSM12 Integration for Home Assistant

This integration allows you to integrate your Boli CSM12 energy monitoring device with Home Assistant.

## Features

- Monitor energy consumption
- Real-time power readings
- Historical data tracking

## Installation

### HACS

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click on the three dots in the top right corner and select "Custom repositories"
4. Add the URL of this repository
5. Click "Add"
6. Search for "Boli CSM12" and install

### Manual Installation

1. Download the latest release
2. Unzip the file
3. Copy the `boli_csm12` folder to your Home Assistant `custom_components` directory
4. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Boli CSM12"
4. Enter the host address and port of your device
5. Click "Submit"

## Usage

After configuring the integration, you will see a new sensor entity in Home Assistant that displays the energy consumption from your Boli CSM12 device.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License.
