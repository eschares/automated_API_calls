# automated_API_calls
 
Run API calls in three databases and finds the number of Iowa State University authored papers published in 2022 and 2023:

- Web of Science
- Dimensions
- OpenAlex

Records these number in two .csv files.

Uses a .bat file to runs each day at 9:05am, assuming computer is powered on and plugged in to power.

### To run for yourself, change:
- line 26 to change to your institution and include your own email address for OpenAlex's [polite API pool](https://docs.openalex.org/api#the-polite-pool)
- line 45 to assign your own Dimensions API key
- line 64 to assign your own Web of Science API Key, apply at https://developer.clarivate.com/

![graph](https://github.com/eschares/automated_API_calls/blob/main/ISU_2022_3databases_comparison.png)
