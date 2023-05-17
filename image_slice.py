import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

data_dir = "neurocon"

#output folder
output_dir = "10_sliced_mri_dataset"
# os.makedirs(output_dir,  exist_ok=True)
os.makedirs(output_dir+'/control', exist_ok=True)
os.makedirs(output_dir+'/parkinson', exist_ok=True)



folders = next(os.walk(data_dir))[1]

control_folders = []
patient_folders = []

for folder in folders:
    folder_name = os.path.basename(folder)
    if 'control' in folder_name:
        control_folders.append(folder)
    elif 'patient' in folder_name:
        patient_folders.append(folder)

print("\nControl Folders:"+str(len(control_folders)))
print("Patient Folders:"+str(len(patient_folders))+"\n")

num_slices = 10

for folder in control_folders:

    nii = os.path.join(data_dir,folder)
    nii_folder=os.path.join(nii,'anat')

    for filename in os.listdir(nii_folder):

        if filename.endswith(".nii.gz"):
            
            img = nib.load(os.path.join(nii_folder, filename))
            img_data = img.get_fdata()

            output_folder_name = os.path.splitext(os.path.splitext(filename)[0])[0]
            output_path = os.path.join(output_dir,'control',output_folder_name)
            os.makedirs(output_path, exist_ok=True)

            mid_slice = img_data.shape[2] // 2

            for i in range(-(num_slices//2),(num_slices//2)if (num_slices%2==0) else (num_slices//2)+1):

                slice_data = np.squeeze(img_data[:, :, mid_slice+i])
                slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data)) * 255 #normalize
                slice_data = slice_data.astype(np.uint8)

                output_filename=os.path.join(output_path,'mid_'+str(i+(num_slices//2)+1)+'_slice.png')
                plt.imsave(output_filename, slice_data, cmap="gray")



for folder in patient_folders:

    nii = os.path.join(data_dir,folder)
    nii_folder=os.path.join(nii,'anat')
    
    for filename in os.listdir(nii_folder):
        
        if filename.endswith(".nii.gz"):
            
            img = nib.load(os.path.join(nii_folder, filename))
            img_data = img.get_fdata()

            output_folder_name = os.path.splitext(os.path.splitext(filename)[0])[0]
            output_path = os.path.join(output_dir,'parkinson',output_folder_name)
            os.makedirs(output_path, exist_ok=True)

            mid_slice = img_data.shape[2] // 2

            for i in range(-(num_slices//2),(num_slices//2)if (num_slices%2==0) else (num_slices//2)+1):
                
                slice_data = np.squeeze(img_data[:, :, mid_slice+i])
                slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data)) * 255 #normalize
                slice_data = slice_data.astype(np.uint8)
                
                output_filename=os.path.join(output_path,'mid_'+str(i+(num_slices//2)+1)+'_slice.png')
                plt.imsave(output_filename, slice_data, cmap="gray")

print("Conversion complete. Patient images are saved in:", output_dir)
