import argparse, os
import exiftool
import csv

parser = argparse.ArgumentParser(description="This script requires a path to Image folder")
parser.add_argument("-p", "--path", help="The directory of Image files", type=str)
valid_images = [".jpg", ".jpeg", ".gif",".png",".tga"]
args = parser.parse_args()


def check_path_argument():
    if args.path is not None:
        return validate_path(args.path)
    else:
        print("You forgot to add the path argument")


def validate_path(path):
    if os.path.isdir(path):
        return read_image_files(path)
    else:
        raise NotADirectoryError(path)


def read_image_files(path):
    images = []
 
    for file in os.listdir(path):
        ext = os.path.splitext(file)[1]
        if (ext.lower() not in valid_images):
            continue
        images.append(os.path.join(path, file))
    
    extract_exif(images, path)

def extract_exif(images, path):
    #Make a folder (or override) for csv files
    os.makedirs(path+"/Exif_Data", exist_ok=True);

    #Get the exif data from all images
    with exiftool.ExifToolHelper() as et:
        flag = 0
        metadata = et.get_metadata(images)
        for data in metadata:
            #For each json object that has the data in,
            #save it to the path with the image name
            save_to_csv(data, images[flag], path)
            flag+=1
    print("Process completed")

def save_to_csv(data, image:str, path):
    #Remove the path from the name
    imgName = image[len(path): len(image)]

    #Split the file extension from the name
    if os.path.splitext(imgName)[1] in valid_images:
        imgName = os.path.splitext(imgName)[0]
    #Open a new csv file and use csvwriter to append data
    with open("./Images/Exif_Data"+imgName+".csv", "w") as file:
        writer = csv.writer(file)
        for key in data:
            writer.writerow([key, data[key]])

def main():
    check_path_argument()


if __name__ == "__main__": 
    main()
