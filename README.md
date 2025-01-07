# Health Check Program

## Prerequisites
### 1. Install Python
Ensure Python 3.8 or later is installed.

### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install requests pyyaml
```

#### Replace the path in the help argument in "parse_args()" function with the actual path to your configuration file.
parser.add_argument(
    "config_file",
    help="C:\\path\\to\\your\\.yaml\\file")


#### Clone the repositor. You can modify application.yaml file or create your own. Make sure it follows the YAML format.
git clone <link to the repo>
cd <repo-folder>

Or download the files:
Save health-check.py and application.yaml in the same directory.

## Running the Program:
#### Run the program using the following command:
```bash
python health-check.py <path-to-your-configuration-file>
```
Example: (both health-check.py and application.yml are in the same directory in the example below)
```bash
python health-check.py application.yaml
```

#### To stop the program, press Ctrl+C.