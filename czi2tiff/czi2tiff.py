import os
import czifile
import tifffile
from PIL import Image
from absl import app
import xmltodict
from dateutil import parser
from datetime import datetime
import bpconfig
def main(argv):
  bpc_items = bpconfig.load('bpconfig_czi2tiff.csv', 'czi_file_name')
  print("Batch processing configuration items: ", bpc_items)
  possible_keywords = {' Pre', ' pre', ' Post', ' post'}
  for bpc_item in bpc_items:
    actually_output_tiffs = int(bpc_item['actually_output_tiffs'])
    max_num_frames_to_process = int(bpc_item['max_num_frames_to_process'])
    input_czi_file_name = bpc_item['czi_file_name']
    tiff_file_name_format = bpc_item['tiff_file_name_format']
    if tiff_file_name_format == 0:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = False
    elif tiff_file_name_format == 1:
        include_full_date_time_string_in_tiff_file_name = False
        include_duration_in_tiff_file_name = True
    elif tiff_file_name_format == 2:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = False
    else:
        include_full_date_time_string_in_tiff_file_name = True
        include_duration_in_tiff_file_name = True
    file_name_without_suffix = os.path.splitext(input_czi_file_name)[0]
    for k in possible_keywords:
        if k in file_name_without_suffix:
            output_folder_name = file_name_without_suffix.split(k)[0]
            print("CZI Processing for: ", file_name_without_suffix)  # Output: example
            break
    
    # Open the CZI file
    with czifile.CziFile(input_czi_file_name) as czi_file:
        # Get the dimensions of the CZI image
        #print("CZI Shape:", czi_file.shape)

        # Get the metadata XML object
        metadata_xml = czi_file.metadata()

        # Convert the XML to a dictionary
        metadata_dict = xmltodict.parse(metadata_xml)

        # Retrieve the order of the dimensions
        md = metadata_dict['ImageDocument']['Metadata']['Information']['TimelineTracks']['TimelineTrack']['TimelineElements']['TimelineElement']
        #print(md)
        #for m in md:
            #[]'TimelineElement']
            #keys = list(md.keys())
            #print(keys)
            #print(m['@Id'], m['Time'], m['Duration'])

        data_and_time = metadata_dict['ImageDocument']['Metadata']['Information']['Image']['AcquisitionDateAndTime']

        channels = metadata_dict['ImageDocument']['Metadata']['Information']['Image']['Dimensions']['Channels']['Channel']
        for c in channels:
            if c['@Name'] == 'Phase':
                print("Intend to skip all frames for channel: ", c['@Name'])
            else:
                print("Intend to save all frames for channel: ", c['@Name'])
        

        sizeX = metadata_dict['ImageDocument']['Metadata']['Information']['Image']['SizeX']
        sizeY = metadata_dict['ImageDocument']['Metadata']['Information']['Image']['SizeY']
        num_channels = int(metadata_dict['ImageDocument']['Metadata']['Information']['Image']['SizeC'])
        num_frames  = int(metadata_dict['ImageDocument']['Metadata']['Information']['Image']['SizeT'])
        print("CZI Image Acquisition Started at: ", data_and_time)
        print("CZI Dimensions: ", "sizeX = ", sizeX, "; sizeY = ", sizeX, "; Number of Channels = ", num_channels, "; Number of Frames = ", num_frames)
        if actually_output_tiffs:
            image_data = czi_file.asarray()
        if max_num_frames_to_process > num_frames:
            max_num_frames_to_process = num_frames

        #if False:
        # Iterate over each frame and each channel
        for channel_idx in range(num_channels):
            # Specify the output directory
            cn = channels[channel_idx]['@Name']
            if cn == 'Phase':
               continue
            output_dir = os.path.join('output', output_folder_name, cn)
            print(f'Intended TIFF Path-Names for channel {cn}: ')
                  
            if actually_output_tiffs:
                # Create the output directory if it doesn't exist
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

            num_frames_processed = 0
            for m in md: #range(num_frames):
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
                    output_file = os.path.join(output_dir, f'T{tid}_{date_string}_D{dur}.tif')
                else:
                    output_file = os.path.join(output_dir, f'T{tid}_{date_string}.tif')
                                           
                # Save the channel image as TIFF
                if actually_output_tiffs:
                    tifffile.imwrite(output_file, channel_data, imagej=True)
                else:
                    print(output_file)


if __name__ == "__main__":
    app.run(main)
