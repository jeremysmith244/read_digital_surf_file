import struct
import numpy as np
import matplotlib.pyplot as plt


class surface():

    '''Class to read Digital Surf .sur files,
       typical of scanners and certain microscopes
       
       Based on:
       https://www.mathworks.com/matlabcentral/fileexchange/61731-read-surf-file

       Attributes:

       signature: text of filetype
       format: byte format, 16 or 32 bit into
       objNum: object number
       version: file version
       objType: type of object
       objname: object name
       operatorname: operator name
       materialCode: material type
       acquisitionType: type of acquisition
       rangeType: range type
       specialPoints: any special points
       absoluteHeights: absolute heights
       gaugeResolution: resolution of the gauge
       sizeOfPoints: size of the points
       zMin: defines minimum z in matrix
       zMax: defines maximum z in matrix
       xPoints: size of matrix in x
       yPoints: size of matrix in y
       totalPoints: total number of data points
       xSpacing: spacing in x dimension
       ySpacing: spacing in y dimension
       zSpacing: spacing in z dimension
       xName: x axis name
       yName: y axis name
       zName: z axis name
       xStepUnit: units in x
       yStepUnit: units in y
       zStepUnit: units in z
       xLengthUnit: length of x
       yLengthUnit: length of y
       zLengthUnit: length of z
       xUnitRatio: scaling in x
       yUnitRatio: scaling in y
       zUnitRatio: scaling in z
       imprint: binary imprinted or not
       inverted: binary, inveted or not
       levelled: binary, inverted or not
       startSeconds:
       startMintues:
       startHours:
       startDays:
       startMonths:
       startYears:
       startWeekDay:
       MeasurementDuration:
       commentSize:
       privateSize:
       clientZone:
       xOffset: offset in x to 0, 0 corner of image
       yOffset:offset in y to 0, 0 of image
       zOffset: offset in z to image plane
       tempSpacing:
       tempOffset:
       tempStepUnit:
       tempStepUnit:
       tempAxisName:
       tempAxisName:
       comment:
       private:
       points: data, in 1D array, transformed into floats
       pointsAligned: points reshaped into image
       xAxis: x for matrix points
       yAxis: y for matrix points
       '''

    # https://docs.python.org/3/library/struct.html
    # https://www.mathworks.com/help/matlab/ref/fread.html

    def __init__(self, path):

        # read in all the header stuff
        with open(path, 'rb') as f:

            self.signature = ''
            for i in range(12):
                # these are just single byte characters, read one by one
                self.signature += f.read(1).decode('utf8')

            # any read like this is a two byte 'short' int
            self.format = int.from_bytes(f.read(2), byteorder='little')
            self.objNum = int.from_bytes(f.read(2), byteorder='little')
            self.version = int.from_bytes(f.read(2), byteorder='little')
            self.objType = int.from_bytes(f.read(2), byteorder='little')

            self.objectname = ''
            for i in range(30):
                self.objectname += f.read(1).decode('utf8')

            self.operatorname = ''
            for i in range(30):
                self.operatorname += f.read(1).decode('utf8')

            self.materialCode = int.from_bytes(f.read(2), byteorder='little')
            self.acquisitionType = int.from_bytes(f.read(2), byteorder='little')
            self.rangeType = int.from_bytes(f.read(2), byteorder='little')
            self.specialPoints = int.from_bytes(f.read(2), byteorder='little')
            self.absoluteHeights = int.from_bytes(f.read(2), byteorder='little')

            # any read like this is a 4 byte floating point number
            self.gaugeResolution = round(struct.unpack('<f', f.read(4))[0], 4)

            # some junk
            f.read(4)

            # important things start here, this defines the structure of the
            # data (i.e. size of the image matrix along with the resolution in
            # the x, y and z direction for building the image

            self.sizeOfPoints = int.from_bytes(f.read(2), byteorder='little')

            # any read like this is a 4 byte standard binary int
            self.zMin = struct.unpack('<i', f.read(4))[0]
            self.zMax = struct.unpack('<i', f.read(4))[0]
            self.xPoints = struct.unpack('<i', f.read(4))[0]
            self.yPoints = struct.unpack('<i', f.read(4))[0]
            self.totalPoints = struct.unpack('<i', f.read(4))[0]
            self.xSpacing = struct.unpack('<f', f.read(4))[0]
            self.ySpacing = struct.unpack('<f', f.read(4))[0]
            self.zSpacing = struct.unpack('<f', f.read(4))[0]

            # read in some labels, units and stuff
            self.xName = ''
            for i in range(16):
                self.xName += f.read(1).decode('utf8')
            self.xName = self.xName.split()[0]

            self.yName = ''
            for i in range(16):
                self.yName += f.read(1).decode('utf8')
            self.yName = self.yName.split()[0]

            self.zName = ''
            for i in range(16):
                self.zName += f.read(1).decode('utf8')
            self.zName = self.zName.split()[0]

            self.xStepUnit = ''
            for i in range(16):
                self.xStepUnit += f.read(1).decode('utf8')
            self.xStepUnit = self.xStepUnit.split()[0]

            self.yStepUnit = ''
            for i in range(16):
                self.yStepUnit += f.read(1).decode('utf8')
            self.yStepUnit = self.yStepUnit.split()[0]

            self.zStepUnit = ''
            for i in range(16):
                self.zStepUnit += f.read(1).decode('utf8')
            self.zStepUnit = self.zStepUnit.split()[0]

            self.xLengthUnit = ''
            for i in range(16):
                self.xLengthUnit += f.read(1).decode('utf8')
            self.xLengthUnit = self.xLengthUnit.split()[0]

            self.yLengthUnit = ''
            for i in range(16):
                self.yLengthUnit += f.read(1).decode('utf8')
            self.yLengthUnit = self.yLengthUnit.split()[0]

            self.zLengthUnit = ''
            for i in range(16):
                self.zLengthUnit += f.read(1).decode('utf8')
            self.zLengthUnit = self.zLengthUnit.split()[0]

            self.xUnitRatio = round(struct.unpack('<f', f.read(4))[0], 4)
            self.yUnitRatio = round(struct.unpack('<f', f.read(4))[0], 4)
            self.zUnitRatio = round(struct.unpack('<f', f.read(4))[0], 4)

            # this ends the section of useful attributes
            self.imprint = int.from_bytes(f.read(2), byteorder='little')
            self.inverted = int.from_bytes(f.read(2), byteorder='little')
            self.levelled = int.from_bytes(f.read(2), byteorder='little')

            # some more junk
            f.read(12)

            # timestamps, not used for our data

            self.startSeconds = int.from_bytes(f.read(2), byteorder='little')
            self.startMintues = int.from_bytes(f.read(2), byteorder='little')
            self.startHours = int.from_bytes(f.read(2), byteorder='little')
            self.startDays = int.from_bytes(f.read(2), byteorder='little')
            self.startMonths = int.from_bytes(f.read(2), byteorder='little')
            self.startYears = int.from_bytes(f.read(2), byteorder='little')
            self.startWeekDay = int.from_bytes(f.read(2), byteorder='little')
            self.MeasurementDuration = round(struct.unpack('<f', f.read(4))[0], 4)

            # even more junk
            f.read(10)

            self.commentSize = int.from_bytes(f.read(2), byteorder='little')
            self.privateSize = int.from_bytes(f.read(2), byteorder='little')

            self.clientZone = ''
            for i in range(128):
                self.clientZone += f.read(1).decode('utf8')

            # offsets in spatial dimensions
            self.xOffset = round(struct.unpack('<f', f.read(4))[0], 4)
            self.yOffset = round(struct.unpack('<f', f.read(4))[0], 4)
            self.zOffset = round(struct.unpack('<f', f.read(4))[0], 4)

            # temperature offsets
            self.tempSpacing = round(struct.unpack('<f', f.read(4))[0], 4)
            self.tempOffset = round(struct.unpack('<f', f.read(4))[0], 4)

            self.tempStepUnit = ''
            for i in range(13):
                self.tempStepUnit += f.read(1).decode('utf8')

            self.tempAxisName = ''
            for i in range(13):
                self.tempAxisName += f.read(1).decode('utf8')

            self.comment = ''
            for i in range(self.commentSize):
                self.comment += f.read(1).decode('utf8')

            if self.privateSize != 0:
                self.private = ''
                for i in range(self.privateSize):
                    self.private += f.read(1).decode('utf8')

            # read in all the data as a big binary vector
            if self.sizeOfPoints == 16:
                self.points = np.fromfile(f, dtype=np.dtype(np.int16),
                                          count=self.totalPoints)
            elif self.sizeOfPoints == 32:
                self.points = np.fromfile(f, dtype=np.dtype(np.int32),
                                          count=self.totalPoints)
            else:
                print('something is wrong with your file,\
                       or the this code is not valid for your file')

            # tranform points into floats with correct as numpy matrix
            self.points = self.points * self.zSpacing / self.zUnitRatio
            self.pointsAligned = np.reshape(self.points,
                                            (self.yPoints, self.xPoints))

            # create the x and y axes without offset
            self.xAxis = np.array(list(range(self.xPoints)))\
                * self.xSpacing / self.xUnitRatio
            self.yAxis = np.array(list(range(self.yPoints)))\
                * self.ySpacing / self.yUnitRatio


    def plot(self):
        '''Plot a surface object using matplotlib

           INPUT: surface object returned from class above

           OUTPUT: None'''

        plt.figure(figsize=(15, 15))
        plt.imshow(self.pointsAligned,
                   extent=[self.xAxis[0], self.xAxis[-1],
                           self.yAxis[-1], self.yAxis[0]])
        plt.colorbar()
