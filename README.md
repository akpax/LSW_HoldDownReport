# LSW_HoldDownReport


## Project Summary


### Functionality
This tool automates the post-processing of hold down forces from the Light Shear Wall (LSW) application, producing a comprehensive .xlsx report file. It processes shearwall input (.txt) and force output files (.pdf) from LSW to determine the maximum tension force each holdown experiences.


### Behind the Scenes
Internally, the tool parses the input files and converts them into dataframes for analysis. It utilizes the shearwall location data to identify walls that are stacked on top of each other. Given the LSW's limited snapping capabilities, which often result in slightly misaligned shear wall locations, the tool employs the DBSCAN clustering algorithm. This algorithm clusters walls based on their locations, generating unique location keys for each wall. These keys are then left joined with the shear wall output data to accurately identify stacked walls. Subsequently, the tool calculates the difference in tension forces between adjacent floors of each wall, identifying the maximum delta force for each wall's left and right holdowns across various load cases. The final output is an .xlsx report that includes a summary of the maximum force for each type of holdown, the maximum left and right holdown forces for each wall, and intermediate output files. The report is formatted with the MAR logo on the first two sheets, tailored for printing.


## Using the Executable
To download the executable, visit[ https://github.com/akpax/LSW_HoldDownReport/tags](https://github.com/akpax/LSW_HoldDownReport/tags) and click on the most recent release. In the assets section, select the LSW_HoldownReport_windows.exe file for download and place it in your desired directory. (This will also be the directory where the output folder is created.) Note: the .exe file is standalone, and downloading the source code is not necessary to run this application.


When the user launches the executable, the File Selector GUI appears, prompting for input and output file selection. (Refer to the next section for the correct file format).

<img width="735" alt="Screenshot 2024-01-05 at 6 34 05 PM" src="https://github.com/akpax/LSW_HoldDownReport/assets/78048703/4e0829a2-7047-4e8d-8f9b-0cc4dd26aa55">


After file selection, the paths should appear in italics. Please confirm that the files have been correctly selected.

![](https://lh7-us.googleusercontent.com/lez3lC5ynUYPiByIsbw5DsGHFGPS_nkEynqVVB-MLGkFiIadDai8rSMWXW8XDCrQLhcHuzO1vNS8YobzE9nHLC04OvK15T_k2okom2qk_4dZ9sWufV-4bzZEsYVjtmX8TXx5UTeqPmuoOMgLRls0e1E)



Upon clicking submit, the backend parses the files and performs the logic to identify the governing delta hold down forces. If successful, a success window will appear, and the output report (.xlsx) will be located in the “LSW_HoldownReport” folder in the current working directory.

![](https://lh7-us.googleusercontent.com/wff7HXbiVFmjXBSzYndC0f0-ySQ7d26j_ZtSL82wuvLLV5InGhEbrRdPzQMNzfOk6hTo2lrPKE_A4AP78qUjoSFOTIM5MyyST2M4UqmicBF2JKQfSpQxbCAX5SAAfLj5hWCzAFa2m-FjQ2umjCPU6TU)



If this message does not appear, the analysis has likely failed. The most common reasons are incorrect data format (refer to the next section) or an issue parsing the output pdf. Please double check the data files per  the “correctly Formatting the LSW Files” section. If this does not produce an output, please create an “issue” on GitHub detailing the problem you are experiencing.

## Correctly Formatting the LSW files
The LSW shearwall input and force output files must follow a specific format for the application to process them correctly. This section covers the proper formatting for these files:

### Shearwall Input File
In LSW, navigate to components, click on tables, and in the dropdown, change the selection to shearwalls.

![](https://lh7-us.googleusercontent.com/zvuQ7H8j3K4ccY7fqeOSUHyFwQBQjk9BvnyIDtMO4riBbgeFVRhAKD3oECf8RGoYi2HS-bPHBvzS8FvNBK_LYh2FcyXUQUkNzw69N9VaLYoxG0y-EDTAlM19N2JfYe5hmO-UpM5ERNXzI4EjiC9nxBw)



The application expects the following columns in this order:

``` [Handle, Diaphragm, Name, Shearwall Type, Left Location, Right Location, Left Boundary Type, Right Boundary Type] ``` Note: Diaphragm must have a numerical value in it; the tool will extract digits from the diaphragm entry and use the extracted digit to determine where each wall is vertically located.

To adjust displayed columns, right-click within the table and select settings in the dialogue box.

![](https://lh7-us.googleusercontent.com/5cMvXOjZvgg4hiqyhBzPjtwjpLkJGXNO4TAV7KHdX7t9T3es1Kthoud38Z7FQ2CwP6nmfO4QjCHzCoZQ_FyTqJb-iranryDTK_NM1kVPL0Q3ERxq-PUAbdgJO49QZcIOG1HAKn13gvkZl6owr0h6tAc)



Column visibility can be adjusted using the lightbulbs in the settings window:![img](https://lh7-us.googleusercontent.com/-bXE-Zipi7tEqkmdDfO_rv5wvPIVnS7bQt64cjZ15-3LC46gC1H31zYXNkY6hmgLhVnwlQx6XIBROyx1LvKDiRyQR9speubl1TaJ6T0JqfM8ho1tAIk00b83hnkdlTfxKLLpo1KrnxwyX8yn8KYE4eE)

After including the correct columns, highlight all the data and paste it into a .txt file. This file will be input into the application.

### Shear Wall Force output

The other required file is the shearwall force output file (.pdf).

First, the user needs to run the model by navigating to the buildings tab, clicking the red check, and then clicking the green triangle (located in the same area as the red check).

![](https://lh7-us.googleusercontent.com/xCT_puQBCXbDf6_ZWzFJE1aqVRhJbI3CHR496RUC_O5dCBgFb6UOcjCFlYg3YsdMuNi7gGcQPpOL41tKyMsAnrel6EhyHDb_m8cATrYbiitG_mMojZsJaGLGalPLdP_b6mCCUI8-bUDYmJGgxyjhHwk)



To view the results, go to components, click view results, and change the drop-down selection to shearwalls. Then, adjust the table settings as in the previous section to display only the following columns: 
``` [Handle, Name, Lower Diaphragm, Shearwall Type, Left Boundary Type, Left Tension, Right Boundary Type, Right Tension] ```

![](https://lh7-us.googleusercontent.com/jArAyvs1sgsraLSI34k3f7rDtoszPREqeh6uKnlMyMUNlPq_xOf94ZDM-LQXVVrq1sZsDky1czAQozQZYxATDrqOuSMnMH5ule9Qf1TvTA3rFXySn7eWlB6Z0uqLC9V-_s-N3u94HG-dyqJQQ1ZC0As)



To print to pdf, print and go to options:

![](https://lh7-us.googleusercontent.com/wHzI6dSpOGeNenRgHeXPEOh_ym2_tXjiQh789FcKq3CrNiXqJ6sl_F8yerSQ1fmISAQXWF4B4iqpKolFPuNMfjL5Q_HaLGC4yR5K9v67J9xhk8jmKqwMigAmkfW1sMxtick-z57MBOSa1CEx2Xmt6M8)



In Options, deselect everything except “Shearwalls” under Results Tables. Ensure “envelope” is unselected and click on all load cases.

![](https://lh7-us.googleusercontent.com/9s_hHAEoH22j_WtWXMtVweQ-XFJftJFBZHPyCoPYSf3WLC2R8VPN7Gb02Nu4WEu8zB-aBvS01tZU53T6wmw9Rdwvj7DBFdwGb7YtL4lrPFxyfk2EQc0-R2bHO6O6_OEjd6L8Z0Ey3_FDk_SaQTSCLOc)

The output forces PDF is now prepared for the application.
