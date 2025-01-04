# Johnson & Johnson, Signal Processing and Machine Learning for Wrist Sensor Gait Analysis

## Specific Aims
- Apply open source lower back gait detection algorithms to partially labeled lower back data to validate best approach for generating labels for the whole dataset
- Use generated labels from lower back model to train a custom DCNN to make gait detection predictions on unsupervised wrist-worn sensor data
- Based on this self-supervised learning approach, use the data from predicted walking bouts to characterize subjects’ gait focusing on walking speed


## Accomplishments

- Built state-of-the-art DCNNs on terabytes of data with transfer learning, oversampling, and custom loss functions for gait classification

- Self-supervised wrist labels derived from lumbar sensors with signal preprocessing, dynamic thresholding and peak detection

- Designed an end-to-end pipeline for gait classification and speed prediction, achieving 0.93 F1 and 0.03 RMSE across participants <br>

![Workflow](https://github.com/katlass/Self-Supervised-Wrist-Gait-Characterization/blob/main/Visualizations/workflow_figure.png)
 <br>

## Repository Directory Overview
- Wrist: Contains scripts for mapping lower-back model labels to wrist data and performing activity classification and gait speed prediction. The script for final wrist activity classification is stored in SSL_Wrist-Based_Activity_Classification.ipynb, while the script for final walking speed predictions is stored in gait_speed_OLS.ipynb. There are also several files in that directory that show the model development of the DCNN including different loss functions and ways to address class imbalance.

- Lower Back: Tracks key scripts for processing sensor data from the lower back and extracting walking bouts and gait parameters. The script for final lumbar modeling is stored in mobgap_lowerback_pipeline.ipynb.

- Visualizations: Stores scripts for exploratory data analysis, focusing on visualizing signal data and results. Includes a Python visualization application.

- full_pipeline_public.ipynb: A comprehensive notebook compiling all lower-back and wrist data processing steps, as well as final models, into a single pipeline

## Results

![Results](https://github.com/katlass/Self-Supervised-Wrist-Gait-Characterization/blob/main/Visualizations/result_metrics.png)

![OLS Speed](https://github.com/katlass/Self-Supervised-Wrist-Gait-Characterization/blob/main/Visualizations/gait_speed_visual.png)
