# User Study

This Unity application was developed for the user study for predicting body movements. The participant is virtually placed via OptiTracks motion capturing system and an HTC Vive as head mounted device in a scene similar to the real surroundings where the study takes place. Via external adjustments the motion captured body movements are getting intercepted, changed and projected on the participants virtual model based on different prediction values.

The application can be subdivided into three main purposes:

### Body Visualization

At start the participant is located without any configuration in a replica of the studio. The different body movement predictions and their effects can be experienced while moving freely or by predefined tasks.

### Evaluating Self-Perception

After some time where the participant could adjust itself to the altered movement predictions a questionnaire can be enabled externally for evaluating made experiences. 

The questionnaire is segmented into two contentual parts with the first part being questions from the IPQ questionnaire and and secondly questions regarding limb ownership. The questions from each segment are randomly sorted each time the questionnaire is getting started while the segment order remains static.

The questionnaire can be started by "touching" the virtually placed start button. After selection of one of the five offered answer options a forward button is displayed until no questions remain where the questionnaire is disabled again automatically.

### Performance Task

For this task the two whiteboards have to be enabled in the scene externally while placing the real world equivalents at the predefined same positions. While the participant touches virtually and in reality each whiteboard in alternation for a specific time the repetitions are getting counted and recorded by the study master.

# Configuration and Usage Instructions

### Configuration

For being able to project the body movements on the model from the motion capturing system, OptiTracks Unity plugin is required ([Link](https://optitrack.com/downloads/plugins.html#unity-plugin)). 

It should be configured on the "Client - OptiTrack" game object with the **ServerAddress** being the IP address of the streaming OptiTrack host and on the "Avatar" game object with **Skeleton Asset Name** the skeleton id defined inside the OptiTrack client.

### Default Scene Configuration

The starting scene configuration should be with
* the **questionnaire** object being **disabled**,
* the **whiteboards outside** the marked area **enabled** and
* the **whiteboards inside** the marked area **disabled**. 

### Prior Study

Before the study can be conducted and the scene started, the **personId** has to be specified on the **Questionnaire** object for being able to associate results to a participant.

### Mid-Study

During the study 
* the **questionnaire** object has to be **enabled** when needed (being disabled again automatically) and
* the **whiteboard** objects switched in its availibility status for the performance task.

# Results

While the performance task results are recorded by the study master solely, the answers from the evaluation questionnaire are stored inside a CSV file (*C:\Users\LocalAdmin\Documents\Projekte\VR-Prediction\questionnaire.csv*).

For each answered questions a new line like the following is appended to the CSV: `5,6,4,20190823144016` and can be read as `[PARTICIPANT_ID],[QUESTION_ID],[ANSWER_OPTION_ID],[DATETIME_STAMP]`.

