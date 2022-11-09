# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoreferencerDialog
                                 A QGIS plugin
 This plugin georeference the image
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-11-09
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Deepak Parajuli
        email                : deepak.parajuli002@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from osgeo import gdal
from osgeo import osr
import cv2

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geo_ref_dialog_base.ui'))


class GeoreferencerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GeoreferencerDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.calculateOutput.clicked.connect(self.calculateOutputClicked)

    #create a function which takes the link of the 2 images and add them using opencv
    def calculateOutputClicked(self):
        #get the link of the 2 images
        image1 = self.inputLink.toPlainText()
        image2 = self.outputLink.toPlainText()
        output = self.outputLink_2.toPlainText()

        #take all the images from image1 directory and store them in a list
        #image1List = os.listdir(image1)
        #print(image1List)
        input_files = [geotif[:-4] for geotif in os.listdir(image1) if geotif[-4:] == '.png']
        image_files = [png[:-4] for png in os.listdir(image2) if png[-4:] == '.png']
        output_files = [png[:-4] for png in os.listdir(output) if png[-4:] == '.png']
        missing_pngs_list = [geotif for geotif in input_files if geotif not in output]
        for i, img in enumerate(missing_pngs_list):
            geotiff_image = os.path.join(image1, img + '.png')
            predict_image = os.path.join(image2, img + '.png')
            output_path = os.path.join(output, img + '.png')
            raster_src = gdal.Open(geotiff_image, gdal.GA_ReadOnly)
            # coordinates of upper left corner and resolution
            ulx, xres, xskew, uly, yskew, yres = raster_src.GetGeoTransform()
            # coordinates of lower right corner
            lrx = ulx + (raster_src.RasterXSize * xres)
            lry = uly + (raster_src.RasterYSize * yres)
            #image_bbox = shapely.geometry.box(ulx, lry, lrx, uly)
            bbox_gen = [uly, lrx, lry, ulx]
            image_gen = cv2.imread(predict_image, 1)
            #image = cv2.imwrite(output_path, image_read)
            # print(image)
            print(image_gen)
            save_as_geotif(bbox_gen, image_gen, output_path)
        return

def save_as_geotif(bbox, image, save_path):
    """
    Function to save a jpg or png as GEOTIFF
    Inputs
    ----------
    bbox : list
        bounding box coordinates of image:
        [latitude_min, longitude_min, latitude_max, longitude_max]
    image : numpy array
        RGB image as a numpy array with shape [x_pixels, y_pixels, 3]
    save_path : string
        string that determines the path including filename to save the GEOTIFF
        filename should end with ".tif"
    Outputs
    ----------
    None - function saves GEOTIFF to path
    """
    # set geotransform
    nx = image.shape[0]
    ny = image.shape[1]
    

    xmin, ymin, xmax, ymax = [bbox[1], bbox[0], bbox[3], bbox[2]]
    xres = (xmax - xmin) / float(nx)
    yres = (ymax - ymin) / float(ny)

    geotransform = (xmin, xres, 0, ymax, 0, -yres)

    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(
        save_path, ny, nx, 3, gdal.GDT_Byte)
    #print(dst_ds)

    dst_ds.SetGeoTransform(geotransform)  # specify coords
    srs = osr.SpatialReference()  # establish encoding
    srs.ImportFromEPSG(4326)  #
    dst_ds.SetProjection(srs.ExportToWkt())  # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(
        image[:, :, 2])  # write r-band to the raster
    dst_ds.GetRasterBand(2).WriteArray(
        image[:, :, 1])  # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(
        image[:, :, 0])  # write b-band to the raster
    dst_ds.FlushCache()  # write to disk
    

    return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GeoreferencerDialog()
    ui.show()
    sys.exit(app.exec_())



 
