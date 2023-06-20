import os
import sys
import czifile
import tifffile
from PIL import Image
from absl import app
import xmltodict
from dateutil import parser
from datetime import datetime
import csv

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to the import search path
sys.path.append(parent_dir)
# Now we can import bpconfig from LocalTools
from LocalTools import bpconfig

def main(argv):
  bpc_items = bpconfig.load('bpconfig_czi2tiff.csv', 'czi_file_name')
  print("Batch processing configuration items: ", bpc_items)
  possible_keywords = {' Pre', ' pre', ' Post', ' post'}
  fields = ['current_channel_name', 'output_file_name', 'width', 'height', 'start_time_including_fractional_seconds',
            'frame_interval','exposure_duration', 'processed_at', 'for_input']
  dict_of_frame_info = {}
  for bpc_item in bpc_items:
    actually_output_tiffs = int(bpc_item['actually_output_tiffs'])
    max_num_frames_to_process = int(bpc_item['max_num_frames_to_process'])
    input_czi_file_name = bpc_item['czi_file_name']
    tiff_file_name_format = bpc_item['tiff_file_name_format']
    if tiff_file_name_format == 0:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = False
        frame_number_at_end = False
    elif tiff_file_name_format == 1:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = True
        frame_number_at_end = False
    elif tiff_file_name_format == 2:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = False
        frame_number_at_end = False
    elif tiff_file_name_format == 3:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = True
        frame_number_at_end = False
    elif tiff_file_name_format == 4:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = False
        frame_number_at_end = True
    elif tiff_file_name_format == 5:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = True
        frame_number_at_end = True
    elif tiff_file_name_format == 6:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = False
        frame_number_at_end = True
    elif tiff_file_name_format == 7:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = True
        frame_number_at_end = True
    
    
    file_name_without_suffix = os.path.splitext(input_czi_file_name)[0]
    for k in possible_keywords:
        if k in file_name_without_suffix:
            output_folder_name = file_name_without_suffix.split(k)[0]
            print("CZI Processing for: ", file_name_without_suffix)
            break

    # Open the CZI file
    with czifile.CziFile(input_czi_file_name) as czi_file:
        # Get the dimensions of the CZI image
        #print("CZI Shape:", czi_file.shape)

        # Get the metadata XML object
        metadata_xml = czi_file.metadata()

        # Convert the XML to a dictionary
        metadata_dict = xmltodict.parse(metadata_xml)

        #print(metadata_dict['ImageDocument']['Metadata']['Experiment']['ExperimentBlocks']['AcquisitionBlock']['SubDimensionSetups']['TimeSeriesSetup']['Interval'])
        md_info = metadata_dict['ImageDocument']['Metadata']['Information']
        md_info_image = md_info['Image']

        data_and_time = md_info_image['AcquisitionDateAndTime']
        sizeX = md_info_image['SizeX']
        sizeY =  md_info_image['SizeY']
        num_channels = int(md_info_image['SizeC'])
        num_frames  = int(md_info_image['SizeT'])
        print("CZI Image Acquisition Started at: ", data_and_time)
        print("CZI Dimensions: ", "sizeX = ", sizeX, "; sizeY = ", sizeX, "; Number of Channels = ", num_channels, "; Number of Frames = ", num_frames)

        frame_interval = float(md_info['Image']['Dimensions']['T']['Positions']['Interval']['Increment'])
        if 'TimelineTracks' in md_info:
            md_tlt = md_info['TimelineTracks']['TimelineTrack']
            if 'TimelineElements' in md_tlt:
                md_tt = md_tlt['TimelineElements']['TimelineElement']
            else:
                md_tlt_0 = md_tlt[0]
                #print(md_tlt_0)
                md_tt = md_tlt_0['TimelineElements']['TimelineElement']
        else:
            md_tt = []
            md_T = md_info['Image']['Dimensions']['T']
            #print(md_info)#['Image'])#['Dimensions'])
            time_string = md_T['StartTime']
            timestamp_float = parser.parse(time_string).timestamp()
            for frame_idx in range(num_frames):
                md_tt.append({'@Id':frame_idx+1, 'Time':time_string, 'Duration': None})
                timestamp_float += frame_interval
                # Convert the timestamp float back to a datetime object
                timestamp_datetime = datetime.utcfromtimestamp(timestamp_float)
                # Convert the datetime object to a formatted time string with fractional seconds
                time_string = timestamp_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        #print(md_tt)
        #for m in md_tt:
        #    print(m['@Id'], m['Time'], m['Duration'])

        print(data_and_time)
        channels = md_info['Image']['Dimensions']['Channels']['Channel']
        for c in channels:
            if c['@Name'] == 'Phase':
                print("Intend to skip all frames for channel: ", c['@Name'])
            else:
                print("Intend to save all frames for channel: ", c['@Name'])
        
        if actually_output_tiffs:
            image_data = czi_file.asarray()
        if max_num_frames_to_process > num_frames:
            max_num_frames_to_process = num_frames
        
        if output_folder_name in dict_of_frame_info:
            frame_info = dict_of_frame_info[output_folder_name]
        else:
            frame_info = []
            dict_of_frame_info[output_folder_name] = frame_info
        #if False:
        # Iterate over each frame and each channel
        for channel_idx in range(num_channels):
            # Specify the output directory
            
            cn = channels[channel_idx]['@Name']
            if cn == 'Phase':
               continue
            print(f'Intended TIFF Path-Names for channel {cn}: ')
            
            output_dir = os.path.join('output', output_folder_name, cn)
            if actually_output_tiffs:
                # Create the output directory if it doesn't exist
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

            num_frames_processed = 0
            for m in md_tt: #range(num_frames):
                if num_frames_processed >= max_num_frames_to_process:
                    break

                num_frames_processed += 1
                # Read the channel data and extract the intended frame
                if actually_output_tiffs:
                    frame_data = image_data[int(m['@Id'])-1]
                    channel_data = frame_data[channel_idx]

                if include_full_date_time_string_in_tiff_file_name:
                    date_string = m['Time']
                    date_string = date_string.replace(":", "-")
                else:
                    time_value = parser.parse(m['Time'])
                    date_string = time_value.strftime("%Y-%m-%d--%H-%M-%S")
       
                tid = m['@Id']
                dur = m['Duration']
                if include_duration_in_tiff_file_name:
                    if frame_number_at_end:
                        output_file_name = f'{date_string}_D{dur}_T{tid}.tif'
                    else:
                        output_file_name = f'T{tid}_{date_string}_D{dur}.tif'
                else:
                    if frame_number_at_end:
                        output_file_name = f'{date_string}_T{tid}.tif'
                    else:
                        output_file_name = f'T{tid}_{date_string}.tif'

               
                
                # Convert the UTC time to a string
                utc_time_string =  datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                frame_info.append({'current_channel_name': cn,'output_file_name': output_file_name,
                                    'width': sizeX, 'height': sizeY, 'start_time_including_fractional_seconds': m['Time'],
                                    'frame_interval': frame_interval,
                                    'exposure_duration': dur, 'processed_at':utc_time_string,
                                    'for_input':file_name_without_suffix})

                output_file = os.path.join(output_dir, output_file_name)
                                           
                # Save the channel image as TIFF
                if actually_output_tiffs:
                    tifffile.imwrite(output_file, channel_data, imagej=True)
                else:
                    print(output_file)

  #print(dict_of_frame_info)
  for key, value in dict_of_frame_info.items():
    #print(key, value)      
    information_output_dir = os.path.join('output', key)
    if not os.path.exists(information_output_dir):
        os.makedirs(information_output_dir)
    csv_path = os.path.join(information_output_dir, f'czi2tiff_log.csv')
        
    with open(csv_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = fields)
            writer.writeheader()
            #writer = csv.writer(file)
            writer.writerows(frame_info)


if __name__ == "__main__":
    app.run(main)
