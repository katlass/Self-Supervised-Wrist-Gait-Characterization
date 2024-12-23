import skdh
import os

def load_and_configure_pipeline(input_file, output_file, test=False, window_days=False):
    """
    Configure the skdh pipeline for action classification with the necessary steps found in our first try at
    creating this baseline model. Allows for testing mode that uses less rows.
    
    Inputs:
    - input_file: Path to the input CSV file
    - output_file: Path to save the output results. Should standardize output name
    - test: T/F if you want to quickly test that this works
    - window_days: [Experimental] I do no think we need this part of the pipeline, might have to turn to True
    
    Returns:
    - Configured skdh pipeline object
    """
    if test:
        read_csv_kwargs = {'nrows': 5000, 'parse_dates': ['time'], 'na_filter': False}
        
    pipeline = skdh.Pipeline()
    
    pipeline.add(
        skdh.io.ReadCSV(
            time_col_name='time',
            column_names={'accel': ['accel_x', 'accel_y', 'accel_z']},
            trim=None,
            drop_duplicate_timestamps=True,
            fill_gaps=True,
            fill_value={'accel': [0.0, 1.0, 0.0]},
            raw_conversions={'accel': 9.81},
            read_csv_kwargs={'parse_dates': ['time'], 'na_filter': False},
        )
    )
    
    if window_days:
        pipeline.add(skdh.preprocessing.GetDayWindowIndices(bases=[0], periods=[24]))
    pipeline.add(skdh.preprocessing.CalibrateAccelerometer())
    pipeline.add(skdh.context.PredictGaitLumbarLgbm())
    pipeline.add(
        skdh.gait.GaitLumbar(),
        save_file=output_file
    )
    
    return pipeline

def check_input_output_paths(input_file, output_folder):
    """
    Validate the input file and output folder paths.
    
    Inputs:
    - input_file: Path to the input file
    - output_folder: Path to the folder where results will be saved, might want to standardize this as well
    
    Returns:
    - (output_file, error) where output_file is the complete path for the results and error is any path-related issues
    """
    if not os.path.exists(input_file):
        return None, f"Input file {input_file} does not exist."

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, "gait_results.csv")
    
    return output_file, None

def run_pipeline(pipeline, input_file, height):
    """
    Execute the action classification pipeline.
    
    Inputs:
    - pipeline: Configured skdh pipeline object
    - input_file: Path to the input file
    - height: Height of the individual for gait prediction, can get from meta file
    
    Returns:
    - Result of pipeline execution or error message if any
    """
    try:
        res = pipeline.run(file=input_file, height=height)
        return res, None
    except Exception as e:
        return None, f"Error during pipeline execution: {str(e)}"

def run_action_classification_pipeline(input_file, output_folder, height, test=False, window_days=False):
    """
    Main function to run the full action classification pipeline.
    
    Inputs:
    - input_file: Path to the input CSV file containing the accelerometer data and labeled/unlabeled lumbar data
    - output_folder: Path to the folder where the output will be saved, need standard names and possible error
                     catching to prevent two of these from being made (don't want to redo work)
    - height: Height of the individual for gait prediction, should use meta file to find actual height
    
    Returns:
    - Outputs the results to the specified output folder
    """
    # Step 1: Check the input/output paths exist
    output_file, path_error = check_input_output_paths(input_file, output_folder)
    if path_error:
        print(path_error)
        return
    
    # Step 2: Load and configure the skdh baseline model pipeline
    pipeline = load_and_configure_pipeline(input_file, output_file, test=test, window_days=window_days)
    
    # Step 3: Run the pipeline on this file
    result, pipeline_error = run_pipeline(pipeline, input_file, height)
    
    if pipeline_error:
        print(pipeline_error)
    else:
        print(f"Pipeline completed successfully! Results saved to {output_file}.")
