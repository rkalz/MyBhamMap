To run this program, IntelliJ PyCharm is required.

Install the dependencies
* Extract the contents of “mybhammap.zip” and open PyCharm. Select File -> Open, and select the “mybhammap” folder.
* Go to File -> Settings -> Project: mybhammap -> Project Interpreter.
* Select the gear icon -> Add -> OK -> OK.
* At the bottom, select “Terminal” -> type “pip install -r requirements.txt”
* If you get a “ModuleNotFound” error, type “pip install six” and then retry the previous command.

Configure run parameters
* Now go to “Add Configuration…” -> select the ‘+’ icon -> Python.
* In script path, select the folder icon, select “mybhammap\local_calculations\calculate_path.py”.
* In environment variables, select the folder icon, select the ‘+’ icon.
* Set the name to GOOGLE_API_KEY and the value to “REDACTED (SEE REPORT)” (excluding quotes).

Run the program
* Go to the dropdown box in the top right, select “Unnamed”, and press the green “Run” button.
* At the end, it should generate a base64 string. Copy the "entire" base64 string.
* Go to https://codebeautify.org/base64-to-image-converter and paste in the base64 string
* The resulting image being the shortest path from UAB Campbell Hall to the McWane Center.