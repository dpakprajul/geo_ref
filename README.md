# A QGIS plugin to georeference the image with the same image id.
### part of my thesis, where there was a predicted image from a deep learning model. The predicted image is non-georeferenced, and needs to be georeferenced to carry out further post processing. Hence this tool could help to input the original data with georeferenced images and predicted unreferenced image to output the referenced output image.

### Need to change the UI of the dialog box

#### Georeferenced Image should be like: D:\RID-master\RID-master\data\gutter_image_trash (input which is the folder of georeferenced image)
#### Unreferenced Image should be like: D:\RID-master\RID-master\data\gutter_image_trash (input which is the folder of unreferenced predicted image)
#### The last one is the Output Link:  D:\output (this is an output where the Unreferenced Image would be georeferenced and stored in a folder)


![image](https://user-images.githubusercontent.com/38970123/200932378-eebd8eaa-41b9-4e56-a714-760fd887b1bc.png)


#### Example of input prediction image (unreferenced)
<img src="https://user-images.githubusercontent.com/38970123/200933563-e669fbee-b4d3-41a5-8a0c-2d34f1c82418.PNG" width="400" height="200">


#### Example of output image (georeferenced image)
<img src="https://user-images.githubusercontent.com/38970123/200932999-b059b8ca-8692-48f3-bd6e-0e725343bc95.png" width="400" height="200">

#### This image has same grayscale and could be visualized using softwares like ImageJ

## License
This Plugin is licensed under the [GPL](http://docs.geoserver.org/latest/en/user/introduction/license.html). See also LICENSE file in this repo.

### TO DO
#### Need to make a drop down where user can choose the input file format. For example: png, tif, jpeg
